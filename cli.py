import argparse
from financial_metrics import run_all_metrics

def main():
    parser = argparse.ArgumentParser(description='LBO Decision Engine CLI')
    parser.add_argument('--cashflows', nargs='+', type=float, required=True,
                        help='List of cash flows for analysis (e.g. -100 30 50 60)')
    parser.add_argument('--net_income', type=float, default=50,
                        help='Net income for ROIC calc')
    parser.add_argument('--invested_capital', type=float, default=100,
                        help='Invested capital for ROIC calc')
    args = parser.parse_args()

    print("Running LBO Decision Engine metrics...")
    run_all_metrics(args.cashflows, args.net_income, args.invested_capital)

if __name__ == "__main__":
    main()
