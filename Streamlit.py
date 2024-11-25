import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Set page title
st.title('Paralympic 1500m T46 Results')

# Add a header
st.header('Results for Selected Athlete')

# Load data from CSV
data = pd.read_csv(https://raw.githubusercontent.com/joelmcwilliam/para1500mT46/refs/heads/main/paralympic_t46_results.csv)

# Create athlete multi-selection box with NPC, sorted by NPC
athlete_options = [f"{row['NPC']} - {row['ATHLETE']}" for _, row in data[['NPC', 'ATHLETE']].drop_duplicates().sort_values('NPC').iterrows()]
athlete_selections = st.multiselect('Select Athletes:', options=athlete_options)

# Create round filter checkboxes
st.sidebar.write("Filter Rounds:")
rounds = data['ROUND'].unique()
selected_rounds = {}
for round_type in rounds:
    selected_rounds[round_type] = st.sidebar.checkbox(round_type, value=True)

# Filter data based on selected athletes and rounds
filtered_data = pd.DataFrame()
if athlete_selections:  # Only process if athletes are selected
    for selection in athlete_selections:
        selected_athlete = selection.split(' - ')[1]
        athlete_data = data[data['ATHLETE'] == selected_athlete]
        filtered_data = pd.concat([filtered_data, athlete_data])

    # Only apply round filtering if we have data
    if not filtered_data.empty:
        filtered_data = filtered_data[filtered_data['ROUND'].isin([round_type for round_type, selected in selected_rounds.items() if selected])]

# Add dropdown for detailed results above the graph
if athlete_selections:
    with st.expander("View Detailed Results"):
        athlete_for_details = st.selectbox(
            'Select athlete to view detailed results:',
            options=[''] + athlete_selections
        )
        
        if athlete_for_details:
            selected_athlete = athlete_for_details.split(' - ')[1]
            athlete_data = filtered_data[filtered_data['ATHLETE'] == selected_athlete]
            if not athlete_data.empty:
                display_df = athlete_data[['ROUND', 'TIME', 'RANK', 'PARALYMPICS']].copy()
                display_df['RANK'] = display_df['RANK'].astype(int)
                st.dataframe(display_df, hide_index=True)

# Create the graph below (full width)
if not filtered_data.empty:
    # Convert YEAR to datetime year format
    filtered_data['YEAR'] = pd.to_datetime(filtered_data['YEAR'], format='%Y').dt.year
    # Sort by year to ensure correct ordering
    filtered_data = filtered_data.sort_values('YEAR')
    
    # Create Plotly chart with color differentiation by ATHLETE and line style by ROUND
    fig = px.line(
        filtered_data, 
        x='YEAR', 
        y='TIME_SECONDS',
        color='ATHLETE',
        line_dash='ROUND',
        title='Finishing Times across Paralympics',
        markers=True
    )
    
    # Update layout to format x-axis and ensure good color contrast
    fig.update_layout(
        xaxis=dict(
            tickformat='d',
            dtick=4
        ),
        showlegend=True
    )
    
    st.plotly_chart(fig, use_container_width=True)
else:
    st.write('No data available for selected athletes')
