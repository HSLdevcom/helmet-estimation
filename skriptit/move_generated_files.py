import os
import shutil

# Define source and target directories
source_dir = "C:/Users/HajduPe/H4_estimointi/Helmet4/helmet_estimation/skriptit/generated/"
target_dir = "C:/Users/HajduPe/helmet-model-system/Scripts/parameters/"

new_names = {
    "destinations_dict.py": "destination_choice.py",
    "modes_dict_calibrated.py": "mode_choice.py",
    # "tour_combinations_dict.py": "tour_generation.py",
    # "demand_dict.py": "departure_time.py",
    # "assignment_dict.py": "assignment.py",
    # "impedance_dict.py": "impedance_transformation.py",
}
# Move and rename files
for filename in os.listdir(source_dir):
    if "yy" not in filename and filename != "modes_dict.py" and filename in new_names:
        source_file = os.path.join(source_dir, filename)
        target_file = os.path.join(target_dir, new_names[filename])
        shutil.copy(source_file, target_file)

print("Files have been moved and renamed.")