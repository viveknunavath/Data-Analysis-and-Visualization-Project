# %%
import pandas as pd
import openpyxl
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


# %% [markdown]
# Load the Data

# %%
file_path = r'C:\Users\lenovo\OneDrive\Desktop\familydata.xlsx'
data = pd.read_excel(file_path, sheet_name='FamilyData')
data.head()

# %% [markdown]
# 1 . DATA ANALYSIS

# %% [markdown]
# Removing Duplicates

# %%
data_cleaned = data.drop_duplicates()
data_cleaned == data
data.head()

# %% [markdown]
# Check missing values

# %%
missing_values = data_cleaned.isnull().sum()
missing_values.head(12)

# %%
data.describe().round(3)

# %% [markdown]
# Family Level Spending Pattern

# %%
family_total_spending = data.groupby('family id')['amount'].sum().sort_values(ascending=False)

#Display result
print('\n Top 5 Families by total spendings')
family_total_spending.head()

# %% [markdown]
# Member Level Spending Pattern

# %%
member_level_spending = data.groupby('member id')['amount'].sum().sort_values(ascending=False)

#Display Results
print('\n Top 5 Members by total Spendings')
member_level_spending.head()
      

# %% [markdown]
# Correlation between Financial Metrics

# %%
print(data.columns)

# %%
data.columns = data.columns.str.strip()  # Removes leading/trailing spaces
data.columns = data.columns.str.lower()  # Converts to lowercase for consistency
data.columns  # Verify the cleaned column names


# %%
financial_data = data[['income', 'monthly expenses', 'savings', 'credit card spending']] #Load relevant Financial metrics
correlation_matrix = financial_data.corr() #Calculate Correlation 
correlation_matrix

# %% [markdown]
# Visualize the correlation matrix as a Heatmap

# %%
plt.figure(figsize=(8, 2))
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Correlation Between Financial Matrics')
plt.show()

# %% [markdown]
# 2 . BUILD A FINANCIAL SCORE MODEL

# %%
#Normalize key metrics

data['savings_to_income_ratio'] = data['savings'] / data['income']
data['expenses_to_income_ratio'] = data['monthly expenses'] / data['income']
data['loan_to_income_ratio'] = data['loan payments'] / data['income']
data['credit_card_to_income_ratio'] = data['credit card spending'] / data['income']
data['discretionary_spending_ratio'] = data['amount'] / data['income']  
data['financial_goals_met_ratio'] = data['financial goals met (%)'] / 100

# Assign weights to each factor

weights = {
    'savings_to_income_ratio': 0.2,
    'expenses_to_income_ratio': 0.2,
    'loan_to_income_ratio': 0.15,
    'credit_card_to_income_ratio': 0.15,
    'discretionary_spending_ratio': 0.2,
    'financial_goals_met_ratio': 0.1
}

# Calculate financial health score

data['financial_health_score'] = (
    data['savings_to_income_ratio'] * weights['savings_to_income_ratio'] +
    (1 - data['expenses_to_income_ratio']) * weights['expenses_to_income_ratio'] +
    (1 - data['loan_to_income_ratio']) * weights['loan_to_income_ratio'] +
    (1 - data['credit_card_to_income_ratio']) * weights['credit_card_to_income_ratio'] +
    (1 - data['discretionary_spending_ratio']) * weights['discretionary_spending_ratio'] +
    data['financial_goals_met_ratio'] * weights['financial_goals_met_ratio']
) * 100  # Scale to 0–100

# Display scores
data[['family id', 'financial_health_score']]


# %% [markdown]
# 3 . INSIGHTS VISUALIZATION

# %% [markdown]
# 3.1 Spending distribution across categories

# %%
plt.figure(figsize=(10, 5))
spending_data = data[['family id', 'category', 'amount']]
plt.title('Spending Distribution Across Categories')
sns.boxplot(x='category', y='amount', data=spending_data, hue='category', palette='husl')
plt.tight_layout()
plt.show()

# %% [markdown]
# 3.2 Family wise financial score.

# %%
#Calculate the financial health score
#formula : financial health score = (savings/income)*100 - (expenses/income)*50 

data['financial_health_score'] = (data['savings'] / data['income']) * 100 - (data['monthly expenses'] / data['income']) * 50

#plot the financial health score
data_subset = data.head(5000)
plt.figure(figsize=(12, 6))
sns.barplot(x='family id', y='financial_health_score', data=data_subset, hue='income', palette='viridis')
plt.title('Family Wise Financial Score')
plt.xlabel('family ID')
plt.ylabel('Financial Health Score')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# %% [markdown]
# 3.3 Member wise spending trends.

# %%
data_subset = data.head(500)
#Create a Lineplot

plt.figure(figsize=(12,6))
sns.lineplot(x='member id', y='amount',hue='category', data=data_subset, marker='o', palette='coolwarm')
plt.title('Member Wise Spending Trends')
plt.xlabel('Member ID')
plt.ylabel('Spending Amount')
plt.legend(title='Spending Category')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


