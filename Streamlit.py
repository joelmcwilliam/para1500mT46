import streamlit as st
import pandas as pd
import numpy as np

# Set page title
st.title('My Streamlit App')

# Add a header
st.header('Welcome to my app!')

# Add some text
st.write('This is a simple Streamlit application.')

# Create a sample dataframe
data = pd.DataFrame({
    'Column 1': np.random.randn(10),
    'Column 2': np.random.randn(10)
})

# Display the dataframe
st.subheader('Sample Data')
st.dataframe(data)

# Add a chart
st.subheader('Line Chart')
st.line_chart(data)

# Add a sidebar
st.sidebar.header('Sidebar')
st.sidebar.write('You can add controls here')

# Add interactive widgets
if st.button('Click me'):
    st.write('Button clicked!')

number = st.slider('Select a number', 0, 100, 50)
st.write(f'Selected number: {number}')

