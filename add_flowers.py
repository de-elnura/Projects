import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from store.models import Category, Flower
from django.utils.text import slugify

# Bazani tozalash (eskilarini o'chirish)
Flower.objects.all().delete()
Category.objects.all().delete()

# 5 xil gul toifasi: Har biri uchun 100% HAQIQIY, lokal papkaga yuklangan professional fotosuratlar
catalog_5x5 = [
    {
        "name": "Atirgul",
        "slug": "atirgul",
        "icon": "fa-rose",
        "items": [
            ("Ulkan 101 dona Qirollik Qizil Atirgullari", "/media/flowers/atirgul/1_qizil_101.jpg", 1650000, 0, "VIP yetkazib berish bepul"),
            ("Eksklyuziv Oq Kelin Atirgullari Buketi", "/media/flowers/atirgul/2_oq_kelin.jpg", 850000, 0, "Bugun 1 soatda tezkor"),
            ("Hashamatli Qizil Golland Atirgullari", "/media/flowers/atirgul/3_qizil_golland.jpg", 920000, 30000, "Tezkor kuryer yetkazishi"),
            ("Nafis Pushti Pastel Qirollik Atirgullari", "/media/flowers/atirgul/4_pushti_pastel.jpg", 780000, 0, "Yetkazish bepul"),
            ("Savatdagi 51 dona Oltin Sariq Atirgullar", "/media/flowers/atirgul/5_sariq_savat.jpg", 1200000, 0, "VIP yetkazib berish"),
        ]
    },
    {
        "name": "Lola",
        "slug": "lola",
        "icon": "fa-seedling",
        "items": [
            ("Ulkan 101 dona Bahoriy Qizil Lolalar", "/media/flowers/lola/1_qizil_101.jpg", 1450000, 0, "VIP yetkazib berish bepul"),
            ("Savatdagi 51 dona Oq Royal Lolalar", "/media/flowers/lola/2_oq_savat.jpg", 890000, 0, "Bugun 1-2 soatda"),
            ("Yorqin Oltin Sariq Bahor Lolalari Buketi", "/media/flowers/lola/3_sariq_oltin.jpg", 680000, 25000, "Tezkor yetkazish"),
            ("Nafis Pushti Baxmalli Lolalar Buketi", "/media/flowers/lola/4_pushti_baxmal.jpg", 750000, 0, "Yetkazish bepul"),
            ("Qirollik Ikki Rangli Qizil-Oq Lolalar", "/media/flowers/lola/5_bicolor_qirollik.jpg", 820000, 0, "Maxsus sovutgichda yetkazish"),
        ]
    },
    {
        "name": "Xrizantema",
        "slug": "xrizantema",
        "icon": "fa-sun",
        "items": [
            ("Katta Savatdagi Oq Premium Xrizantemalar", "/media/flowers/xrizantema/1_oq_savat.jpg", 690000, 0, "Yetkazish bepul"),
            ("Oltin Sariq Quyosh Xrizantemasi Buketi", "/media/flowers/xrizantema/2_sariq_quyosh.jpg", 620000, 20000, "1 soatda yetkaziladi"),
            ("Pushti Pastel Nozik Xrizantema Buketi", "/media/flowers/xrizantema/3_pushti_pastel.jpg", 650000, 0, "Yetkazish bepul"),
            ("Kuzgi Olovli Rangli Baltika Xrizantemasi", "/media/flowers/xrizantema/4_kuzgi_qizil.jpg", 710000, 0, "Bugun 2 soatda"),
            ("Hashamatli Vazadagi Miks Xrizantemalar", "/media/flowers/xrizantema/5_miks_xrizantema.jpg", 1150000, 0, "VIP yetkazib berish"),
        ]
    },
    {
        "name": "Siyohrang gul",
        "slug": "siyohrang-gul",
        "icon": "fa-spa",
        "items": [
            ("Qirollik Siyohrang Falenopsis Orxideyasi", "/media/flowers/siyohrang/1_orxideya_falenopsis.jpg", 950000, 0, "Yetkazish bepul"),
            ("Binafsharang Ametist Iris Guldastasi", "/media/flowers/siyohrang/2_binafsha_iris.jpg", 760000, 25000, "Bugun 1 soatda"),
            ("Fransuz Siyohrang Premium Lavandasi", "/media/flowers/siyohrang/3_fransuz_lavandasi.jpg", 670000, 0, "Yetkazish bepul"),
            ("Nafis Binafsharang Eustoma Buketi", "/media/flowers/siyohrang/4_siyohrang_eustoma.jpg", 810000, 0, "Tezkor yetkazish"),
            ("To'q Siyohrang Katta Gortenziya Buketi", "/media/flowers/siyohrang/5_katta_gortenziya.jpg", 980000, 0, "VIP kuryer yetkazishi"),
        ]
    },
    {
        "name": "Mini atirgul",
        "slug": "mini-atirgul",
        "icon": "fa-fan",
        "items": [
            ("Hashamatli Savatdagi Mini Kustovoy Atirgullar", "/media/flowers/mini_atirgul/1_savat_mini.jpg", 1100000, 0, "VIP yetkazib berish"),
            ("Nafis Pushti Madam Bombastic Kustovoy Buketi", "/media/flowers/mini_atirgul/2_madame_bombastic.jpg", 890000, 0, "Bugun 2 soatda"),
            ("Qizil Kustovoy Mini Atirgullar Buketi", "/media/flowers/mini_atirgul/3_qizil_kustovoy.jpg", 740000, 0, "Yetkazish bepul"),
            ("Oq Kelin Mini Atirgullari To'plami", "/media/flowers/mini_atirgul/4_oq_kelin_mini.jpg", 790000, 20000, "1 soatda yetkaziladi"),
            ("Shaftolirang Shirin Kustovoy Atirgullar", "/media/flowers/mini_atirgul/5_shaftoli_kustovoy.jpg", 830000, 0, "Yetkazish bepul"),
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
print(f"Muvaffaqiyatli! Barcha {len(flowers_list)} ta gul o'z turiga mansub haqiqiy lokal fotosuratlari bilan bazaga joylandi!")
