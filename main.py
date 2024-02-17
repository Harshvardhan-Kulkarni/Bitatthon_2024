import streamlit as st
import pandas as pd
from webcolors import name_to_rgb

# Load your dataset
df = pd.read_excel('Sheet 1.xlsx')

# Create Streamlit interface
st.title('Filter Data by Status, Lifetime Value, Account Age, Credit Class, and RFM Score')

# Add a sidebar for page navigation
selected_page = st.sidebar.selectbox('Select Page', ['Page 1', 'Page 2', 'Page 3'])


# Add content for each page
if selected_page == 'Page 1':
    st.sidebar.write("You are on Page 1")
    # Filter by status
    status = st.selectbox('Select Status', ['Active', 'Inactive'])

    # Filter by lifetime value range
    lifetime_value_range = st.slider('Select Lifetime Value Range', -7000, 65000, (-7000, 65000))

    # Filter by account age in years
    acct_age_options = ['All', 'Less than 5 years', 'Between 5 and 10 years', 'Greater than 10 years']
    selected_acct_age = st.selectbox('Select Account Age', acct_age_options)

    # Filter by credit class using Checkboxes
    credit_class_options = ['Prime', 'Other', 'Near Prime', 'Risky', 'Smax Prime']
    selected_credit_classes = [st.checkbox(credit_class.lower(), key=credit_class) for credit_class in credit_class_options]

    # Filter by RFM score using Text Input
    rfm_score_threshold = st.text_input('Enter Minimum RFM Score', 150)

    # Add a button to reset all filters
    if st.button('Reset Filters'):
        status = 'Active'
        lifetime_value_range = (-7000, 65000)
        selected_acct_age = 'All'
        selected_credit_classes = [False] * len(credit_class_options)
        rfm_score_threshold = '150'

    # Convert the 'churn' column to boolean (0 -> False, 1 -> True)
    df['churn'] = df['churn'].astype(bool)

    # Apply filters
    filtered_df = df.copy()

    # Filter by status
    if status == 'Inactive':
        filtered_df = filtered_df[~filtered_df['churn']]

    # Filter by lifetime value range
    filtered_df = filtered_df[(filtered_df['lifetime_value'] >= lifetime_value_range[0]) & (filtered_df['lifetime_value'] <= lifetime_value_range[1])]

    # Filter by account age
    if selected_acct_age == 'Less than 5 years':
        filtered_df = filtered_df[filtered_df['acct_age'] < 5 * 12]
    elif selected_acct_age == 'Between 5 and 10 years':
        filtered_df = filtered_df[(filtered_df['acct_age'] >= 5 * 12) & (filtered_df['acct_age'] <= 10 * 12)]
    elif selected_acct_age == 'Greater than 10 years':
        filtered_df = filtered_df[filtered_df['acct_age'] > 10 * 12]

    # Filter by credit class
    selected_credit_classes = [credit_class.lower() for credit_class, selected in zip(credit_class_options, selected_credit_classes) if selected]
    if selected_credit_classes:
        filtered_df = filtered_df[filtered_df['credit_class'].str.lower().isin(selected_credit_classes)]

    # Filter by RFM score
    try:
        rfm_score_threshold = int(rfm_score_threshold)
        filtered_df = filtered_df[filtered_df['rfm_score'] >= rfm_score_threshold]
    except ValueError:
        st.warning("Please enter a valid integer for RFM Score.")

    # Display the count of filtered rows
    st.markdown(f"### Filtered Rows Count: {filtered_df.shape[0]}")

    # Display filtered data
    st.write(filtered_df)

    # Add specific content for Page 1 if needed
elif selected_page == 'Page 2':
    st.sidebar.write("You are on Page 2")

