"""Forest analysis user interface"""
from utils.interface import Menu, get_valid_input

class ForestView:
    @staticmethod
    def display_analysis_report(forest_data):
        print("\n=== FOREST ANALYSIS REPORT ===")
        print(f"\nTotal trees: {forest_data.total_trees}")
        print(f"Healthy trees: {forest_data.total_healthy}")
        print(f"Sick percentage: {forest_data.total_sick_percentage:.1f}%")
        
        print("\nBy Species:")
        for tree in forest_data.species:
            print(f"{tree.name:<10} {tree.total:>6} total "
                  f"{tree.healthy:>6} healthy "
                  f"{tree.sick_percentage:>6.1f}% sick")

    @staticmethod
    def display_species_detail(tree):
        print(f"\n{tree.name} Details:")
        print(f"- Total: {tree.total}")
        print(f"- Healthy: {tree.healthy}")
        print(f"- Sick: {tree.sick_count} ({tree.sick_percentage:.1f}%)")

    @staticmethod
    def get_search_input():
        return input("\nEnter tree species to search: ").strip()

    @staticmethod
    def show_message(message: str):
        print(message)

    @staticmethod
    def get_serialization_choice():
        return get_valid_input(
            "Choose format (csv/pickle): ",
            lambda x: x.lower() in ['csv', 'pickle'],
            "Please enter 'csv' or 'pickle'"
        )