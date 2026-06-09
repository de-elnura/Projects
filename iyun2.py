# 2
# yosh = int(input("Yoshingiz nechida: "))
# if yosh == 70:
#     print("Siz COVID-19 riks guruhida  ekansiz!")
# else:
#     print("Siz COVID-19 riks guruhida emas ekansiz")

# 5
# son1 = float(input("Birinchi sonni kiriting: "))
# son2 = float(input("Ikkinchi sonni kiriting: "))
# if son1 == son2:
#     print("sonlarning hammasi teng va a'lo")

# 6
# son = float(input("Son kiriting: "))
# if son > 0:
#     ildiz = (son)
#     print("Sonning ildizi: ", ildiz)
# else:
#     print("Musbat son kiriting: ")






# 1
# son = float(input("Son kiriting: "))

# if son > 0:
#     print("Sonning kvadrat ildizi:", (son))
# else:
#     print("Musbat son kiriting")

# 2
# yosh = int(input("Yoshingizni kiriting: "))
# if yosh >= 4:
#     print("Sizga kirish bepul")
# if yosh >= 18:
#     print("Kirish 10000")
# if yosh <= 18:
#     print("Sizga kirish 20000")

# 3
# son = int(input("Birinchi sonni kiriting: "))
# son1 = int(input("Ikkinchi sonni kiriting: "))
# print(son)
# print(son1)

# 4
# mahsulotlar = [
#     "olma", "banan", "anor", "uzum", "nok",
#     "shaftoli", "sabzi", "kartoshka", "piyoz", "bodring"
# ]
# savat = []
# for i in range(5):
#     mahsulot = input(f"{i+1}-mahsulotni kiriting: ").lower()
#     savat.append(mahsulot)
# for mahsulot in savat:
#     if mahsulot in mahsulotlar:
#         print(f"{mahsulot} - Mahsulot do'konimizda bor.")
#     else:
#         print(f"{mahsulot} - Mahsulot do'konimizda yo'q.")

# 5
# mahsulotlar = [
#     "olma", "banan", "anor", "uzum", "nok",
#     "shaftoli", "sabzi", "kartoshka", "piyoz", "bodring"
# ]

# bor_mahsulotlar = []
# mavjud_emas = []

# for i in range(5):
#     mahsulot = input(f"{i+1}-mahsulotni kiriting: ").lower()

#     if mahsulot in mahsulotlar:
#         bor_mahsulotlar.append(mahsulot)
#     else:
#         mavjud_emas.append(mahsulot)

# if len(mavjud_emas) == 0:
#     print("Siz so'ragan barcha mahsulotlar do'konimizda bor.")
# else:
#     print("Quyidagi mahsulotlar do'konimizda yo'q:")
#     for mahsulot in mavjud_emas:
#         print(mahsulot)

# 6
# foydalanuvchilar = ("Farangiz", "Zahro", "Ro'zigul", "Charos", "Aygul")
# yangi_login = input("Yangi login kiritng: ")
# if yangi_login in foydalanuvchilar:
#     print("login band, boshqa login tanlang!")
# else:
#     print("Xush kelibsiz, xurmatli foydalanuvchi!")

# 7
# son =  int(input("Istalgan butun sonni kiriting: "))
# for i in range(2,11):
#     if son % i == 0:
#         print(f"{son} soni {i} ga qoldiqsiz 100 % bo'linadi")