# import all required libraries
import os
import streamlit as st
from langchain_google_genai import GoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Set Page Configuration 
st.set_page_config(page_title="AI Travel Planner",layout="wide") 

# CSS For Better UI
st.markdown("""
            <style>
                body{
                    background-color:#f5f5f5;
                    font-family:'Ariel',sans-serif;
                }
                .main_heading{
                    color: green;
                    text-align:centre;
                    font-size:50px !important;
                    font-weight:bold;
                }
                .subtext{
                    color:#585;
                    text-align-centre;
                    font-size:20px;
                }
                .stButton>button{
                    background-color:#0077b6 !important;
                    color:white !important;
                    font-size:16px;
                    border-radius:10px;
                }
            
            </style>""",
unsafe_allow_html=True)

#display title
st.markdown("<p class='main_heading'> ✈ AI Powered Travel Planner </p>",unsafe_allow_html=True)
st.markdown("<p class='subtext' Get optimized travel options with cost-effective recommendations!",unsafe_allow_html=True)
st.markdown("---")

#sidebar for inputs
with st.sidebar:
    st.header("Travel Options")
    source=st.text_input("Enter source location",placeholder="Ex-Delhi")
    destination=st.text_input("Enter Destination location",placeholder="Ex-Meerut")
    search_button=st.button("🔍 Find Travel options")

# Fetch API Key
api_key=os.getenv("GOOGLE_API_KEY")

# define langchain model
model=GoogleGenerativeAI(model="gemini-1.5-pro",google_api_key=api_key)

#Define Prompt Template
prompt_template=ChatPromptTemplate.from_messages(messages=[("system","""You are an AI-powered travel assistant that provides users with the best travel options based on their preferences.
    Given a source and destination, you must provide the distance to be traveled and generate a structured travel plan with multiple options (cab, train, bus, flights).
    Each option should include the estimated cost, travel time, and any relevant details like stops or transfers.
    Prioritize accuracy, cost-effectiveness, and convenience while presenting the results in a clear, easy-to-read format."""),

    ("human", "Find travel options from {source} to {destination} with optimized costs.")
])

#Function to fetch travel recommendation
def get_travel(source,destination):
    user_input=prompt_template.format(source=source,destination=destination)
    response=model.invoke(user_input)
    return response

#display result
if search_button:
    if source and destination:
        with st.spinner("🔄 Fetching Best Travel options"):
            recommendation=get_travel(source,destination)
        st.success("✅ Travel Plan Generated")

        #Travel Summary section
        st.subheader("Travel Summary")
        st.write(f" **From:** {source} ➡ **To** {destination}")
        st.write(" Estimated Distance: ~ To be fetched by API (Google Maps or another source)")
        st.write("---")
        
        #Display Travel Option
        st.subheader("🚗🚆✈ Recommended Travel Options")
        st.write(recommendation)
    else:
         st.warning("⚠ Please enter both source and destination!")
