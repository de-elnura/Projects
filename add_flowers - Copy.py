import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from store.models import Category, Flower
from django.utils.text import slugify

# Bazani tozalash (eskilarini o'chirish)
Flower.objects.all().delete()
Category.objects.all().delete()

# 5 xil gul toifasi: FAQAT haqiqiy, eng go'zal va hashamatli gullar
catalog_5x5 = [
    {
        "name": "Atirgul",
        "slug": "atirgul",
        "icon": "fa-rose",
        "items": [
            ("Ulkan 101 dona Qirollik Qizil Atirgullari", "https://images.unsplash.com/photo-1525310072745-f49212b5ac6d?w=900&auto=format&fit=crop&q=80", 1650000, 0, "VIP yetkazib berish bepul"),
            ("Eksklyuziv Oq Kelin Atirgullari Buketi", "https://images.unsplash.com/photo-1559563458-527698bf5295?w=900&auto=format&fit=crop&q=80", 850000, 0, "Bugun 1 soatda tezkor"),
            ("Hashamatli Qizil Golland Atirgullari", "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=900&auto=format&fit=crop&q=80", 920000, 30000, "Tezkor kuryer yetkazishi"),
            ("Nafis Pushti Pastel Qirollik Atirgullari", "https://images.unsplash.com/photo-1468327768560-75b778cbb551?w=900&auto=format&fit=crop&q=80", 780000, 0, "Yetkazish bepul"),
            ("Savatdagi 51 dona Oltin Sariq Atirgullar", "https://images.unsplash.com/photo-1508615039623-a25605d2b022?w=900&auto=format&fit=crop&q=80", 1200000, 0, "VIP yetkazib berish"),
        ]
    },
    {
        "name": "Lola",
        "slug": "lola",
        "icon": "fa-seedling",
        "items": [
            ("Ulkan 101 dona Bahoriy Qizil Lolalar", "https://images.unsplash.com/photo-1520763185298-1b434c919102?w=900&auto=format&fit=crop&q=80", 1450000, 0, "VIP yetkazib berish bepul"),
            ("Savatdagi 51 dona Oq Royal Lolalar", "https://images.unsplash.com/photo-1589998059171-988d887df646?w=900&auto=format&fit=crop&q=80", 890000, 0, "Bugun 1-2 soatda"),
            ("Yorqin Oltin Sariq Bahor Lolalari Buketi", "https://images.unsplash.com/photo-1519378058457-4c29a0a2efac?w=900&auto=format&fit=crop&q=80", 680000, 25000, "Tezkor yetkazish"),
            ("Nafis Pushti Baxmalli Lolalar Buketi", "https://images.unsplash.com/photo-1527061011665-3652c757a4d4?w=900&auto=format&fit=crop&q=80", 750000, 0, "Yetkazish bepul"),
            ("Qirollik Ikki Rangli Qizil-Oq Lolalar", "https://images.unsplash.com/photo-1528183429752-a97d0bf99b5a?w=900&auto=format&fit=crop&q=80", 820000, 0, "Maxsus sovutgichda yetkazish"),
        ]
    },
    {
        "name": "Xrizantema",
        "slug": "xrizantema",
        "icon": "fa-sun",
        "items": [
            ("Katta Savatdagi Premium Xrizantemalar", "https://images.unsplash.com/photo-1572454591674-2739f30d8c40?w=900&auto=format&fit=crop&q=80", 690000, 0, "Yetkazish bepul"),
            ("Oltin Sariq Quyosh Xrizantemasi Buketi", "https://images.unsplash.com/photo-1508615039623-a25605d2b022?w=900&auto=format&fit=crop&q=80", 620000, 20000, "1 soatda yetkaziladi"),
            ("Pushti Pastel Nozik Xrizantema Buketi", "https://images.unsplash.com/photo-1490750967868-88aa4486c946?w=900&auto=format&fit=crop&q=80", 650000, 0, "Yetkazish bepul"),
            ("To'q Qizil Olovli Baltika Buketi", "https://images.unsplash.com/photo-1548094891-c4969f4d7421?w=900&auto=format&fit=crop&q=80", 710000, 0, "Bugun 2 soatda"),
            ("Hashamatli 101 dona Miks Xrizantemalar", "https://images.unsplash.com/photo-1519378058457-4c29a0a2efac?w=900&auto=format&fit=crop&q=80", 1150000, 0, "VIP yetkazib berish"),
        ]
    },
    {
        "name": "Siyohrang gul",
        "slug": "siyohrang-gul",
        "icon": "fa-spa",
        "items": [
            ("Qirollik Siyohrang Falenopsis Orxideyasi", "https://images.unsplash.com/photo-1527061011665-3652c757a4d4?w=900&auto=format&fit=crop&q=80", 950000, 0, "Yetkazish bepul"),
            ("Binafsharang Ametist Iris Guldastasi", "https://images.unsplash.com/photo-1468327768560-75b778cbb551?w=900&auto=format&fit=crop&q=80", 760000, 25000, "Bugun 1 soatda"),
            ("Fransuz Siyohrang Premium Lavandasi", "https://images.unsplash.com/photo-1528183429752-a97d0bf99b5a?w=900&auto=format&fit=crop&q=80", 670000, 0, "Yetkazish bepul"),
            ("Siyohrang Negrita Premium Buketi", "https://images.unsplash.com/photo-1516205651411-aef33a44f7c2?w=900&auto=format&fit=crop&q=80", 810000, 0, "Tezkor yetkazish"),
            ("To'q Siyohrang Katta Gortenziya Buketi", "https://images.unsplash.com/photo-1509223197845-458d87318791?w=900&auto=format&fit=crop&q=80", 980000, 0, "VIP kuryer yetkazishi"),
        ]
    },
    {
        "name": "Mini atirgul",
        "slug": "mini-atirgul",
        "icon": "fa-fan",
        "items": [
            ("Hashamatli Savatdagi Mini Atirgullar", "https://images.unsplash.com/photo-1550953159-66d11e865324?w=900&auto=format&fit=crop&q=80", 1100000, 0, "VIP yetkazib berish"),
            ("Nafis Pushti Madam Bombastic Buketi", "https://images.unsplash.com/photo-1468327768560-75b778cbb551?w=900&auto=format&fit=crop&q=80", 890000, 0, "Bugun 2 soatda"),
            ("Qizil Kustovoy Mini Atirgullar Buketi", "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=900&auto=format&fit=crop&q=80", 740000, 0, "Yetkazish bepul"),
            ("Oq Kelin Mini Atirgullari To'plami", "https://images.unsplash.com/photo-1559563458-527698bf5295?w=900&auto=format&fit=crop&q=80", 790000, 20000, "1 soatda yetkaziladi"),
            ("Shaftolirang Shirin Kustovoy Atirgullar", "https://images.unsplash.com/photo-1508615039623-a25605d2b022?w=900&auto=format&fit=crop&q=80", 830000, 0, "Yetkazish bepul"),
        ]
    }
]

flowers_list = []

for cat in catalog_5x5:
    category_obj = Category.objects.create(
        name=cat["name"], 
        slug=cat["slug"], 
        icon=cat["icon"]
    )
    for i, (title, img_url, price, del_cost, del_time) in enumerate(cat["items"], start=1):
        flowers_list.append(
            Flower(
                category=category_obj,
                title=title,
                slug=f"{cat['slug']}-{i}-{slugify(title)}",
                price=price,
                old_price=price + 120000,
                image_url=img_url,
                delivery_type="free" if del_cost == 0 else "standard",
                delivery_price=del_cost,
                delivery_time=del_time,
                rating=5.0,
                reviews_count=25 + i,
                in_stock=True
            )
        )

Flower.objects.bulk_create(flowers_list)
print("Muvaffaqiyatli! Sumka, qasr va boshqa begona rasmlar butunlay tozalanib, faqat haqiqiy gullar joylandi!")