import pandas as pd
import os

# Folder containing datasets
dataset_folder = "datasets"
all_files = [os.path.join(dataset_folder, f) for f in os.listdir(dataset_folder) if f.endswith(".csv")]

# Load all datasets into a list
dfs = [pd.read_csv(f) for f in all_files]

# Get union of all symptom columns
all_columns = set()
for df in dfs:
    all_columns.update(df.columns[:-1])  # exclude disease/prognosis column

all_columns = sorted(list(all_columns))
merged_df = pd.DataFrame(columns=all_columns + ["disease"])

# Merge datasets
for df in dfs:
    temp_df = pd.DataFrame(columns=merged_df.columns)
    # Fill symptoms
    for col in df.columns[:-1]:
        if col in temp_df.columns:
            temp_df[col] = df[col]
    # Fill disease column
    temp_df["disease"] = df.iloc[:, -1]
    # Fill missing symptom columns with 0
    temp_df = temp_df.fillna(0)
    merged_df = pd.concat([merged_df, temp_df], ignore_index=True)

# Save merged dataset
merged_df.to_csv("datasets/merged_dataset.csv", index=False)
print("Merged dataset saved as datasets/merged_dataset.csv")
