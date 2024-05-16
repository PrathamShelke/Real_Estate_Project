import streamlit as st
import pandas as pd
import plotly.express as px
import pickle
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Analytics")
st.title(":orange[Gurgaon Property Analytics Page]")

#Visualization 1 for Geo Map Plot

new_df=pd.read_csv("csv_files/data_viz1.csv")
# Group by 'sector' and calculate the mean
group_df = new_df.groupby('sector')[['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']].mean()

st.subheader(':green[Sector Wise Price per Sqft Geomap]')
fig = px.scatter_mapbox(group_df, lat="latitude", lon="longitude", color="price_per_sqft", size='built_up_area',
                  color_continuous_scale=px.colors.cyclical.IceFire, zoom=10,
                  mapbox_style="open-street-map",width=1200,height=700,hover_name=group_df.index)

st.plotly_chart(fig,use_container_width=True)

#Visualisation 2:WordCloud of Facilities

st.subheader(':green[Gurgaon Facilities WordCloud]')

feature_text = pickle.load(open('pkl_files/feature_text.pkl','rb'))
#print(feature_text)

plt.rcParams["font.family"] = "Arial"

wordcloud = WordCloud(width = 800, height = 800,
                      background_color ='white',
                      stopwords = set(['s']),  # Any stopwords you'd like to exclude
                      min_font_size = 10).generate(feature_text)

st.image(wordcloud.to_array(), use_column_width=True)

#Visualization 3: Gurgaon SectorWise Wordcloud Facilties

st.subheader(":green[Gurgaon SectorWise Facilities WordCloud]")

df=pd.read_csv("csv_files/wordcloud_sectorwise.csv")

# Dropdown to select sector
def generate_wordcloud(facilities):
    wordcloud = WordCloud(width=800, height=800, background_color='white', colormap='viridis',min_font_size = 5).generate(facilities)
    st.image(wordcloud.to_array(), use_column_width=True)


selected_sector = st.selectbox("Select Sector", df['sector'].unique())
facilities = df[df['sector'] == selected_sector]['features'].values[0]
#print(facilities)
generate_wordcloud(facilities)

#Visualization4 : Area vs Price Per Sqft
st.subheader(":green[Area Vs Price] ")

df2 = pd.read_csv('csv_files/gurgaon_properties_missing_value_imputation.csv')

property_type = st.selectbox('Select Property Type', ['flat','house'])

if property_type == 'house':
    fig1 = px.scatter(df2[df2['property_type'] == 'house'], x="built_up_area", y="price", color="bedRoom", title="House Area Vs Price")

    st.plotly_chart(fig1, use_container_width=True)
else:
    fig2 = px.scatter(df2[df2['property_type'] == 'flat'], x="built_up_area", y="price", color="bedRoom",
                      title="Flat Area Vs Price")

    st.plotly_chart(fig2, use_container_width=True)

#Visualization 5:PIE CHart of BHK
st.subheader(':green[BHK Pie Chart]')

sector_options = df2['sector'].unique().tolist()
sector_options.insert(0,'overall')

selected_sector = st.selectbox('Select Sector', sector_options)

if selected_sector == 'overall':

    fig3= px.pie(df2, names='bedRoom')

    st.plotly_chart(fig3, use_container_width=True)
else:

    fig4 = px.pie(df2[df2['sector'] == selected_sector], names='bedRoom')

    st.plotly_chart(fig4, use_container_width=True)



#Visualization 6: Side by Side BHK Price Comparison
st.subheader(':green[Side by Side BHK price comparison]')

fig5 = px.box(df2[df2['bedRoom'] <= 4], x='bedRoom', y='price', title='BHK Price Range')

st.plotly_chart(fig5, use_container_width=True)

#Visualization 7:Side by Side Distplot
st.subheader(':green[Side by Side Distplot for property type]')

fig6 = plt.figure(figsize=(10, 4))
sns.distplot(df2[df2['property_type'] == 'house']['price'],label='house')
sns.distplot(df2[df2['property_type'] == 'flat']['price'], label='flat')
plt.legend()
st.pyplot(fig6)

#st.snow()










