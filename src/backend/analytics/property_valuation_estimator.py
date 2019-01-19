import pandas as pd

from sklearn import linear_model
from utils.pickler import load_data_pickle, save_data_pickle


DEPENDENT_VARIABLES = [
    'priceInfo.price'
]

INDEPENDENT_VARIABLES = [
    'postcode',
    'details.bedrooms',
    'details.style',
    'details.heating',
    'details.amenities.bayWindow',
    'details.amenities.driveway',
    'details.amenities.garage',
    'details.amenities.garden'
]


def predict_property_price(property_data):
    property_estimation_model = load_data_pickle(
        file_name='property_estimation_model')
    indy_df = load_data_pickle(
        file_name='independent_variables_df')
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
        columns=INDEPENDENT_VARIABLES + DEPENDENT_VARIABLES).dropna()
    indy_df = pd.DataFrame(
        data=complete_df,
        columns=INDEPENDENT_VARIABLES)
    save_data_pickle(
        data=indy_df,
        file_name='independent_variables_df')
    depy_df = pd.DataFrame(
        data=complete_df,
        columns=DEPENDENT_VARIABLES)
    lm = linear_model.LinearRegression()
    property_estimation_model = lm.fit(
        X=pd.get_dummies(indy_df),
        y=depy_df[DEPENDENT_VARIABLES[0]])
    save_data_pickle(
        data=property_estimation_model,
        file_name='property_estimation_model')
