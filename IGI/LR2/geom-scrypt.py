import geometric_lib.circle
import geometric_lib.square

shapeID = ""

while True:
    print("""
Какая фигура вас интересует?
1) Круг
2) Квадрат
""")
    shapeID = input()
    if shapeID == "1" or shapeID == "2":
        break
    else:
        print("Ошибка ввода!!!")

infoID = ""

while True:
    print("""
Что вы хотите узнать?
1) Периметр
2) Площадь
    """)
    infoID = input()
    if infoID == "1" or infoID == "2":
        break
    else:
        print("Ошибка ввода!!!")

if shapeID == "1":
    print("Введите радиус круга:\n")
    R = float(input())
    if infoID == "1":
        print(f"Периметр круга: {geometric_lib.circle.perimeter(R)}!")
    else:
        print(f"Площадь круга: {geometric_lib.circle.area(R)}!")
else:
    print("Введите длину стороны квадрата:\n")
    a = float(input())
    if infoID == "1":
        print(f"Периметр квадрата: {geometric_lib.square.perimeter(a)}!")
    else:
        print(f"Площадь квадрата: {geometric_lib.square.area(a)}!")
