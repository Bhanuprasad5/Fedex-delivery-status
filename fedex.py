import streamlit as st
import pandas as pd
import pickle
from PIL import Image

# Load the pre-trained model
model = pickle.load(open("Fedex.pkl", 'rb'))

# Set the title and subtitle
st.title("FedEx Delivery Status Prediction")
st.image(r"573326-innomatics_research_labs_logo.png", width=200)
# Display FedEx logo/image
image = Image.open(r"fedex.png")
st.image(image, use_column_width=True)

st.subheader("Predict the status of your FedEx delivery with ease")

# Add a sidebar for inputs
st.sidebar.header("Input Shipment Details")
st.sidebar.write("Fill in the following details to predict the delivery status")

# Define features
numerical_features = ['Carrier_Num', 'Distance']
categorical_features = {
    'Year': [2008],
    'Month': list(range(1, 13)),  # Updated for all months
    'DayofMonth': list(range(1, 32)),
    'DayOfWeek': list(range(1, 8)),
    'Carrier_Name': ['WN', 'XE', 'YV', 'OH', 'OO', 'UA', 'US', 'DL', 'EV', 'F9', 'FL',
                     'HA', 'MQ', 'NW', '9E', 'AA', 'AQ', 'AS', 'B6', 'CO']
}
categories = ['Source', 'Destination']

# Collect user inputs
input_data = {}
for feature in numerical_features:
    input_data[feature] = st.sidebar.number_input(f'Enter value for {feature}', min_value=0.0)

for feature, options in categorical_features.items():
    input_data[feature] = st.sidebar.selectbox(f'Select {feature}', options)

for feature in categories:
    input_data[feature] = st.sidebar.text_input(f"Enter {feature}")

# Time inputs
st.sidebar.write("Enter Times (in HH:MM format)")

# Function to get time in minutes
def get_time_in_minutes(label):
    hours = st.sidebar.selectbox(f"{label} Hours", list(range(0, 24)), key=label+"h")
    minutes = st.sidebar.selectbox(f"{label} Minutes", list(range(0, 60)), key=label+"m")
    return hours * 60 + minutes

# Input times
input_data['Actual_Shipment_Time'] = get_time_in_minutes("Actual Shipment Time")
input_data['Planned_Shipment_Time'] = get_time_in_minutes("Planned Shipment Time")
input_data['Planned_Delivery_Time'] = get_time_in_minutes("Planned Delivery Time")
input_data['Planned_TimeofTravel'] = get_time_in_minutes("Planned Time of Travel")
input_data['Shipment_Delay'] = get_time_in_minutes("Shipment Delay Time")

# Convert input data to DataFrame
input_df = pd.DataFrame([input_data])

# Debug: Display the input DataFrame
st.write("### Input DataFrame for Debugging", input_df)

# Display prediction
if st.button('Predict Delivery Status'):
    try:
        prediction = model.predict(input_df)
        if int(prediction[0]) == 1:
            st.success("Your delivery is predicted to be ON TIME!")
            st.image("delivered.jpeg", width=400, caption="Your delivery is on time! 🚀")
        else:
            st.warning("Your delivery is predicted to be DELAYED!")
            st.image("not.jpeg", width=400, caption="Your delivery is delayed. 😞")
    except ValueError as e:
        st.error(f"Prediction failed: {str(e)}")

