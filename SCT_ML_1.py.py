import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

# Load data
train = pd.read_csv("train.csv")
test = pd.read_csv("test.csv")

# Save test IDs for submission
test_ids = test['Id']

# Drop columns (but keep 'Id' in test data)
drop_cols = [
    "Alley", "PoolQC", "Fence", "MiscFeature", 
    "MiscVal", "MoSold", "YrSold", "Condition2", "MasVnrType"
]
train = train.drop(columns=drop_cols, errors="ignore")
test = test.drop(columns=drop_cols, errors="ignore")

# Handle missing values
def handle_missing(df, train_df=None):
    # For categoricals
    fill_none = ['FireplaceQu', 'GarageType', 'GarageFinish', 
                'BsmtFinType2', 'BsmtExposure', 'BsmtFinType1']
    for col in fill_none:
        df[col].fillna('None', inplace=True)
    
    fill_TA = ['GarageCond', 'GarageQual', 'BsmtQual', 'BsmtCond']
    for col in fill_TA:
        df[col].fillna('TA', inplace=True)
    
    # For numericals
    if train_df is not None:  # For test data
        df['LotFrontage'].fillna(train_df['LotFrontage'].median(), inplace=True)
        df['GarageYrBlt'].fillna(train_df['GarageYrBlt'].median(), inplace=True)
    else:  # For train data
        df['LotFrontage'].fillna(df.groupby('Neighborhood')['LotFrontage'].transform('median'), inplace=True)
        df['GarageYrBlt'].fillna(df['GarageYrBlt'].median(), inplace=True)
    
    df['MasVnrArea'].fillna(0, inplace=True)
    if 'Electrical' in df.columns:
        df['Electrical'].fillna(df['Electrical'].mode()[0], inplace=True)
    
    return df

train = handle_missing(train)
test = handle_missing(test, train)

# Separate features and target
X_train = train.drop(["SalePrice", "Id"], axis=1)  # Drop Id from training features
y_train = train["SalePrice"]
X_test = test.drop("Id", axis=1)  # Drop Id from test features (but we saved it earlier)

# Identify column types
numeric_cols = X_train.select_dtypes(include=['int64', 'float64']).columns
categorical_cols = X_train.select_dtypes(include=['object']).columns

# Preprocessing pipeline
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_cols),
        ('cat', categorical_transformer, categorical_cols)
    ])

# Full pipeline with model
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())
])

# Train model
model.fit(X_train, y_train)

# Make predictions
predictions = model.predict(X_test)

# Create submission file
submission = pd.DataFrame({
    'Id': test_ids,
    'SalePrice': predictions
})
submission.to_csv('submission.csv', index=False)

print("Submission file created successfully!")
print(submission.head(20))  # Show first 20 predictions