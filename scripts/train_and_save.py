# This script trains the MLPRegressor on the provided synthetic dataset
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_squared_error, r2_score

df = pd.read_csv('../data/traffic_synthetic.csv')
features = ['hour','day_of_week','is_weekend','is_holiday','temperature','precipitation','wind_speed']
X = df[features].values
y = df['congestion'].values

X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2,random_state=42)
mlp = MLPRegressor(hidden_layer_sizes=(64,32),max_iter=400,random_state=42)
mlp.fit(X_train,y_train)
y_pred = mlp.predict(X_test)
print('MSE:', mean_squared_error(y_test,y_pred))
print('R2:', r2_score(y_test,y_pred))
joblib.dump(mlp, '../model/traffic_mlp.joblib')
print('Model saved to ../model/traffic_mlp.joblib')
