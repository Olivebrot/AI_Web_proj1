import pandas as pd  # Importing pandas for data manipulation
import os  # Importing os to handle file paths and system operations
import streamlit as st  # Importing Streamlit for the web app interface

# Define the file path for the CSV file using the current working directory
filepath = os.path.join(os.getcwd(), 'df1.csv')

# Main function that handles the core logic of the Streamlit app
def main():
    st.header('Original Data')

    # Read the CSV file into a DataFrame using pandas
    df1 = pd.read_csv(filepath)

    # Display the original DataFrame in the Streamlit app
    data = st.dataframe(df1)

    # Sidebar form to input new data, cleared after submission
    with st.sidebar.form(key='df1', clear_on_submit=True):
        # Input fields for the country and number of guesses
        add_col1 = st.text_input('country')  # Input for country name
        add_col2 = st.number_input('number_of_guesses', min_value=0)  # Input for number of guesses (only non-negative values)
        
        # Submit button for the form
        submit = st.form_submit_button('Submit')
        
        # If the form is submitted, update the DataFrame
        if submit:
            # Create a new row of data with the provided inputs
            new_data = {'country': add_col1, 'number_of_guesses': add_col2}
            
            # Concatenate the new row with the existing DataFrame
            df1 = pd.concat([df1, pd.DataFrame([new_data])], ignore_index=True)
            
            # Save the updated DataFrame back to the CSV file
            df1.to_csv(filepath, index=False)

    # Display the updated DataFrame after new data is added
    st.header('After Update')
    st.dataframe(df1)

# Check if the script is being run directly and execute the main function
if __name__ == '__main__':
    main()
