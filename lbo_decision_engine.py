
import json
import random
from math import pow
from enum import Enum
from statistics import mean, stdev
from dataclasses import dataclass, field
from typing import List

# === Constants ===
YEARS = 5
DEFAULT_DISCOUNT_RATE = 0.12
team_name = "MANKEY_PE"

class Dir(str, Enum):
    INVEST = "INVEST"
    PASS = "PASS"

@dataclass
class Deal:
    name: str
    ebitda: float
    entry_multiple: float
    exit_multiple: float
    revenue_growth: float
    margin: float
    leverage: float
    interest_rate: float
    risk_score: float = 0.0
    sector: str = "General"

@dataclass
class DealResult:
    name: str
    decision: Dir
    irr: float
    moic: float
    risk_adjusted_irr: float
    commentary: str

class RiskModel:
    def assess(self, deal: Deal) -> float:
        risk = 0
        if deal.leverage > 0.65:
            risk += 2
        elif deal.leverage > 0.5:
            risk += 1

        if deal.margin < 0.15:
            risk += 1
        elif deal.margin < 0.1:
            risk += 2

        if deal.sector.lower() in {"biotech", "crypto"}:
            risk += 2
        elif deal.sector.lower() in {"industrial", "consumer"}:
            risk += 0.5

        return risk

class FinancialModel:
    def simulate_cashflows(self, deal: Deal) -> List[float]:
        ebitda = deal.ebitda
        debt = deal.ebitda * deal.entry_multiple * deal.leverage
        cash_flows = []

        for year in range(YEARS):
            growth_factor = pow(1 + deal.revenue_growth, year + 1)
            current_ebitda = ebitda * growth_factor
            interest = debt * deal.interest_rate
            annual_cash = current_ebitda - interest
            cash_flows.append(annual_cash)

        return cash_flows

    def compute_exit_value(self, deal: Deal) -> float:
        ebitda_final = deal.ebitda * pow(1 + deal.revenue_growth, YEARS)
        return ebitda_final * deal.exit_multiple

    def compute_irr_and_moic(self, equity: float, cash_flows: List[float], exit_value: float) -> (float, float):
        total_return = sum(cash_flows) + exit_value
        moic = total_return / equity
        irr = ((total_return / equity) ** (1 / YEARS)) - 1
        return irr, moic

class CommentaryEngine:
    def generate(self, deal: Deal, irr: float, moic: float, risk_score: float) -> str:
        comments = []
        if irr > 0.25:
            comments.append("High return potential")
        elif irr < 0.1:
            comments.append("Weak IRR")

        if moic > 2.5:
            comments.append("Strong value multiple")
        elif moic < 1.5:
            comments.append("Low MOIC")

        if risk_score > 3:
            comments.append("Elevated risk profile")
        elif risk_score <= 1:
            comments.append("Low risk")

        return ", ".join(comments) if comments else "Neutral outlook"

class StateManager:
    def __init__(self, deals: List[Deal]):
        self.deals = deals
        self.results: List[DealResult] = []
        self.risk_model = RiskModel()
        self.fin_model = FinancialModel()
        self.commentary = CommentaryEngine()

    def evaluate_deals(self):
        for deal in self.deals:
            deal.risk_score = self.risk_model.assess(deal)

            purchase_price = deal.ebitda * deal.entry_multiple
            equity = purchase_price * (1 - deal.leverage)
            cash_flows = self.fin_model.simulate_cashflows(deal)
            exit_value = self.fin_model.compute_exit_value(deal)
            irr, moic = self.fin_model.compute_irr_and_moic(equity, cash_flows, exit_value)

            adjusted_irr = irr - (deal.risk_score * 0.01)

            decision = Dir.INVEST if adjusted_irr > 0.15 and moic >= 2 else Dir.PASS
            commentary = self.commentary.generate(deal, irr, moic, deal.risk_score)

            self.results.append(DealResult(
                name=deal.name,
                decision=decision,
                irr=irr,
                moic=moic,
                risk_adjusted_irr=adjusted_irr,
                commentary=commentary
            ))

    def print_summary(self):
        print(f"=== {team_name} | LBO Evaluation Report ===")
        for r in self.results:
            print(f"\nDeal: {r.name}")
            print(f"  Decision: {r.decision}")
            print(f"  IRR: {r.irr*100:.2f}%")
            print(f"  Risk-Adjusted IRR: {r.risk_adjusted_irr*100:.2f}%")
            print(f"  MOIC: {r.moic:.2f}x")
            print(f"  Notes: {r.commentary}")

def generate_mock_deals(n: int = 100) -> List[Deal]:
    sectors = ["Industrial", "Consumer", "Biotech", "Tech", "Crypto", "Healthcare"]
    return [
        Deal(
            name=f"TargetCo_{i}",
            ebitda=random.randint(3_000_000, 15_000_000),
            entry_multiple=random.uniform(6, 10),
            exit_multiple=random.uniform(7, 12),
            revenue_growth=random.uniform(0.05, 0.2),
            margin=random.uniform(0.1, 0.3),
            leverage=random.uniform(0.4, 0.7),
            interest_rate=random.uniform(0.05, 0.09),
            sector=random.choice(sectors)
        )
        for i in range(n)
    ]

def main():
    deals = generate_mock_deals()
    manager = StateManager(deals)
    manager.evaluate_deals()
    manager.print_summary()

if __name__ == "__main__":
    main()
