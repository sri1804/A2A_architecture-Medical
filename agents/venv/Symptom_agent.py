# from python_a2a import A2AServer, agent, skill

# @agent(name="SymptomAgent", version="1.0", description="Identifies possible conditions from symptons")
# class SymptomAgent(A2AServer):

#     @skill(name="identify_symptoms")
#     def check_symptoms(self, symptoms):
#         result=[]
#         if "fever" in symptoms and "cough" in symptoms:
#             result.append("Flu")
#         if "headache" in symptoms:
#             result.append("Migraine")
#         return {"conditions": result}
    
#     def handle_task(self, task):
#         symptoms=task.input.get("symptoms","").lower()
#         return self.check_symptoms(symptoms)

# if __name__=="__main__":
#     agent=SymptomAgent()
#     agent.run(port=5001)

from python_a2a import A2AServer, agent, skill
from flask import Flask, request, jsonify
from Datasets.Symptom import find_diseases
from llama_model import process_symptom_text

app = Flask(__name__)

@agent(name="SymptomAgent", version="1.0", description="Identifies possible conditions from symptoms")
class SymptomAgent(A2AServer):

    def __init__(self, app):
        super().__init__(app)

    @skill(name="identify_symptoms")
    def check_symptoms(self, input_data):
        symptoms_str = input_data.get("symptoms", "")
        symptoms_list = process_symptom_text(symptoms_str)
        print("Extracted symptoms list:", symptoms_list)

        predictions = find_diseases(symptoms_list)
        print("Predictions:", predictions)

        result = [{"disease": disease, "match": f"{score * 100:.0f}%"} for disease, score in predictions]

        return {"Conditions": result}



    def handle_task(self, task):
        input_data = task.get("input", {})
        return self.check_symptoms(input_data)

agent_instance = SymptomAgent(app)

@app.route("/task", methods=["POST"])
def task_endpoint():
    data = request.get_json()
    result = agent_instance.handle_task(data)
    return jsonify({"output": result})


if __name__ == "__main__":
    app.run(port=5001)
