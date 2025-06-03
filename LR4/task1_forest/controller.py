"""Forest analysis main controller"""
from .models import ForestData
from .serializers import ForestSerializer
from .views import ForestView
from utils.file_io import FileHandler
from utils.interface import Menu 

class ForestController:
    def __init__(self):
        self.sample_data = [
            {"species": "Oak", "total": "1500", "healthy": "1200"},
            {"species": "Pine", "total": "2300", "healthy": "2000"},
            {"species": "Birch", "total": "800", "healthy": "650"},
        ]
        self.forest = ForestData(self.sample_data)

    def run_task(self):
        main_menu = Menu(
            "Forest Data Analysis",
            {
                "1": "Show full analysis",
                "2": "Search species",
                "3": "Save data",
                "4": "Load data",
                "Q": "Return to main menu"
            }
        )

        while True:
            main_menu.display()
            choice = main_menu.get_choice()

            if choice == "1":
                ForestView.display_analysis_report(self.forest)
            
            elif choice == "2":
                species = ForestView.get_search_input()
                tree = next(
                    (t for t in self.forest.species if t.name.lower() == species.lower()),
                    None
                )
                if tree:
                    ForestView.display_species_detail(tree)
                else:
                    ForestView.show_message("Species not found")
            
            elif choice == "3":
                format_type = ForestView.get_serialization_choice()
                filename = f"forest_data.{format_type}"
                ForestSerializer.save(self.sample_data, filename, format_type)
                ForestView.show_message(f"Data saved to {filename}")
            
            elif choice == "4":
                format_type = ForestView.get_serialization_choice()
                filename = f"forest_data.{format_type}"
                try:
                    loaded_data = ForestSerializer.load(filename, format_type)
                    self.forest = ForestData(loaded_data)
                    ForestView.show_message(f"Data loaded from {filename}")
                except FileNotFoundError:
                    ForestView.show_message("File not found")
                except Exception as e:
                    ForestView.show_message(f"Error loading file: {str(e)}")
            
            elif choice == "Q":
                break