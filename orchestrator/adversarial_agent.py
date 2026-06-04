import cavitation_engine as engine
from openai import OpenAI
import csv
import os
import json

class LLMAuditor:
    def __init__(self):
        # Local Ollama endpoint
        self.client = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")
        self.model = "llama3.1"

    def audit(self, history):
        # Summarize history for the local LLM
        recent = history[-3:] if len(history) > 3 else history
        # Doubled {{ and }} escape the braces for the LLM prompt
        prompt = f"Previous reactor states: {recent}. Predict next (freq, amp) parameters to stress-test stability. Output ONLY JSON: {{\"freq\": float, \"amp\": float}}"
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)

class ReactorAdversarialAgent:
    def __init__(self):
        self.state = engine.ReactorState(1e-4, 0.0, False)
        self.auditor = LLMAuditor()
        self.history = []

    def run_adversarial_loop(self, steps=10):
        print(f"Starting v2.0 Cognitive Audit...")
        for i in range(steps):
            params = self.auditor.audit(self.history)
            # Ensure safe default dt
            params['dt'] = 1e-6
            breached = engine.step(self.state, float(params['freq']), float(params['amp']), params['dt'])
            self.history.append({"step": i, "params": params, "breached": breached})
            print(f"Step {i}: Params={params}, Breached={breached}")
            if breached: 
                print("Breach achieved by AI auditor!")
                break
        
        os.makedirs("logs", exist_ok=True)
        with open("logs/adversarial_run_v2.csv", "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=["step", "params", "breached"])
            writer.writeheader()
            writer.writerows(self.history)

if __name__ == "__main__":
    agent = ReactorAdversarialAgent()
    agent.run_adversarial_loop()
