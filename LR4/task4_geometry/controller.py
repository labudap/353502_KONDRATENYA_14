"""Matrix analysis main controller"""
from .models import GeometricFigure, MyRectangle, MyTriangle, MyCircle, MySquare
from utils.interface import Menu
from abc import ABC, abstractmethod
from math import pi, sqrt
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, Ellipse
import os

class GeometricController:
    def run_task(self):
        main_menu = Menu(
            "Geometry Menu",
            {
                "1": "Create rectangle",
                "2": "Create circle",
                "3": "Create triangle",
                "4": "Create square circumscribed about circle",
                "Q": "Exit"
            }
        )

        while True:
            main_menu.display()
            choice = main_menu.get_choice()

            if choice == "1":
                width = get_valid_input("Enter rectangle width: ")
                height = get_valid_input("Enter rectangle height: ")
                color = input("Enter rectangle color: ")
                rect = MyRectangle(width, height, color)
                print(rect.get_params())
                draw_figure(rect)    
            
            elif choice == "2":
                radius = get_valid_input("Enter circle radius: ")
                color = input("Enter circle color: ")
                circle = MyCircle(radius, color)
                print(circle.get_params())
                draw_figure(circle)
            elif choice == "3":
                side = get_valid_input("Enter triangle side length: ")
                color = input("Enter triangle color: ")
                triangle = MyTriangle(side, color)
                print(triangle.get_params())
                draw_figure(triangle)
            elif choice == "4":
                create_circumscribed_square()
            elif choice == "Q":
                break

def draw_figure(figure: GeometricFigure, label: str = ""):
    """Visualize the figure using matplotlib"""
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_title(f"{figure.name}\n{label}" if label else figure.name)

    if isinstance(figure, MyRectangle):
        patch = Rectangle((0.1, 0.1), figure.width, figure.height, 
                         facecolor=figure.color_obj.color)
    elif isinstance(figure, MySquare):
        patch = Rectangle((0.5, 0.5), figure.side, figure.side, 
                      facecolor=figure.color_obj.color)
    elif isinstance(figure, MyCircle):
        patch = Circle((0.5, 0.5), figure.radius, 
                      facecolor=figure.color_obj.color)
    elif isinstance(figure, MyTriangle):
        points = [(0.1, 0.1), (figure.side, 0.1), (figure.side/2, figure.side*0.866)]
        patch = Polygon(points, facecolor=figure.color_obj.color)
    else:
        raise ValueError("Unsupported figure type")

    ax.add_patch(patch)
    ax.autoscale_view()
    
    # Save to file
    output_dir = "figure_outputs"
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{output_dir}/{figure.name.lower()}_{figure.color_obj.color}.png"
    plt.savefig(filename)
    print(f"Figure saved to {filename}")
    plt.show()

def create_circumscribed_square():
    """Create square circumscribed about a circle"""
    radius = get_valid_input("Enter circle radius: ")
    circle = MyCircle(radius, "blue")
    square_side = 2 * radius
    square = MySquare(square_side, "red")
    
    print("\nCircle parameters:")
    print(circle.get_params())
    print("\nCircumscribed square parameters:")
    print(square.get_params())

    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.set_title( f"Circumscribed square\nCircle radius: {radius}")
    patch = Rectangle((0.5, 0.5), square.width, square.width, facecolor=square.color_obj.color)
    ax.add_patch(patch)
    patch = Circle((0.5 + circle.radius, 0.5 + circle.radius), circle.radius, facecolor=circle.color_obj.color)
    ax.add_patch(patch)
    ax.autoscale_view()
    output_dir = "figure_outputs"
    os.makedirs(output_dir, exist_ok=True)
    filename = f"{output_dir}/{square.name.lower()}_{circle.color_obj.color}.png"
    plt.savefig(filename)
    print(f"Figure saved to {filename}")
    plt.show()
    
    # # Draw both figures
    # draw_figure(circle, "Original circle")
    # draw_figure(square, f"Circumscribed square\nCircle radius: {radius}")


def get_valid_input(prompt: str, type_func=float, min_val=0.1) -> float:
    """Get and validate user input"""
    while True:
        try:
            value = type_func(input(prompt))
            if value < min_val:
                print(f"Value must be >= {min_val}")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a number")