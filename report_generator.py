import pandas as pd

class ReportGenerator:
    def __init__(self):
        self.sections = []

    def add_section(self, title, content):
        self.sections.append({'title': title, 'content': content})

    def to_text(self, file_path="lbo_report.txt"):
        with open(file_path, 'w') as f:
            for s in self.sections:
                f.write(f"### {s['title']}\n")
                f.write(f"{s['content']}\n\n")
        print(f"Report saved to {file_path}")

    def to_excel(self, data, file_path="lbo_report.xlsx"):
        with pd.ExcelWriter(file_path) as writer:
            for name, df in data.items():
                df.to_excel(writer, sheet_name=name)
        print(f"Excel report saved to {file_path}")

if __name__ == "__main__":
    rep = ReportGenerator()
    rep.add_section("Executive Summary", "This is a sample LBO analysis report.")
    rep.add_section("Key Metrics", "IRR: 23.1%, MOIC: 2.3x, Payback: 4 years.")
    rep.to_text()
    data = {"Summary": pd.DataFrame({'Metric': ['IRR', 'MOIC'], 'Value': [0.231, 2.3]})}
    rep.to_excel(data)

