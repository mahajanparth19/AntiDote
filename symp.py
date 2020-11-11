import pandas as pd

df = pd.read_csv('Training.csv')

for col in df.columns:
	col = col.replace("_", " ").title()
	ob = Symptom.objects.create(Name=col)