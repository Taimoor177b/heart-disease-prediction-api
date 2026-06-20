import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib

data = pd.read_csv("heart_disease_uci.csv")
data.drop(['id', 'dataset'], axis=1, inplace=True)

data['trestbps'] = data['trestbps'].fillna(data['trestbps'].median())
data['chol']     = data['chol'].fillna(data['chol'].median())
data['fbs']      = data['fbs'].fillna(data['fbs'].mode()[0])
data['restecg']  = data['restecg'].fillna(data['restecg'].mode()[0])
data['thalch']   = data['thalch'].fillna(data['thalch'].median())
data['exang']    = data['exang'].fillna(data['exang'].mode()[0])
data['oldpeak']  = data['oldpeak'].fillna(data['oldpeak'].median())
data['slope']    = data['slope'].fillna(data['slope'].mode()[0])
data['ca']       = data['ca'].fillna(data['ca'].mean())
data['thal']     = data['thal'].fillna(data['thal'].mode()[0])

data['num'] = (data['num'] > 0).astype(int)


data['sex'] = data['sex'].map({'Male': 1, 'Female': 0})
data['fbs'] = data['fbs'].map({True: 1, False: 0})
data['exang'] = data['exang'].map({True: 1, False: 0})

data = pd.get_dummies(data, columns=['cp', 'thal', 'restecg', 'slope'], drop_first=True)

x = data.drop('num', axis=1)
y = data['num']
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=42)


model = RandomForestClassifier(
    n_estimators=200,
    max_depth=10,
    min_samples_split=5,
    class_weight='balanced',
    random_state=42
)
model.fit(x_train, y_train)

joblib.dump(model,'model.pkl')
joblib.dump(x_train.columns.tolist(),'columns.pkl')

print(f'model trained')


