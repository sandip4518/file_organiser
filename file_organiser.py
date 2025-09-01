import os
import shutil
from pathlib import Path

# ==== CONFIGURATION ====
# Change this to the folder you want to organize
FOLDER_TO_TRACK = r"C:\Users\Sandi\Downloads"

# File type mapping
FILE_TYPES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv"],
    "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx"],
    "Audio": [".mp3", ".wav", ".aac"],
    "Code": [".py", ".java", ".cpp", ".js", ".html", ".css"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"]
}

# ==== SCRIPT ====
def organize_folder():
    folder_path = Path(FOLDER_TO_TRACK)

    if not folder_path.exists():
        print(f"Folder {folder_path} does not exist!")
        return

    for file in folder_path.iterdir():
        if file.is_file():
            file_ext = file.suffix.lower()

            moved = False
            for folder_name, extensions in FILE_TYPES.items():
                if file_ext in extensions:
                    target_folder = folder_path / folder_name
                    target_folder.mkdir(exist_ok=True)
                    shutil.move(str(file), str(target_folder / file.name))
                    print(f"Moved {file.name} → {folder_name}")
                    moved = True
                    break

            if not moved:
                other_folder = folder_path / "Others"
                other_folder.mkdir(exist_ok=True)
                shutil.move(str(file), str(other_folder / file.name))
                print(f"Moved {file.name} → Others")

if __name__ == "__main__":
    organize_folder()
    print("✅ Folder organized successfully!")
