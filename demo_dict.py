import pandas as pd

# ----- A dictionary (key–value) -----
person_dict = {
    "Name": "Alice",
    "Age": 30,
    "City": "Berlin"
}

print("Dictionary:")
print(person_dict)
print(type(person_dict), "\n")


# ----- A DataFrame (table with rows + columns) -----
df = pd.DataFrame([
    {"Name": "Alice", "Age": 30, "City": "Berlin"},
    {"Name": "Bob",   "Age": 25, "City": "Paris"}
])

print("DataFrame:")
print(df)
print(type(df), "\n")


# ----- Convert one DataFrame row to a dictionary -----
row_dict = df.iloc[0].to_dict()

print("One row from DataFrame as dictionary:")
print(row_dict)
print(type(row_dict))