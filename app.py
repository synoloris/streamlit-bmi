import streamlit as st
import pandas as pd
import plotly.express as px
import os


# Set page config
st.set_page_config(
    page_title="Body Mass Index Dashboard - by vonlalor",
    page_icon=":chart_with_upwards_trend:",
)


# Function to download dataset from GitHub
@st.cache_data()
def download_dataset():
    import requests

    # URL des GitHub-Rohdaten-Links zum Dataset
    dataset_url = "https://raw.githubusercontent.com/synoloris/bmi-dataset/main/500_Person_Gender_Height_Weight_Index.csv"

    try:
        # HTTP-Anfrage senden, um das Dataset herunterzuladen
        response = requests.get(dataset_url)
        response.raise_for_status()  # Prüfen, ob die Anfrage erfolgreich war

        # Speichern des heruntergeladenen Datasets in einer lokalen CSV-Datei
        with open("500_Person_Gender_Height_Weight_Index.csv", "wb") as f:
            f.write(response.content)

        return True  # Rückgabe, dass das Dataset erfolgreich heruntergeladen wurde

    except Exception as e:
        st.error(f"Error downloading dataset: {e}")
        return (
            False  # Rückgabe, dass das Dataset nicht erfolgreich heruntergeladen wurde
        )


# Streamlit app interface
st.title("Body Mass Index Dashboard - by vonlalor")

# Check if data has been loaded
if "data_loaded" not in st.session_state:
    st.session_state["data_loaded"] = False

# Button to download data
if not st.session_state["data_loaded"]:
    if st.button("Download Dataset", key="download_button"):
        if download_dataset():
            st.session_state["data_loaded"] = True
else:
    st.write("Dataset has been downloaded.")

# Check if data has been loaded before displaying further content
if not st.session_state["data_loaded"]:
    st.markdown("To begin, click the 'Download Dataset' button.")
    st.stop()

# Load the dataset
data = pd.read_csv("500_Person_Gender_Height_Weight_Index.csv")

# Calculate Body Mass Index (BMI)
data["BMI"] = data["Weight"] / ((data["Height"] / 100) ** 2)

# Define overweight as BMI > 25
overweight_data = data[data["BMI"] > 25]

# Pie chart showing the distribution of overweight individuals by gender
gender_distribution = overweight_data["Gender"].value_counts().reset_index()
gender_distribution.columns = ["Gender", "Count"]
# Display the number of overweight individuals
st.subheader("Number of Overweight Individuals")
st.write(f"There are {len(overweight_data)} overweight individuals in the dataset.")

# Sidebar for customizing the Pie Chart
st.sidebar.subheader("Customize Pie Chart")

# Input fields for customizing the Pie Chart
title = st.sidebar.text_input(
    "Title", "Distribution of Overweight Individuals by Gender"
)
title_font_size = st.sidebar.slider("Title Font Size", 10, 30, 20)
label_font_size = st.sidebar.slider("Label Font Size", 10, 20, 14)
color = st.sidebar.color_picker("Color", "#1f77b4")  # Default color: blue

# Create Pie Chart based on customized inputs
fig = px.pie(
    gender_distribution,
    values="Count",
    names="Gender",
    title=title,
    color_discrete_sequence=[color],
)
fig.update_layout(
    title_font=dict(size=title_font_size),
    font=dict(size=label_font_size),
)
st.plotly_chart(fig, use_container_width=True)
