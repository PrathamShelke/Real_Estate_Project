import streamlit as st
import pickle
import pandas as pd
st.set_page_config(page_title="Recommend Apartments")
st.title(":orange[Gurgaon Apartments Recommender ]")

location_df = pickle.load(open('pkl_files/location_distance.pkl','rb'))

#Level 1 :Recommend Apartments/Property Name according to  Location and Radius entered by user
st.subheader(':red[Select Location and Radius]')

selected_location = st.selectbox(':green[Location]',sorted(location_df.columns.to_list()))
radius = st.number_input(':green[Radius in Kms]')

if st.button(':blue[Search]'):
    st.subheader(":red[Nearest Apartment Names:]")
    df = pd.read_csv("csv_files/apartments_links.csv")

    result_ser = location_df[location_df[selected_location] < radius * 1000][selected_location].sort_values()
    if not result_ser.empty:
        recommended_apartments = result_ser.index.tolist()
        apartment_data = []
        for apartment_name in recommended_apartments:
            link = df.loc[df['PropertyName'] == apartment_name, 'Link'].values
            if len(link) > 0:
                apartment_data.append([apartment_name, round(result_ser[apartment_name] / 1000), link[0]])
            else:
                apartment_data.append([apartment_name, round(result_ser[apartment_name] / 1000), "Link not found"])

        recommendations_df = pd.DataFrame(apartment_data, columns=['Apartment Name', 'Distance (kms)', 'Link'])
        st.dataframe(recommendations_df)
        st.success("Apartments Recommendation Successful")
        #st.balloons()
    else:
        st.error("No locations found within the specified radius.")

#Level 2:Recommend Top 5 similar Apartments
st.subheader(':red[Recommend Appartments]')

cosine_sim1 = pickle.load(open('pkl_files/cosine_sim1.pkl','rb'))
cosine_sim2 = pickle.load(open('pkl_files/cosine_sim2.pkl','rb'))
cosine_sim3 = pickle.load(open('pkl_files/cosine_sim3.pkl','rb'))


def recommend_properties_with_scores(property_name, top_n=5):
    cosine_sim_matrix = 0.5 * cosine_sim1 + 0.8 * cosine_sim2 + 1 * cosine_sim3
    # cosine_sim_matrix = cosine_sim3

    # Get the similarity scores for the property using its name as the index
    sim_scores = list(enumerate(cosine_sim_matrix[location_df.index.get_loc(property_name)]))

    # Sort properties based on the similarity scores
    sorted_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Get the indices and scores of the top_n most similar properties
    top_indices = [i[0] for i in sorted_scores[1:top_n + 1]]
    top_scores = [i[1] for i in sorted_scores[1:top_n + 1]]

    # Retrieve the names of the top properties using the indices
    top_properties = location_df.index[top_indices].tolist()

    # Fetch corresponding links from df DataFrame
    df1=pd.read_csv("csv_files/apartments_links.csv")
    # Fetch corresponding links from df DataFrame
    property_links = []
    for prop in top_properties:
        link = df1.loc[df1['PropertyName'] == prop, 'Link'].values
        if len(link) > 0:
            property_links.append(link[0])
        else:
            property_links.append("Link not found")

    # Create a dataframe with the results
    recommendations_df = pd.DataFrame({
        'PropertyName': top_properties,
        'SimilarityScore': top_scores,
        'Link': property_links
    })

    return recommendations_df

selected_appartment = st.selectbox(':green[Select an appartment]',sorted(location_df.index.to_list()))

if st.button(':blue[Recommend]'):
    recommendation_df = recommend_properties_with_scores(selected_appartment)

    st.dataframe(recommendation_df)
    st.success("Apartments Recommendation Successful")
    #st.snow()

