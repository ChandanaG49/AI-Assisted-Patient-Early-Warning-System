import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("heart.csv")

encoder = LabelEncoder()
df["Sex"] = encoder.fit_transform(df["Sex"])

X = df[
    [
        "Age",
        "Sex",
        "RestingBP",
        "Cholesterol",
        "MaxHR",
        "Oldpeak"
    ]
]

y = df["HeartDisease"]

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

def predict(data):
    return model.predict([data])[0]