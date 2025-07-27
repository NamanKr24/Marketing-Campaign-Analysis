import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OrdinalEncoder, StandardScaler

def preprocessing(df):
    """
    Takes the raw bank marketing dataframe and performs all preprocessing steps.
    Returns X_train, X_test, y_train, y_test, X_train_scaled, X_test_scaled.
    """
    df['y_numeric'] = df['y'].apply(lambda x: 1 if x == 'yes' else 0)

    df_processed = df.drop(columns=['duration'])

    df_processed['was_contacted_previously'] = (df_processed['pdays'] != 999).astype(int)
    df_processed = df_processed.drop(columns=['pdays'])

    education_order = [
        'illiterate', 'basic.4y', 'basic.6y', 'basic.9y',
        'high.school', 'professional.course', 'university.degree', 'unknown'
    ]
    ordinal_encoder = OrdinalEncoder(categories=[education_order])
    df_processed['education'] = ordinal_encoder.fit_transform(df_processed[['education']])

    X = df_processed.drop(columns=['y', 'y_numeric'])
    y = df_processed['y_numeric']
    X_encoded = pd.get_dummies(X, drop_first=True)

    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print("--- Data successfully preprocessed and split ---")
    
    return X_train, X_test, y_train, y_test, X_train_scaled, X_test_scaled