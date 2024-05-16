import streamlit as st
import pandas as pd
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from pandasai import SmartDataframe, SmartDatalake
import os
from langchain_experimental.agents.agent_toolkits import create_csv_agent
import time
# Loading environment variables from .env file
load_dotenv()

st.set_page_config(
    page_title="Chatbot",
    page_icon="👋",
)

st.header(":orange[Gurgaon Real Estate Q and A]")

def chat_with_csv(dataframe, query):
    # Function to initialize conversation chain with GROQ language model
    groq_api_key = os.getenv('GROQ_API_KEY')

    # Initializing GROQ chat with provided API key, model name, and settings
    llm = ChatGroq(
        groq_api_key=groq_api_key, model_name="llama3-70b-8192",
        temperature=0.2)

    # Initialize SmartDataframe with DataFrame and LLM configuration
    #pandas_ai = SmartDataframe(dataframe,config={"llm": llm})
    # Chat with the DataFrame using the provided query
    #result = pandas_ai.chat(query)

    agent_executer = create_csv_agent(llm, dataframe, verbose=True)
    result=agent_executer.invoke(query)
    return result['output']

# Function to load CSV file and display its preview
def load_csv_and_preview(file_name):
    # Load CSV file
    df = pd.read_csv(file_name)

    st.subheader(f"Preview of Selected Dataframe")
    st.write(df.head())
    st.info("CSV uploaded successfully")

    return df

# Display file selection and preview
selected_file = st.selectbox("Select CSV files for Q&A", [
    "apartments_links.csv",
    "gurgaon_properties_cleaned_v2.csv",
    "residential-land.csv",
    "latlong.csv"
])

# Load selected CSV files and display preview
file_path = os.path.join("csv_files", selected_file)
df = load_csv_and_preview(file_path)
input_text = st.text_area("Enter the query")

# Perform analysis\
if st.button("Chat with CSV"):
    if input_text:
        #st.info("Your Query: "+ input_text)
        def response():
            result = chat_with_csv(file_path, input_text)
            for word in result.split(" "):
                yield word + " "
                time.sleep(0.2)
        #if st.button("Chat with CSV"):
        st.write_stream(response)

