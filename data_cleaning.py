import pandas as pd
from datetime import datetime

# Step 1: Load the Data and Inspect It
df = pd.read_csv("employees.csv")

# Standardize column names
df.columns = df.columns.str.strip().str.lower()
print(df.info())
print(df.head())

# Step 2: Handle Missing Values
df = df.assign(
    name=df['name'].fillna("Unknown"),
    department=df['department'].fillna("Unassigned"),
    salary=df['salary'].fillna(df['salary'].mean())
)
df.dropna(subset=['age', 'dob'], inplace=True)

# Rename columns if necessary
column_renames = {
    'joining date': 'joining_date',
    'dob': 'dob',
    'performance score': 'performance_score'
}
df.rename(columns={k: v for k, v in column_renames.items() if k in df.columns}, inplace=True)

# Step 3: Standardize Column Formats
df['dob'] = pd.to_datetime(df['dob'], errors='coerce')
df['joining_date'] = pd.to_datetime(df['joining_date'], errors='coerce')
df['performance_score'] = df['performance_score'].astype('category')

# Step 4: Create New Derived Columns
df['tenure'] = (datetime.now() - df['joining_date']).dt.days / 365

def experience_level(tenure):
    if tenure < 1:
        return "New"
    elif tenure < 5:
        return "Intermediate"
    elif tenure < 10:
        return "Experienced"
    else:
        return "Veteran"

df['experience_level'] = df['tenure'].apply(experience_level)

# Save the cleaned dataset
df.to_csv("cleaned_employees.csv", index=False)

print("Data cleaning and transformation completed successfully.")