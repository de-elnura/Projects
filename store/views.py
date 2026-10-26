from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Category, Flower, Order, OrderItem

def home(request):
    categories = Category.objects.all()
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())
    return render(request, 'store/index.html', {
        'categories': categories,
        'cart_count': cart_count
    })

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    flowers = category.flowers.all()
    cart = request.session.get('cart', {})
    cart_count = sum(cart.values())
    return render(request, 'store/category_detail.html', {
        'category': category,
        'flowers': flowers,
        'cart_count': cart_count
    })

def add_to_cart(request, flower_id):
    cart = request.session.get('cart', {})
    f_id = str(flower_id)
    cart[f_id] = cart.get(f_id, 0) + 1
    request.session['cart'] = cart
    return JsonResponse({'status': 'ok', 'cart_count': sum(cart.values())})

def update_cart(request, flower_id, action):
    cart = request.session.get('cart', {})
    f_id = str(flower_id)
    if f_id in cart:
        if action == 'increase':
            cart[f_id] += 1
        elif action == 'decrease':
            cart[f_id] -= 1
            if cart[f_id] <= 0:
                del cart[f_id]
        elif action == 'remove':
            del cart[f_id]
    request.session['cart'] = cart
    return redirect('cart_view')

def cart_view(request):
    cart = request.session.get('cart', {})
    items = []
    total_price = 0

    for f_id, qty in list(cart.items()):
        try:
            flower = Flower.objects.get(id=f_id)
            subtotal = flower.price * qty
            total_price += subtotal
            items.append({
                'flower': flower,
                'quantity': qty,
                'subtotal': subtotal
            })
        except Flower.DoesNotExist:
            del cart[f_id]
            request.session['cart'] = cart

    delivery_cost = 0 if total_price > 500000 or total_price == 0 else 30000
    grand_total = total_price + delivery_cost

    return render(request, 'store/cart.html', {
        'items': items,
        'total_price': total_price,
        'delivery_cost': delivery_cost,
        'grand_total': grand_total,
        'cart_count': sum(cart.values())
    })

def checkout(request):
    if request.method == "POST":
        cart = request.session.get('cart', {})
        if not cart:
            return redirect('cart_view')

        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')
        delivery_time = request.POST.get('delivery_time', 'Bugun 2 soatda')
        greeting_card = request.POST.get('greeting_card', '')
        is_anonymous = bool(request.POST.get('is_anonymous'))

        total_price = 0
        order_items_to_create = []

        for f_id, qty in cart.items():
            try:
                flower = Flower.objects.get(id=f_id)
                total_price += flower.price * qty
                order_items_to_create.append((flower, qty, flower.price))
            except Flower.DoesNotExist:
                continue

        delivery_cost = 0 if total_price > 500000 else 30000
        grand_total = total_price + delivery_cost

        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            full_name=full_name,
            phone=phone,
            address=address,
            delivery_time=delivery_time,
            greeting_card=greeting_card,
            is_anonymous=is_anonymous,
            total_price=grand_total,
            status='delivering'
        )

        for flower, qty, price in order_items_to_create:
            OrderItem.objects.create(
                order=order,
                flower=flower,
                quantity=qty,
                price=price
            )

        # Savatni tozalash
        request.session['cart'] = {}
        messages.success(request, f"Buyurtma muvaffaqiyatli qabul qilindi! Buyurtma raqami: #{order.id}")
        return redirect('order_history')

    return redirect('cart_view')

def order_history(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
    else:
        orders = Order.objects.all().order_by('-created_at')

    active_orders_count = orders.filter(status__in=['pending', 'delivering']).count()
    cart = request.session.get('cart', {})
    return render(request, 'store/order_history.html', {
        'orders': orders,
        'active_orders_count': active_orders_count,
        'cart_count': sum(cart.values())
    })

def cancel_order(request, order_id):
    if request.user.is_authenticated:
        order = get_object_or_404(Order, id=order_id, user=request.user)
    else:
        order = get_object_or_404(Order, id=order_id)

    if order.status == 'delivered':
        messages.error(request, f"#{order.id}-sonli buyurtma allaqachon yetkazib berilgan, uni bekor qilib bo'lmaydi.")
    elif order.status == 'cancelled':
        messages.warning(request, f"#{order.id}-sonli buyurtma allaqachon bekor qilingan.")
    else:
        order.status = 'cancelled'
        order.save()
        messages.success(request, f"#{order.id}-sonli buyurtma muvaffaqiyatli bekor qilindi ❌")

    return redirect('order_history')

def cancel_all_orders(request):
    if request.user.is_authenticated:
        active_orders = Order.objects.filter(user=request.user, status__in=['pending', 'delivering'])
    else:
        active_orders = Order.objects.filter(status__in=['pending', 'delivering'])

    count = active_orders.count()
    if count > 0:
        active_orders.update(status='cancelled')
        messages.success(request, f"Barcha faol buyurtmalaringiz ({count} ta) muvaffaqiyatli bekor qilindi ❌")
    else:
        messages.info(request, "Bekor qilish uchun faol buyurtmalar mavjud emas.")

    return redirect('order_history')

def reorder(request, order_id):
    if request.user.is_authenticated:
        order = get_object_or_404(Order, id=order_id, user=request.user)
    else:
        order = get_object_or_404(Order, id=order_id)

    cart = request.session.get('cart', {})
    added_count = 0
    for item in order.items.all():
        if item.flower:
            f_id = str(item.flower.id)
            cart[f_id] = cart.get(f_id, 0) + item.quantity
            added_count += item.quantity

    request.session['cart'] = cart
    if added_count > 0:
        messages.success(request, f"#{order.id}-sonli buyurtmadagi gullar savatingizga qayta qo'shildi!")
        return redirect('cart_view')
    else:
        messages.warning(request, "Buyurtmadagi gullarni savatga qo'shib bo'lmadi.")
        return redirect('order_history')

def profile_view(request):
    cart = request.session.get('cart', {})
    if request.user.is_authenticated:
        orders = Order.objects.filter(user=request.user)
    else:
        orders = Order.objects.all()

    total_spent = sum(order.total_price for order in orders.exclude(status='cancelled'))

    return render(request, 'store/profile.html', {
        'cart_count': sum(cart.values()),
        'total_spent': total_spent,
    })
