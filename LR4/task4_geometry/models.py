from abc import ABC, abstractmethod
from math import pi, sqrt
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle, Polygon, Ellipse
import os

# --- Abstract Base Classes ---
class GeometricFigure(ABC):
    """Abstract base class for geometric figures"""
    @abstractmethod
    def area(self) -> float:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

class FigureColor:
    """Class representing figure color"""
    def __init__(self, color: str):
        self._color = color.lower()

    @property
    def color(self) -> str:
        return self._color

    @color.setter
    def color(self, value: str):
        if not isinstance(value, str):
            raise ValueError("Color must be a string")
        self._color = value.lower()

# --- Concrete Shape Classes ---
class MyRectangle(GeometricFigure):
    """Rectangle class inheriting from GeometricFigure"""
    name = "Rectangle"

    def __init__(self, width: float, height: float, color: str):
        self.width = width
        self.height = height
        self.color_obj = FigureColor(color)

    def area(self) -> float:
        return self.width * self.height

    def get_params(self) -> str:
        return "Shape: {name}\nWidth: {width}\nHeight: {height}\nColor: {color}\nArea: {area:.2f}".format(
            name=self.name,
            width=self.width,
            height=self.height,
            color=self.color_obj.color,
            area=self.area()
        )

class MyCircle(GeometricFigure):
    """Circle class inheriting from GeometricFigure"""
    name = "Circle"

    def __init__(self, radius: float, color: str):
        self.radius = radius
        self.color_obj = FigureColor(color)

    def area(self) -> float:
        return pi * self.radius ** 2

    def get_params(self) -> str:
        return "Shape: {name}\nRadius: {radius}\nColor: {color}\nArea: {area:.2f}".format(
            name=self.name,
            radius=self.radius,
            color=self.color_obj.color,
            area=self.area()
        )

class MySquare(MyRectangle):
    """Square class inheriting from Rectangle"""
    name = "Square"

    def __init__(self, side: float, color: str):
        super().__init__(side, side, color)

    def get_params(self) -> str:
        return "Shape: {name}\nSide: {side}\nColor: {color}\nArea: {area:.2f}".format(
            name=self.name,
            side=self.width,
            color=self.color_obj.color,
            area=self.area()
        )

class MyTriangle(GeometricFigure):
    """Equilateral Triangle class"""
    name = "Triangle"

    def __init__(self, side: float, color: str):
        self.side = side
        self.color_obj = FigureColor(color)

    def area(self) -> float:
        return (sqrt(3) / 4 * self.side ** 2)

    def get_params(self) -> str:
        return "Shape: {name}\nSide: {side}\nColor: {color}\nArea: {area:.2f}".format(
            name=self.name,
            side=self.side,
            color=self.color_obj.color,
            area=self.area()
        )
