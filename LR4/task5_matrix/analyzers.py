"""Matrix analysis operations"""
import numpy as np
from task5_matrix.models import MatrixAnalysisResult

class MatrixAnalyzer:
    @staticmethod
    def sum_below_diagonal(matrix: np.ndarray) -> float:
        return np.sum(np.tril(matrix, -1))

    @staticmethod
    def diag_std_dev(matrix: np.ndarray) -> tuple[float, float]:
        diagonal = np.diag(matrix)
        std_numpy = np.std(diagonal)
        
        # Manual calculation
        mean = np.mean(diagonal)
        squared_diffs = [(x - mean) ** 2 for x in diagonal]
        variance = sum(squared_diffs) / len(diagonal)
        std_manual = np.sqrt(variance)
        
        return std_numpy, std_manual

    @staticmethod
    def analyze_matrix(matrix: np.ndarray) -> MatrixAnalysisResult:
        below_sum = MatrixAnalyzer.sum_below_diagonal(matrix)
        std_np, std_manual = MatrixAnalyzer.diag_std_dev(matrix)
        return MatrixAnalysisResult(
            below_diag_sum=below_sum,
            diag_std_numpy=std_np,
            diag_std_manual=std_manual,
            matrix=matrix
        )