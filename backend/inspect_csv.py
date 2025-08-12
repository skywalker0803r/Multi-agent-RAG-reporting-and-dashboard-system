import pandas as pd
import sys
import os

def inspect_csv_columns(file_path: str):
    """Reads a CSV file and prints its column headers."""
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    try:
        df = pd.read_csv(file_path, nrows=0) # Read only header
        print(f"\nColumns in {file_path}:")
        for col in df.columns.tolist():
            print(f"- {col}")
    except Exception as e:
        print(f"Error reading CSV file {file_path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python inspect_csv.py <path_to_csv_file>")
        print("Example: python inspect_csv.py ./warranty-claims.csv")
    else:
        csv_file_path = sys.argv[1]
        inspect_csv_columns(csv_file_path)
