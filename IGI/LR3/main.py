from taylor import calculate_ln_series
from input_validation import float_input
from input_validation import int_input
from substract import substract
from space_comma_counter import space_comma_counter
from text_analyser import text_analyser
from list_analyser import analys_list
import math

def main():
    while True:
        while True:
            print("Выберите номер задания, которое вы хотели бы запустить: ")
            chosen_task = int_input()
            if chosen_task > 0 and chosen_task < 6:
                break
            print("Введите корректное значение!")
        match chosen_task:
            case 1:
                print("Введите значение x (|x| < 1): ")
                while True:
                    x = float_input()
                    if x <= -1 or x >= 1:
                        print("Введите корректное значение!") 
                        continue
                    break
                print("Введите значение точности eps: ")
                eps = float(float_input())
                n, F_x = calculate_ln_series(x, eps)
                math_F_x = math.log(1 - x)
                print("\nРезультаты вычислений:")
                print("|   x   |  n  |   F(x)   | Math F(x) |  eps  |")
                print("|-------|-----|----------|-----------|-------|")
                print(f"| {x:.4f} | {n:3} | {F_x:.6f} | {math_F_x:.6f} | {eps:.6f} |")
            case 2:
                substract()
            case 3:
                space_counter, comma_counter = space_comma_counter()
                print("Количество пробелов в тексте: ", space_counter)
                print("Количество запятых в тексте: ",  comma_counter)
            case 4:
                text_analyser()
            case 5:
                analys_list()
        print("Выберите:\n"
        "1. Если хотите продолжить выполнение программы\n"
        "2. Если хотите завершить выполнение программы")
        while True:
            chose = int_input()
            if chose == 1 or chose == 2:
                break
            print("Выберите 1 или 2!")
        match chose:
            case 1:
                continue
            case 2:
                break
            
if __name__ == "__main__":
    main()