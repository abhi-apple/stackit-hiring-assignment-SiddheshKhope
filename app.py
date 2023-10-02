import streamlit as st
import gspread 

def main():
    st.title("Google Sheets Input Collector")
    st.subheader("Please share your Google Sheet access with: csv-importer@csv-importer-400714.iam.gserviceaccount.com")
    
    s = gspread.service_account(filename="./%APPDATA%/gspread/service_account.json")

    sheet_url = st.text_input("Enter the Google file name:")
    sheet_name = st.text_input("Enter the Sheet Name:")

    if st.button("Submit"):
        try:
            sa = s.open(sheet_url)
            x = sa.worksheet(sheet_name)
            st.session_state['success'] = True
            st.session_state['sheet_url'] = sheet_url
            st.session_state['sheet_name'] = sheet_name
            st.experimental_rerun()  # Rerun the app after success
        except Exception as e:
            st.warning(f"Failed to connect to Google Sheets: {e}")

if 'success' not in st.session_state:
    st.session_state['success'] = False

if st.session_state['success']:
    # If success is True, run the success_page app.
    exec(open("success_page.py").read())
else:
    main()
