import pandas as pd
from scipy.stats import ttest_ind, chi2_contingency
import matplotlib.pyplot as plt


def t_test(data, group_col, value_col, group_a, group_b):
    """Perform T-test between two groups."""
    group1 = data[data[group_col] == group_a][value_col]
    group2 = data[data[group_col] == group_b][value_col]
    t_stat, p_val = ttest_ind(group1, group2, equal_var=False)
    return t_stat, p_val


def chi_square_test(data, col1, col2):
    """Perform Chi-square test between two categorical columns."""
    contingency_table = pd.crosstab(data[col1], data[col2])
    chi2, p, dof, expected = chi2_contingency(contingency_table)
    return chi2, p


def visualize_boxplot(data, x_col, y_col):
    """Visualize a boxplot."""
    data.boxplot(column=y_col, by=x_col)
    plt.title(f"Boxplot of {y_col} by {x_col}")
    plt.ylabel(y_col)
    plt.xlabel(x_col)
    plt.show()


def main():
    # Example usage
    data = pd.read_csv("../data/data.csv")  # Adjust path as necessary

    # Perform hypothesis tests
    t_stat, p_val = t_test(data, 'Province', 'TotalClaims', 'Province_A', 'Province_B')
    print(f"T-test Results: t_stat={t_stat}, p_val={p_val}")

    chi2, p_val = chi_square_test(data, 'Gender', 'RiskType')
    print(f"Chi-square Test Results: chi2={chi2}, p_val={p_val}")

    # Visualize boxplot
    visualize_boxplot(data, 'Province', 'TotalClaims')


if __name__ == "__main__":
    main()
