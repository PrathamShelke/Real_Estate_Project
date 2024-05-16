import streamlit as st
import pickle
import pandas as pd
import numpy as np

st.set_page_config(page_title="Property Price Prediction")
st.title(":orange[Gurgaon Property Price Prediction]")



with open('pkl_files/df.pkl','rb') as file:
    df = pickle.load(file)

with open('pkl_files/pipeline.pkl','rb') as file:
    pipeline = pickle.load(file)


st.subheader(':red[Enter your inputs]')

# property_type
property_type = st.selectbox(':green[Property Type]',['flat','house'])

# sector
sector = st.selectbox(':green[Sector]',sorted(df['sector'].unique().tolist()))

bedrooms = float(st.selectbox(':green[Number of Bedroom]',sorted(df['bedRoom'].unique().tolist())))

bathroom = float(st.selectbox(':green[Number of Bathrooms]',sorted(df['bathroom'].unique().tolist())))

balcony = st.selectbox(':green[Balconies]',sorted(df['balcony'].unique().tolist()))

property_age = st.selectbox(':green[Property Age]',sorted(df['agePossession'].unique().tolist()))

built_up_area = float(st.number_input(':green[Built Up Area(Sqft)]'))

servant_room = float(st.selectbox(':green[Servant Room]',[0.0, 1.0]))
store_room = float(st.selectbox(':green[Store Room]',[0.0, 1.0]))

furnishing_type = st.selectbox(':green[Furnishing Type]',sorted(df['furnishing_type'].unique().tolist()))
luxury_category = st.selectbox(':green[Luxury Category]',sorted(df['luxury_category'].unique().tolist()))
floor_category = st.selectbox(':green[Floor Category]',sorted(df['floor_category'].unique().tolist()))

if st.button(':blue[Predict]'):
    with st.status("Prediction in Progress"):

        # form a dataframe
        data = [[property_type, sector, bedrooms, bathroom, balcony, property_age, built_up_area, servant_room, store_room, furnishing_type, luxury_category, floor_category]]
        columns = ['property_type', 'sector', 'bedRoom', 'bathroom', 'balcony',
                   'agePossession', 'built_up_area', 'servant room', 'store room',
                   'furnishing_type', 'luxury_category', 'floor_category']

        # Convert to DataFrame
        one_df = pd.DataFrame(data, columns=columns)

        #st.dataframe(one_df)

        # predict(We have given range because our model error is around 45 lakhs so we divided the error)
        base_price = np.expm1(pipeline.predict(one_df))[0]
        low = base_price - 0.22
        high = base_price + 0.22

        # display
        st.text("The price of the flat is between {} Cr and {} Cr".format(round(low,2),round(high,2)))
        st.success("Prediction Successful")

