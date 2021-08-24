import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.impute import SimpleImputer
from xgboost import XGBRegressor


# For such a small data set boost regression should be fine -> also try random forest
# TODO we might have too little data -> rule of thumb: for each feature at least 10 data points
class tagRegressor:
    def tag_regression(self):
        data_frame = pd.read_csv("id_to_tags.csv")
        # Drop columns where all entries are Nan
        data_frame = data_frame.dropna(axis="columns", how="all")

        x = data_frame.iloc[:, 1:-1].values
        y = data_frame.iloc[:, -1].values.reshape(-1, 1)

        imputer = SimpleImputer(missing_values=np.nan, strategy="constant")
        imputer.fit(x)
        x = imputer.transform(x)
        imputer.fit(y)
        y = imputer.transform(y)

        from sklearn.model_selection import train_test_split
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)

        regressor = XGBRegressor()
        regressor.fit(x_train, y_train)

        score = regressor.score(x_test, y_test)
        print(score)


if __name__ == "__main__":
    tag_regressor = tagRegressor()
    tag_regressor.tag_regression()