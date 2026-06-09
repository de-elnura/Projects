
while true:
    print("1. O'quvchi qo'shish")
    print("2. O'quvchilarni ko'rsatish")
    print("3. Chiqish")

    chice = input("Tanlovingiz: ")

    if choice == "1":
     def add_student(full_name, age, grade): 
        full_name = input("ism:")
    age = (input("yosh:"))
    grade = input("bahosi:")

with open("students.txt", "a") as file:
    file.write(f"{full_name}, {age}, {grade}/n")

    add_student("", "", "")
    print("O'quvchilar saqlandi")
    elif choice == "2:"
def show_students():
     with open("students.txt", "r") as file:
        students = file.readlines()
        for student in students:
            print(student.strip(), "/n")
      
javob = input("O'quvchilarni ko'rsatilsinmi? (ha/yo'q): ")
if javob == "ha":
    show_students()
else:
    print("O'quvchilar ko'rsatilmaydi.")
    elif choice == "3":
    print("Dasturdan chiqish")
    break 
else:
print("Noto'g'ri tanlov. Iltimos, qaytadan urinib ko'ring.")
students = ["charos", "aygul", "farangiz", "zahro"]
name_to_delete = input("O'chirmoqchi bo'lgan o'quvchi ismini kiriting: ")
if name_to_delete in students:
    students. remove(name_to_delete)
    print(f"{name_to_delete} o'chirildi.")
else:
    print("Bunday o'quvchi topilmaydi.")
print("Yangi ro'yxat:", students)