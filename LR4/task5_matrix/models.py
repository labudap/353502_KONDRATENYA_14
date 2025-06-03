"""Matrix analysis models"""
import numpy as np
from dataclasses import dataclass

@dataclass
class MatrixAnalysisResult:
    below_diag_sum: float
    diag_std_numpy: float
    diag_std_manual: float
    matrix: np.ndarray

class MatrixGenerator:
    def __init__(self, rows: int = 5, cols: int = 5, min_val: int = 1, max_val: int = 100):
        self.rows = rows
        self.cols = cols
        self.min_val = min_val
        self.max_val = max_val
    
    def generate(self) -> np.ndarray:
        return np.random.randint(self.min_val, self.max_val, size=(self.rows, self.cols))