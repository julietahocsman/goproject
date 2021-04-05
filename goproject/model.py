import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import RobustScaler
from goproject.grid_coord import grid_coordinates


# def coordinates_data():
#     data = pd.read_csv('coordinates_data.csv')
#     data['columnx'] = data["new_x"].map(data_x)
#     data['columny'] = data["new_y"].map(data_y)
#     data['tuple_xy'] = list(zip(data.columnx, data.columny))

#     '''Dropping outliers'''
#     data = data[data.columny >= 0]
#     data = data[data.columny <= 39] #nunique de de grid_coordinates_gdf.new_y
#     data = data[data.columnx >= 0]
#     data = data[data.columnx <= 80]
#     data['arrive'] = pd.to_datetime(data['arrive'])
#     data['leave'] = pd.to_datetime(data['leave'])
#     data["year"] = data["arrive"].dt.year
#     data["month"] = data["arrive"].dt.month
#     data["day"] = data["arrive"].dt.day
#     data["hour"] = data["arrive"].dt.hour
#     data["min"] = data["arrive"].dt.minute
#     data["weekday"] = data["arrive"].dt.weekday

#     return data

# def scale_data(data):
#     data_features = data[['search_longitude', 'search_latitude', 'weekday', 'hour']]

#     r_scaler = RobustScaler() # Instanciate Robust Scaler

#     r_scaler.fit(data_features[['weekday']]) # Fit scaler to feature
#     r_scaler.fit(data_features[['hour']]) # Fit scaler to feature

#     data_features['weekday'] = r_scaler.transform(data_features[['weekday']]) #Scale
#     data_features['hour'] = r_scaler.transform(data_features[['hour']]) #Scale

#     return data_features

# def run_model(data_features):
#     X = data_features[['weekday', 'hour']]
#     y = data_features[['search_longitude', 'search_latitude']]
#     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

#     forest = MultiOutputRegressor(RandomForestRegressor(n_estimators=3, random_state=1))

#     forest = forest.fit(X_train, y_train)

#     y_train_pred = forest.predict(X_train)
#     y_test_pred = forest.predict(X_test)

