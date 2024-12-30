import pandas as pd
from scipy.stats import ttest_ind, chi2_contingency
import matplotlib.pyplot as plt

# Load dataset
data = pd.read_csv("../data/data.csv")  # Update path if needed

# Example 1: T-test for numerical data (e.g., TotalClaims by Province)
province_a = data[data['Province'] == 'Province_A']['TotalClaims']
province_b = data[data['Province'] == 'Province_B']['TotalClaims']

# Perform T-test
t_stat, p_val = ttest_ind(province_a, province_b, equal_var=False)
print(f"T-test: t_stat = {t_stat}, p_val = {p_val}")

# Example 2: Chi-square test for categorical data (e.g., Gender and RiskType)
contingency_table = pd.crosstab(data['Gender'], data['RiskType'])
chi2, p, dof, expected = chi2_contingency(contingency_table)
print(f"Chi-square test: chi2 = {chi2}, p_val = {p}")

# Visualization: Boxplot for TotalClaims by Province
data.boxplot(column='TotalClaims', by='Province')
plt.title("Boxplot of Total Claims by Province")
plt.ylabel("Total Claims")
plt.xlabel("Province")
plt.show()
