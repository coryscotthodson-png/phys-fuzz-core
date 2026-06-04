import cavitation_engine as engine
from openai import OpenAI
import csv
import os
import json

class LLMAuditor:
    def __init__(self):
        self.client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
        self.model = "qwen2.5:0.5b"

    def audit(self, history):
        recent = history[-3:] if len(history) > 3 else history
        prompt = f"Previous states: {recent}. Predict next parameters. Output ONLY JSON: {{\"freq\": 0.0, \"amp\": 0.0}}"
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}]
        )
        
        try:
            data = json.loads(response.choices[0].message.content)
            # Defensive access: provide defaults if keys are missing
            freq = float(data.get("freq", 30000.0))
            amp = float(data.get("amp", 500.0))
            return {"freq": freq, "amp": amp}
        except (json.JSONDecodeError, ValueError, TypeError):
            # Fallback if the LLM output is pure garbage
            return {"freq": 30000.0, "amp": 500.0}

class ReactorAdversarialAgent:
    def __init__(self):
        self.state = engine.ReactorState(1e-4, 0.0, False)
        self.auditor = LLMAuditor()
        self.history = []

    def run_adversarial_loop(self, steps=10):
        print(f"Starting v2.0 Cognitive Audit...")
        for i in range(steps):
            params = self.auditor.audit(self.history)
            params['dt'] = 1e-6
            breached = engine.step(self.state, params['freq'], params['amp'], params['dt'])
            self.history.append({"step": i, "params": params, "breached": breached})
            print(f"Step {i}: Params={params}, Breached={breached}")
            if breached: break
        
        os.makedirs("logs", exist_ok=True)
        with open("logs/adversarial_run_v2.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["step", "params", "breached"])
            writer.writeheader()
            writer.writerows(self.history)

if __name__ == "__main__":
    agent = ReactorAdversarialAgent()
    agent.run_adversarial_loop()
