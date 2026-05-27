import pandas as pd
import os

# Folder containing A–Z gesture CSVs
data_folder = "gesture_data"

# List of all gesture files
gesture_files = [f"{chr(i)}_data.csv" for i in range(ord('A'), ord('Z')+1)]

# Combine all into one DataFrame
all_data = pd.DataFrame()

for file in gesture_files:
    path = os.path.join(data_folder, file)
    if os.path.exists(path):
        df = pd.read_csv(path)
        all_data = pd.concat([all_data, df], ignore_index=True)
    else:
        print(f"File not found: {file}")

# Save combined dataset
all_data.to_csv("combined_gesture_data.csv", index=False)
print("✅ Combined dataset saved as combined_gesture_data.csv")
