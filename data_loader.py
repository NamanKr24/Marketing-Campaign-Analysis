import pandas as pd

def load_bank_data(file_path):
    df = pd.read_csv(file_path)
    print("Dataset loaded successfully!")
    return df