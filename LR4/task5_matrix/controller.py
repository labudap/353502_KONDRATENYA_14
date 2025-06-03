"""Matrix analysis main controller"""
import numpy as np
from .models import MatrixGenerator, MatrixAnalysisResult
from .analyzers import MatrixAnalyzer
from utils.interface import Menu, get_valid_input

class MatrixController:
    def run_task(self):
        main_menu = Menu(
            "Matrix Analysis",
            {
                "1": "Generate default matrix (5x5)",
                "2": "Custom matrix size",
                "Q": "Return to main menu"
            }
        )

        while True:
            main_menu.display()
            choice = main_menu.get_choice()

            if choice == "1":
                self.analyze_matrix(MatrixGenerator().generate())
            
            elif choice == "2":
                rows = int(get_valid_input(
                    "Enter rows (2-10): ",
                    lambda x: x.isdigit() and 2 <= int(x) <= 10
                ))
                cols = int(get_valid_input(
                    "Enter columns (2-10): ",
                    lambda x: x.isdigit() and 2 <= int(x) <= 10
                ))
                self.analyze_matrix(MatrixGenerator(rows, cols).generate())
            
            elif choice == "Q":
                break

    def analyze_matrix(self, matrix: np.ndarray):
        result = MatrixAnalyzer.analyze_matrix(matrix)
        
        print("\n=== MATRIX ANALYSIS ===")
        print("\nGenerated Matrix:")
        print(result.matrix)
        
        print("\nResults:")
        print(f"Sum below main diagonal: {result.below_diag_sum}")
        print(f"Diagonal std (numpy): {result.diag_std_numpy:.2f}")
        print(f"Diagonal std (manual): {result.diag_std_manual:.2f}")
        
        if not np.allclose(result.diag_std_numpy, result.diag_std_manual, rtol=1e-3):
            print("\nWarning: Numpy and manual std dev calculations differ!")