import calendar
from datetime import datetime
from typing import Dict, Any

class RussianCalendar:
    """Класс для работы с календарем на русском языке"""
    
    MONTH_NAMES = [
        'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
        'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
    ]
    
    WEEKDAY_NAMES = [
        'Понедельник', 'Вторник', 'Среда', 'Четверг',
        'Пятница', 'Суббота', 'Воскресенье'
    ]
    
    def __init__(self, year: int = None, month: int = None):
        """
        Инициализация календаря
        
        Args:
            year (int): Год (по умолчанию текущий)
            month (int): Месяц (по умолчанию текущий)
        """
        self.year = year or datetime.now().year
        self.month = month or datetime.now().month
        self._calendar = calendar.Calendar(firstweekday=calendar.MONDAY)
    
    def get_month_matrix(self) -> list:
        """
        Получить матрицу дней месяца
        
        Returns:
            list: Список недель, где каждая неделя - список дней
        """
        return self._calendar.monthdays2calendar(self.year, self.month)
    
    def get_month_data(self) -> Dict[str, Any]:
        """
        Получить все данные для отображения календаря
        
        Returns:
            dict: Словарь с данными календаря
        """
        # Получаем первый день месяца и количество дней
        first_day = datetime(self.year, self.month, 1)
        total_days = calendar.monthrange(self.year, self.month)[1]
        
        # Получаем день недели для первого дня (0 = понедельник, 6 = воскресенье)
        first_weekday = first_day.weekday()
        
        # Получаем дни предыдущего месяца
        if self.month == 1:
            prev_month = 12
            prev_year = self.year - 1
        else:
            prev_month = self.month - 1
            prev_year = self.year
        prev_month_days = calendar.monthrange(prev_year, prev_month)[1]
        
        # Получаем текущий день (если это текущий месяц и год)
        now = datetime.now()
        current_day = None
        if now.year == self.year and now.month == self.month:
            current_day = now.day
        
        # Формируем данные календаря
        calendar_data = {
            'year': self.year,
            'month': self.month,
            'month_name': self.MONTH_NAMES[self.month - 1],
            'weekday_names': self.WEEKDAY_NAMES,
            'first_weekday': first_weekday,
            'total_days': total_days,
            'prev_month_days': prev_month_days,
            'today': current_day,
            'matrix': self.get_month_matrix()
        }
        
        return calendar_data
    
    @classmethod
    def get_month_name(cls, month: int) -> str:
        """
        Получить название месяца
        
        Args:
            month (int): Номер месяца (1-12)
            
        Returns:
            str: Название месяца на русском языке
        """
        return cls.MONTH_NAMES[month - 1]
    
    @classmethod
    def get_weekday_name(cls, weekday: int) -> str:
        """
        Получить название дня недели
        
        Args:
            weekday (int): Номер дня недели (0-6, где 0 - понедельник)
            
        Returns:
            str: Название дня недели на русском языке
        """
        return cls.WEEKDAY_NAMES[weekday] 