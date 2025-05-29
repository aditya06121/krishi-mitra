import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score

# Load the dataset
try:
    df = pd.read_csv('data_season.csv')
except FileNotFoundError:
    print("Error: 'data_season.csv' not found. Make sure the file is in the same directory.")
    exit()

print("--- Initial Data Overview ---")
print(df.head())
print("\n--- Data Info ---")
df.info()
print("\n--- Descriptive Statistics (Numerical Columns) ---")
print(df.describe())
print("\n--- Missing Values ---")
print(df.isnull().sum())

# --- Feature Selection for this specific analysis ---
# We are interested in 'price' as the target, and 'Location', 'Rainfall', 'Temperature', 'Humidity' as predictors.
features = ['Location', 'Rainfall', 'Temperature', 'Humidity']
target = 'price'

# Create a subset of the DataFrame for this analysis
analysis_df = df[features + [target]].copy()

# --- Exploratory Data Analysis (EDA) ---
print("\n--- EDA ---")

# 1. Distribution of Price
plt.figure(figsize=(10, 6))
sns.histplot(analysis_df['price'], kde=True)
plt.title('Distribution of Crop Price')
plt.xlabel('Price')
plt.ylabel('Frequency')
plt.show()

# It's often helpful to log-transform skewed price data for better visualization/modeling
analysis_df['log_price'] = np.log1p(analysis_df['price']) # log1p for handling zeros if any
plt.figure(figsize=(10, 6))
sns.histplot(analysis_df['log_price'], kde=True)
plt.title('Distribution of Log-Transformed Crop Price')
plt.xlabel('Log(Price)')
plt.ylabel('Frequency')
plt.show()

# 2. Price by Location
plt.figure(figsize=(12, 7))
# Calculate mean price per location for better bar plot interpretation
mean_price_location = analysis_df.groupby('Location')['price'].mean().sort_values(ascending=False)
sns.barplot(x=mean_price_location.index, y=mean_price_location.values)
plt.title('Average Crop Price by Location')
plt.xlabel('Location')
plt.ylabel('Average Price')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# 3. Weather variables vs. Price (Scatter plots)
weather_vars = ['Rainfall', 'Temperature', 'Humidity']
for var in weather_vars:
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=analysis_df[var], y=analysis_df['price'])
    plt.title(f'{var} vs. Price')
    plt.xlabel(var)
    plt.ylabel('Price')
    plt.show()

    plt.figure(figsize=(10, 6))
    sns.scatterplot(x=analysis_df[var], y=analysis_df['log_price']) # Using log_price
    plt.title(f'{var} vs. Log(Price)')
    plt.xlabel(var)
    plt.ylabel('Log(Price)')
    plt.show()

# 4. Correlation Heatmap (numerical features only)
plt.figure(figsize=(8, 6))
numerical_df_for_corr = analysis_df[weather_vars + ['price', 'log_price']]
correlation_matrix = numerical_df_for_corr.corr()
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f")
plt.title('Correlation Heatmap (Weather Variables and Price)')
plt.show()

# --- Data Preprocessing for Model ---
print("\n--- Model Building ---")

# Define features (X) and target (y)
X = analysis_df[features]
y = analysis_df['log_price'] # Using log_price for potentially better model performance

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define preprocessing steps
# One-hot encode 'Location' and scale numerical features
numerical_features = ['Rainfall', 'Temperature', 'Humidity']
categorical_features = ['Location']

preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numerical_features),
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
    ])

# --- Model Building (Linear Regression) ---
# Create a pipeline with preprocessing and the model
model_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                               ('regressor', LinearRegression())])

# Train the model
model_pipeline.fit(X_train, y_train)

# --- Model Evaluation ---
y_pred_train = model_pipeline.predict(X_train)
y_pred_test = model_pipeline.predict(X_test)

# Inverse transform predictions if you want to see them in original scale
# y_pred_test_original_scale = np.expm1(y_pred_test)
# y_test_original_scale = np.expm1(y_test)


print("\n--- Model Evaluation (on log-transformed price) ---")
train_mse = mean_squared_error(y_train, y_pred_train)
test_mse = mean_squared_error(y_test, y_pred_test)
train_r2 = r2_score(y_train, y_pred_train)
test_r2 = r2_score(y_test, y_pred_test)

print(f"Train MSE: {train_mse:.4f}")
print(f"Test MSE: {test_mse:.4f}")
print(f"Train R-squared: {train_r2:.4f}")
print(f"Test R-squared: {test_r2:.4f}")

# --- Interpretation (Simple) ---
# Get feature names after one-hot encoding
feature_names_out = model_pipeline.named_steps['preprocessor'].get_feature_names_out()
coefficients = model_pipeline.named_steps['regressor'].coef_

print("\n--- Model Coefficients (Influence on log_price) ---")
coef_df = pd.DataFrame({'Feature': feature_names_out, 'Coefficient': coefficients})
print(coef_df.sort_values(by='Coefficient', ascending=False))

print("\n--- Analysis Summary ---")
print(f"The R-squared on the test set is {test_r2:.2f}.")
print("This indicates that the model explains approximately {:.0f}% of the variance in the log-transformed crop price using Location, Rainfall, Temperature, and Humidity.".format(test_r2 * 100))
print("A higher R-squared (closer to 1) would mean a better fit.")
print("The coefficients show the estimated change in log_price for a one-unit change in the (scaled) feature, holding other features constant.")
print("For example, a positive coefficient for a location means, on average, that location tends to have higher log_prices compared to the baseline location (after one-hot encoding), considering weather effects.")
print("Similarly, a positive coefficient for Temperature suggests that higher temperatures are associated with higher log_prices, all else being equal.")

print("\n--- Further Considerations ---")
print("- This is a simple linear model. Relationships might be non-linear.")
print("- Interactions between features (e.g., temperature effect varying by location) are not captured.")
print("- Other factors like 'Year', 'Area', 'Soil type', 'Irrigation', 'Crops', and 'Season' likely play a significant role in price and were not included in this specific model as per the request focusing on location and weather.")
print("- Outlier treatment and more advanced feature engineering could improve results.")
print("- The model predicts log_price. For price predictions, remember to inverse transform (np.expm1).")