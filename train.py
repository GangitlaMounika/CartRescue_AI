import pandas as pd
import joblib

from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, classification_report
from xgboost import XGBClassifier

# ======================
# LOAD DATA
# ======================

sessions = pd.read_csv('data/sessions.csv')
events = pd.read_csv('data/events.csv')

print('Data loaded')

# ======================
# CREATE TARGET LABEL
# ======================

purchase_sessions = set(
    events[events['event_type'].isin(['purchase', 'payment_success'])]['session_id'].unique()
)

sessions['purchased'] = sessions['session_id'].apply(
    lambda x: 1 if x in purchase_sessions else 0
)

print('Purchased sessions:', sessions['purchased'].sum())

# ======================
# FEATURE ENGINEERING
# ======================

features_df = events.groupby('session_id').agg(
    total_events=('event_type', 'count'),
    product_views=('event_type', lambda x: (x == 'view').sum()),
    add_to_cart=('event_type', lambda x: (x == 'add_to_cart').sum()),
    remove_from_cart=('event_type', lambda x: (x == 'remove_from_cart').sum()),
    checkout_events=('event_type', lambda x: (x == 'checkout').sum()),
    payment_attempts=('payment', lambda x: x.notna().sum()),
    avg_cart_size=('cart_size', 'mean'),
    max_cart_size=('cart_size', 'max'),
    avg_discount=('discount_pct', 'mean')
).reset_index()

features_df = features_df.fillna(0)

# ======================
# MERGE
# ======================

data = sessions.merge(features_df, on='session_id', how='left')
data = data.fillna(0)

print('Final dataset shape:', data.shape)

# ======================
# SELECT FEATURES
# ======================

feature_cols = [
    'total_events',
    'product_views',
    'add_to_cart',
    'remove_from_cart',
    #'checkout_events',
    #'payment_attempts',
    'avg_cart_size',
    'max_cart_size',
    'avg_discount'
]

X = data[feature_cols]
y = data['purchased']

# ======================
# TRAIN / TEST SPLIT
# ======================

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ======================
# TRAIN MODEL
# ======================

model = XGBClassifier(
    n_estimators=250,
    max_depth=6,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    eval_metric='logloss',
    random_state=42
)

model.fit(X_train, y_train)

# ======================
# EVALUATE
# ======================

probs = model.predict_proba(X_test)[:, 1]
preds = (probs > 0.5).astype(int)

auc = roc_auc_score(y_test, probs)

print('\\n===== RESULTS =====')
print('AUC:', round(auc, 4))

print('\\nClassification Report:')
print(classification_report(y_test, preds))

# ======================
# SAVE MODEL
# ======================

joblib.dump(model, 'model/risk_model.pkl')
joblib.dump(feature_cols, 'model/features.pkl')

print('\\nModel saved successfully!')