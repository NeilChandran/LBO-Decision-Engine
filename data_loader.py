import pandas as pd
import os

class DataLoader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.data = None

    def load_data(self):
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"{self.filepath} does not exist.")
        ext = self.filepath.split('.')[-1]
        if ext == 'csv':
            self.data = pd.read_csv(self.filepath)
        elif ext in ['xls', 'xlsx']:
            self.data = pd.read_excel(self.filepath)
        else:
            raise ValueError("Unsupported file format.")
        return self.data

    def validate(self, required_cols):
        if self.data is None:
            raise ValueError("No data loaded.")
        missing = [col for col in required_cols if col not in self.data.columns]
        if missing:
            raise ValueError(f"Missing columns: {missing}")
        return True

    def save(self, output_path):
        if self.data is None:
            raise ValueError("No data loaded.")
        self.data.to_csv(output_path, index=False)

if __name__ == "__main__":
    loader = DataLoader("deal_data.csv")
    df = loader.load_data()
    print(f"Loaded data shape: {df.shape}")
    loader.validate(['Revenue', 'EBITDA', 'Debt'])
    loader.save("cleaned_deal_data.csv")
