import pandas as pd

# Load and clean dataset
df = pd.read_csv(r"route or path to the dataset in your local machine")
sym_col = [col for col in df.columns if col.startswith("Symptom")]

df[sym_col] = df[sym_col].fillna("").apply(lambda col: col.map(lambda x: x.strip().lower().replace(" ", "_")))
df = df.dropna(subset=["Disease"])
df["Disease"] = df["Disease"].str.strip().str.lower()

def find_diseases(input_symptoms):
    input_symptoms = [sym.lower().strip().replace(" ", "_") for sym in input_symptoms if sym.strip()] 
    if not input_symptoms:
        return []

    disease_scores = {}

    for _, row in df.iterrows():
        disease = row["Disease"]
        row_symptoms = [row[col] for col in sym_col if row[col]]
        matches = set(input_symptoms).intersection(set(row_symptoms))

        if matches:
            score = len(matches) / len(input_symptoms)
            disease_scores[disease] = max(disease_scores.get(disease, 0), round(score, 2))

    return sorted([(d, s) for d, s in disease_scores.items() if s >= 0.3], key=lambda x: x[1], reverse=True)[0:3]

