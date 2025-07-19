import numpy as np

def calculate_irr(cash_flows):
    return np.irr(cash_flows)

def calculate_moic(cash_flows):
    invested = -sum([cf for cf in cash_flows if cf < 0])
    returned = sum([cf for cf in cash_flows if cf > 0])
    return returned / invested if invested else 0

def calculate_roic(net_income, invested_capital):
    return net_income / invested_capital if invested_capital else 0

def payback_period(cash_flows):
    cumulative = 0
    for i, cf in enumerate(cash_flows, 1):
        cumulative += cf
        if cumulative >= 0:
            return i
    return None

def run_all_metrics(cash_flows, net_income, invested_capital):
    print("IRR:", round(calculate_irr(cash_flows) * 100, 2), "%")
    print("MOIC:", round(calculate_moic(cash_flows), 2))
    print("ROIC:", round(calculate_roic(net_income, invested_capital) * 100, 2), "%")
    print("Payback period:", payback_period(cash_flows), "years")

if __name__ == "__main__":
    flows = [-100, 20, 30, 40, 50, 70]
    ni = 50
    ic = 100
    run_all_metrics(flows, ni, ic)

