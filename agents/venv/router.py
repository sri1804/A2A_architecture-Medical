import requests
import json

def call_agent(url, skill_name, input_data):
    payload = {
        "skill": skill_name,
        "input": input_data
    }

    headers = {
        "Content-Type": "application/json"
    }

    # print(f"\nCalling agent at {url} with: {payload}")
    # Use json=payload instead of json.dumps
    response = requests.post(url, json=payload, headers=headers)

    # print("Response status code:", response.status_code)
    # print("Response text:", response.text)

    try:
        return response.json().get("output", {})
    except Exception as e:
        print("Error extracting output:", e)
        return {}

def main():
    symptoms = input("Describe your symptoms: ")
    result1 = call_agent("http://localhost:5001/task", "identify_symptoms", {"symptoms": symptoms})
    conditions = result1.get("Conditions", [])
    diseases_only = [c["disease"] for c in conditions]
    #print("\nConditions Identified:", conditions)

    result2 = call_agent("http://localhost:5002/task", "give_advice",  {"conditions": diseases_only})
    print("\nAdvice Given:", result2.get("advice", []))

if __name__ == "__main__":
    main()
