from python_a2a import A2AServer, agent, skill
from flask import Flask, request, jsonify
from llm_advice import get_advice_from_groq

app = Flask(__name__)

@agent(name="AdviceAgent", version="1.0", description="Gives care advice based on conditions")
class AdviceAgent(A2AServer):

    @skill(name="give_advice")
    def advice(self, conditions):
        try:
            advice_text = get_advice_from_groq(conditions)
            return {"advice": advice_text}
        except Exception as e:
            return {"advice": f"Error communicating with Groq: {str(e)}"}

    def handle_task(self, task):
        conditions = task["input"].get("conditions", [])
        return self.advice(conditions)

agent_instance = AdviceAgent(app)

@app.route("/task", methods=["POST"])
def task_endpoint():
    data = request.get_json()
    result = agent_instance.handle_task(data)
    return jsonify({"output": result})

if __name__ == "__main__":
    app.run(port=5002)