# Read the CSV files into DataFrames
    df1 = pd.read_excel('Sheet 1.xlsx')
    df2 = pd.read_excel('CallCentre Data.xlsx')

    # Create Streamlit interface
    st.title('Display Information based on Column 1 Input')

    # User input through a dropdown based on unique values in Column 1 of dataset 1
    user_input = st.selectbox('Enter a value from Column 1 of dataset 1', df1['hh'].unique())

    # Validate if the input is present in Column 1 of dataset 1
    if user_input in df1['hh'].values:
        # Filter rows of Dataset 1 based on user input
        filtered_df1 = df1[df1['hh'] == user_input]

        # Display all columns of the filtered row in an interactive manner
        st.write("### Information from Dataset 1:")
        with st.expander("Household Information"):
            st.write(f"*Household (hh):* {filtered_df1['hh'].values[0]}")

        with st.expander("Churn Information"):
            st.write(f"*Churn:* {filtered_df1['churn'].values[0]}")

        with st.expander("Lifetime Value Information"):
            st.write(f"*Lifetime Value:* {filtered_df1['lifetime_value'].values[0]}")

        with st.expander("Average ARPU (3 months) Information"):
            st.write(f"*Average ARPU (3 months):* {filtered_df1['avg_arpu_3m'].values[0]}")

        with st.expander("Account Age Information"):
            st.write(f"*Account Age:* {filtered_df1['acct_age'].values[0]}")

        with st.expander("Billing Cycle Information"):
            st.write(f"*Billing Cycle:* {filtered_df1['billing_cycle'].values[0]}")

        with st.expander("Number of Contracts Ltd Information"):
            st.write(f"*Number of Contracts Ltd:* {filtered_df1['nbr_contracts_ltd'].values[0]}")

        with st.expander("Credit Class Information"):
            st.write(f"*Credit Class:* {filtered_df1['credit_class'].values[0]}")

        with st.expander("Sales Channel Information"):
            st.write(f"*Sales Channel:* {filtered_df1['sales_channel'].values[0]}")

        with st.expander("RFM Score Information"):
            st.write(f"*RFM Score:* {filtered_df1['rfm_score'].values[0]}")

        with st.expander("Estimated Household Income Information"):
            st.write(f"*Estimated Household Income:* {filtered_df1['Est_HH_Income'].values[0]}")

        # Find the corresponding row in Dataset 2 based on matching Column 1 values
        matching_row_df2 = df2[df2['Customer_ID'] == user_input]

        # Display information from Column 2 of dataset 2 for the matching row
        if not matching_row_df2.empty:
            corresponding_value = matching_row_df2['verbatims'].values[0]
            st.info(f'*verbatims:* {corresponding_value}')
        else:
            st.warning("No verbatims:")
    else:
        st.warning("Please make sure you enter a valid value from Column 1 of Dataset 1.")

    # Add specific content for Page 2 if needed
elif selected_page == 'Page 3':
    st.sidebar.write("You are on Page 3")
    import pandas as pd
    import streamlit as st
    import folium


    # Assuming you have two datasets named data.xlsx and Geography_lookup.csv
    # Load datasets into dataframes
    dataset1 = pd.read_excel('data.xlsx')
    dataset2 = pd.read_csv('Geography_lookup.csv')

    # Take column 1 value from the user using Streamlit input
    column1_value_dataset1 = st.selectbox('Enter a value from Column 1 of dataset 1', dataset1['Customer_ID'].unique())

    # Check if the user input is not empty
    if column1_value_dataset1:
        # Check if there are any matching rows in dataset1
        matching_rows_dataset1 = dataset1[dataset1['Customer_ID'] == column1_value_dataset1]

        if not matching_rows_dataset1.empty:
            # Extract the value from 'zipcode_primary'
            column2_value_dataset1 = matching_rows_dataset1['zipcode_primary'].iloc[0]
            st.write(f"Column 2 value of dataset 1 for column 1 value '{column1_value_dataset1}': {column2_value_dataset1}")

            # Compare column 2 value of dataset 1 with column 1 of dataset 2
            matching_rows_dataset2 = dataset2[dataset2['zipcode_primary'] == column2_value_dataset1]

            # Display information from dataset 2 for matching rows
            if not matching_rows_dataset2.empty:
                result_dataframe = matching_rows_dataset2[['region_lat', 'region_long', 'state_lat', 'state_long', 'city_lat', 'city_long', 'zip_lat', 'zip_long']]
                st.write("Information from dataset 2:")
                st.write(result_dataframe)
            else:
                st.write("No matching rows found in dataset 2.")
        else:
            st.write(f"No matching rows found in dataset 1 for column 1 value '{column1_value_dataset1}'.")
    else:
        st.write("Please enter a valid Customer_ID value.")

    def main():
        st.title("Location Displacement on Map")

        # Input for latitude and longitude
        lat = st.number_input("Enter Latitude:", value=37.7749)
        lon = st.number_input("Enter Longitude:", value=-122.4194)

        # Map creation using Folium
        m = folium.Map(location=[lat, lon], zoom_start=15)

        # Add a marker to the map
        folium.Marker([lat, lon], popup="Selected Location").add_to(m)

        # Get the HTML code of the map
        map_html = m.repr_html()

        # Streamlit to display the map HTML
        st.components.v1.html(map_html, width=800, height=600, scrolling=True)

    if name_to_rgb == "_main_":
        main()