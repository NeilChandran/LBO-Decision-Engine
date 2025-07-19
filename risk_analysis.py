import numpy as np

def scenario_analysis(base_value, up_pct=0.1, down_pct=0.1):
    print("Base value:", base_value)
    print("Upside (+{:.0f}%): {:.2f}".format(up_pct*100, base_value * (1+up_pct)))
    print("Downside (-{:.0f}%): {:.2f}".format(down_pct*100, base_value * (1-down_pct)))

def sensitivity_table(values, var_pct):
    print("\nSensitivity Table:")
    for pct in var_pct:
        print("Change {0:+.0f}%: {1:.2f}".format(pct*100, values * (1 + pct)))

def monte_carlo_simulation(start, mu, sigma, periods, sims=1000):
    np.random.seed(42)
    results = []
    for _ in range(sims):
        val = start
        for _ in range(periods):
            val *= (1 + np.random.normal(mu, sigma))
        results.append(val)
    print("\nMonte Carlo Simulation (mean): {:.2f}".format(np.mean(results)))
    return results

if __name__ == "__main__":
    scenario_analysis(100)
    sensitivity_table(100, [-0.2, -0.1, 0, 0.1, 0.2])
    monte_carlo_simulation(100, 0.05, 0.2, 5)
