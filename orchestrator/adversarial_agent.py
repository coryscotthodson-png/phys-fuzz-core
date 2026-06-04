import cavitation_engine as engine
import csv
import os

agent = engine.ReactorState(1e-4, 0.0, False)
params = {"freq": 32000.0, "amp": 350.0, "dt": 1e-6}
breached = engine.step(agent, params["freq"], params["amp"], params["dt"])

os.makedirs("logs", exist_ok=True)
with open("logs/adversarial_run_001.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["step", "breached"])
    writer.writeheader()
    writer.writerow({"step": 0, "breached": breached})

print(f"Run complete. Breach status: {breached}")
