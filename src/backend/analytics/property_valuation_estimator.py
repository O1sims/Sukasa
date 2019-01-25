import config as cf
import pandas as pd

from sklearn import linear_model
from sukasa.config import REDIS_KEYS
from api.services.RedisService import RedisService


def predict_property_price(property_data):
    property_estimation_model = RedisService().get_skl_model(
        redis_key=REDIS_KEYS['propertyValuationModel'])
    indy_df = RedisService().get_dataframe(
        redis_key=REDIS_KEYS['independentVariables'])
    flat_property_data = pd.io.json.json_normalize(
        data=[property_data])
    indy_df = indy_df.append(flat_property_data)[indy_df.columns.tolist()]
    indy_dummies = pd.get_dummies(indy_df)
    data_len = len(indy_dummies)
    price_prediction = property_estimation_model.predict(
        indy_dummies[data_len-1:data_len])
    return price_prediction[0]


def create_property_estimation_model(property_data):
    property_df = pd.io.json.json_normalize(
        data=property_data)
    complete_df = pd.DataFrame(
        data=property_df,
        columns=cf.INDEPENDENT_VARIABLES + cf.DEPENDENT_VARIABLES).dropna()
    indy_df = pd.DataFrame(
        data=complete_df,
        columns=cf.INDEPENDENT_VARIABLES)
    RedisService().set_dataframe(
        dataframe=indy_df,
        redis_key=REDIS_KEYS['independentVariables'])
    depy_df = pd.DataFrame(
        data=complete_df,
        columns=cf.DEPENDENT_VARIABLES)
    lm = linear_model.LinearRegression()
    property_estimation_model = lm.fit(
        X=pd.get_dummies(indy_df),
        y=depy_df[cf.DEPENDENT_VARIABLES[0]])
    RedisService().set_skl_model(
        model=property_estimation_model,
        redis_key=REDIS_KEYS['propertyValuationModel'])
