import pandas as pd
class DataCleaner:
    def __init__(self, dataframe):
        """
        Initialize the DataCleaner class with a pandas DataFrame.

        Parameters:
            dataframe (pd.DataFrame): The dataset to clean and analyze.
        """
        self.dataframe = dataframe

    def get_overview(self):
        """
        Provides an overview of the dataset, including dimensions and data types.

        Returns:
            dict: A dictionary containing the shape and data types of the dataset.
        """
        return {
            "shape": self.dataframe.shape,
            "data_types": self.dataframe.dtypes.to_dict()
        }

    def summarize_numerical(self):
        """
        Summarizes numerical columns with basic statistics.

        Returns:
            pd.DataFrame: Summary statistics for numerical features.
        """
        return self.dataframe.describe()

    def summarize_categorical(self):
        """
        Summarizes categorical columns with frequency counts.

        Returns:
            dict: Frequency counts for each categorical column.
        """
        categorical_columns = self.dataframe.select_dtypes(include=['object', 'category']).columns
        return {col: self.dataframe[col].value_counts().to_dict() for col in categorical_columns}

    def check_missing_values(self):
        """
        Checks for missing values in the dataset.

        Returns:
            pd.DataFrame: A DataFrame showing count and percentage of missing values for each column.
        """
        missing_counts = self.dataframe.isnull().sum()
        missing_percentages = (missing_counts / len(self.dataframe)) * 100
        missing_df = pd.DataFrame({
            "missing_count": missing_counts,
            "missing_percentage": missing_percentages
        })
        return missing_df[missing_df["missing_count"] > 0]

    def fill_missing_values(self, strategy="mean", columns=None):
        """
        Fills missing values in specified columns using a specified strategy.

        Parameters:
            strategy (str): The strategy to fill missing values ('mean', 'median', 'mode').
            columns (list): List of columns to apply the filling. If None, all columns are considered.

        Returns:
            pd.DataFrame: A DataFrame with missing values filled.
        """
        if columns is None:
            columns = self.dataframe.columns

        for column in columns:
            if self.dataframe[column].isnull().sum() > 0:
                if strategy == "mean" and self.dataframe[column].dtype in ['float64', 'int64']:
                    self.dataframe[column].fillna(self.dataframe[column].mean(), inplace=True)
                elif strategy == "median" and self.dataframe[column].dtype in ['float64', 'int64']:
                    self.dataframe[column].fillna(self.dataframe[column].median(), inplace=True)
                elif strategy == "mode":
                    self.dataframe[column].fillna(self.dataframe[column].mode()[0], inplace=True)

        return self.dataframe

    def handle_datetime(self, datetime_column):
        """
        Converts a column to datetime and extracts features (year, month).

        Parameters:
            datetime_column (str): The column to convert and extract features from.

        Returns:
            pd.DataFrame: A DataFrame with added year and month columns.
        """
        self.dataframe[datetime_column] = pd.to_datetime(self.dataframe[datetime_column], errors='coerce')
        self.dataframe[f"{datetime_column}_year"] = self.dataframe[datetime_column].dt.year
        self.dataframe[f"{datetime_column}_month"] = self.dataframe[datetime_column].dt.month
        return self.dataframe

    def deduplicate(self):
        """
        Removes duplicate rows from the dataset.

        Returns:
            pd.DataFrame: A DataFrame with duplicates removed.
        """
        self.dataframe = self.dataframe.drop_duplicates()
        return self.dataframe

    def drop_columns(self, columns):
        """
        Drops specified columns from the dataset.

        Parameters:
            columns (list): List of column names to drop.

        Returns:
            pd.DataFrame: A DataFrame with the specified columns removed.
        """
        self.dataframe.drop(columns=columns, inplace=True)
        return self.dataframe

    def detect_outliers(self, column):
        """
        Detects outliers in a numerical column using the IQR method.

        Parameters:
            column (str): The column to analyze for outliers.

        Returns:
            dict: Indices of outliers and their corresponding values.
        """
        if column not in self.dataframe.columns or self.dataframe[column].dtype not in ['float64', 'int64']:
            return {}

        Q1 = self.dataframe[column].quantile(0.25)
        Q3 = self.dataframe[column].quantile(0.75)
        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = self.dataframe[(self.dataframe[column] < lower_bound) | (self.dataframe[column] > upper_bound)]
        return outliers[[column]].to_dict(orient="index")
