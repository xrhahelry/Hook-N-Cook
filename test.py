import pandas as pd

# Sample original data
data = {"Category": ["A", "B", "C"], "Value": [10, 20, 30]}
df = pd.DataFrame(data)

# New row data
new_row = {"Category": "B", "Value": 15}

# One-hot encode the original DataFrame
df_encoded = pd.get_dummies(df, columns=["Category"])
print("One-hot Encoded DataFrame:")
print(df_encoded)

# Create a DataFrame from the new row
new_row_df = pd.DataFrame([new_row])

# One-hot encode the new row using the same structure
new_row_encoded = pd.get_dummies(new_row_df, columns=["Category"])

# Align the new row encoded DataFrame with the original encoded DataFrame
new_row_encoded = new_row_encoded.reindex(columns=df_encoded.columns, fill_value=0)
print("\nOne-hot Encoded New Row:")
print(new_row_encoded)
