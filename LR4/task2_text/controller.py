"""Text analysis main controller"""
from .models import TextStats
from .analyzers import TextAnalyzer
from utils.file_io import FileHandler
from utils.interface import Menu, get_valid_input
import zipfile
import os
from datetime import datetime

class TextController:
    def run_task(self):
        main_menu = Menu(
            "Text Analysis",
            {
                "1": "Analyze input text",
                "2": "Analyze text file",
                "Q": "Return to main menu"
            }
        )

        while True:
            main_menu.display()
            choice = main_menu.get_choice()

            if choice == "1":
                text = input("\nEnter text to analyze:\n")
                self.process_text(text)
            
            elif choice == "2":
                filename = get_valid_input(
                    "Enter filename: ",
                    lambda x: bool(x.strip()),
                    "Filename cannot be empty"
                )
                try:
                    text = FileHandler.read_text(filename)
                    self.process_text(text, source=filename)
                except FileNotFoundError:
                    print("File not found")
            
            elif choice == "Q":
                break

    def process_text(self, text: str, source: str = "input"):
        analysis = TextAnalyzer.analyze_text(text)
        
        # Generate timestamp for unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        zip_filename = f"text_analysis_{timestamp}.zip"
        txt_filename = "analysis_results.txt"
        
        # Create and save to ZIP archive
        with zipfile.ZipFile(zip_filename, 'w') as zipf:
            # Add analysis results as text file
            zipf.writestr(txt_filename, str(analysis))
            
            # If source is a file, add original file to archive
            if os.path.exists(source) and source != "input":
                zipf.write(source, os.path.basename(source))
        
        print(f"\nAnalysis results saved to {zip_filename}")
        print(f"Archive contains: {', '.join(zipf.namelist())}")
        
        # Print analysis to console
        print("\nAnalysis Results:")
        print(analysis)