import streamlit as st
import pandas as pd
import gspread
from gspread_dataframe import set_with_dataframe

st.title('CSV Importer for Google Sheets (Streamlit)')

# This assumes that the connection with Google Sheets has already been set up in the previous file.
s = gspread.service_account(filename="./%APPDATA%/gspread/service_account.json")

# The sheet_url and sheet_name from the previous file should be passed to this file.
# For now, I'll assume they're in the session state.
sheet_url = st.session_state['sheet_url']
sheet_name = st.session_state['sheet_name']

uploaded_file = st.file_uploader("Drag & Drop CSV File Here", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("Uploaded Data Preview:")
    st.write(data.head())

    # Allow users to select columns to import
    selected_columns = st.multiselect(
        "Select the columns you want to import",
        options=data.columns.tolist(),
        default=data.columns.tolist()  # Default is to select all columns
    )
    
    # Filter dataframe based on selected columns
    data = data[selected_columns]

    # Checkbox to enable the column mapping feature
    enable_mapping = st.checkbox("Enable column mapping feature")
    
    try:
        # Open the spreadsheet and worksheet
        sa = s.open(sheet_url)
        worksheet = sa.worksheet(sheet_name)

        # Check column names in the Google Sheet
        google_sheet_columns = worksheet.row_values(1)  # Assuming the first row contains column headers

        if enable_mapping:
            # Allow users to select a single column to append
            selected_column = st.selectbox("Select a column to append from the CSV", options=data.columns.tolist())

            # Allow user to map the selected CSV column to an existing Google Sheet column
            mapped_column = st.selectbox("Map the selected CSV column to an existing Google Sheet column", options=google_sheet_columns)

            if st.button("Append Selected Column to Google Sheets"):
                # Find the index of the mapped column in the Google Sheet
                col_idx = google_sheet_columns.index(mapped_column) + 1  # +1 because gspread is 1-indexed

                # For each row in the Google Sheet, update the corresponding cell in the mapped column
                for i, value in enumerate(data[selected_column], start=2):  # Start from 2 as the first row is the header
                    worksheet.update_cell(i, col_idx, value)

                st.success("Selected column appended to Google Sheets successfully!")
                
        else:
            if st.button("Append Selected Columns to Google Sheets"):
                # Check missing columns in the Google Sheet
                missing_columns = list(set(data.columns) - set(google_sheet_columns))
                
                # If there are missing columns, append them to the Google Sheet
                if missing_columns:
                    for col in missing_columns:
                        google_sheet_columns.append(col)
                    worksheet.insert_row(google_sheet_columns, 1)

                # Convert the dataframe to a list of lists and append to the Google Sheet
                rows = data.values.tolist()
                for row in rows:
                    worksheet.append_row(row)

                st.success("Data appended to Google Sheets successfully!")
                
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")







