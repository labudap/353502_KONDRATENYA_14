import math
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Dict, Tuple

class SeriesCalculator:
    MAX_ITERATIONS = 500
    
    def __init__(self, eps: float = 0.01):
        self.eps = eps
        self.results = []
    
    def calculate_series(self, x_values: List[float]) -> List[Dict]:
        """Вычисляет значения функции для каждого x"""
        for x in x_values:
            if abs(x) >= 1:
                raise ValueError("|x| должен быть < 1 для сходимости ряда")
                
            n, sum_series = 0, 0.0
            math_value = math.log(1 - x)
            
            for n in range(1, self.MAX_ITERATIONS + 1):
                term = - (x ** n) / n
                sum_series += term
                
                if abs(term) < self.eps:
                    break
            
            self.results.append({
                'x': x,
                'n': n,
                'F(x)': sum_series,
                'Math F(x)': math_value,
                'eps': self.eps
            })
        return self.results
    
    def calculate_statistics(self) -> Dict:
        """Вычисляет статистические характеристики"""
        if not self.results:
            return {}
            
        f_values = [r['F(x)'] for r in self.results]
        math_values = [r['Math F(x)'] for r in self.results]
        diffs = [abs(f - m) for f, m in zip(f_values, math_values)]
        
        return {
            'mean': np.mean(diffs),
            'median': np.median(diffs),
            'mode': max(set(diffs), key=diffs.count),
            'variance': np.var(diffs),
            'std_dev': np.std(diffs)
        }
    
    def plot_results(self, save_path: str = 'plot.png'):
        """Строит графики и сохраняет их в файл"""
        if not self.results:
            return
            
        x_values = [r['x'] for r in self.results]
        f_values = [r['F(x)'] for r in self.results]
        math_values = [r['Math F(x)'] for r in self.results]
        
        plt.figure(figsize=(10, 6))
        
        # График ряда
        plt.plot(x_values, f_values, 'b-', label='Ряд Тейлора', linewidth=2)
        
        # График math.log
        plt.plot(x_values, math_values, 'r--', label='math.log(1-x)', linewidth=2)
        
        # Настройки графика
        plt.title('Сравнение разложения ln(1-x) в ряд и точного значения')
        plt.xlabel('x')
        plt.ylabel('F(x)')
        plt.axhline(0, color='black', linewidth=0.5)
        plt.axvline(0, color='black', linewidth=0.5)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend()
        
        # Аннотация с точностью
        plt.annotate(f'Точность ε = {self.eps}',
                    xy=(0.02, 0.95), xycoords='axes fraction',
                    bbox=dict(boxstyle='round', fc='white', ec='gray'))
        
        plt.savefig(save_path)
        plt.close()

# Пример использования
if __name__ == "__main__":
    # Параметры вычислений
    eps = 0.01
    x_values = np.linspace(-0.9, 0.9, 20)
    
    # Создание и использование калькулятора
    calculator = SeriesCalculator(eps)
    results = calculator.calculate_series(x_values)
    stats = calculator.calculate_statistics()
    
    # Вывод таблицы
    print("| x     | n  | F(x)    | Math F(x) | eps     |")
    print("|-------|----|---------|-----------|---------|")
    for r in results:
        print(f"| {r['x']:.3f} | {r['n']:2} | {r['F(x)']:.6f} | {r['Math F(x)']:.6f} | {r['eps']:.0e} |")
    
    # Вывод статистики
    print("\nСтатистические характеристики:")
    for k, v in stats.items():
        print(f"{k}: {v:.6f}")
    
    # Построение и сохранение графиков
    calculator.plot_results('ln_comparison.png')
    print("\nГрафик сохранен в файл 'ln_comparison.png'")