import pandas as pd 
# import streamlit as st 
import os 
import streamlit as st 

filepath = os.path.join(os.getcwd(), 'df1.csv')

#""" App Interface  """

def main():
	st.header('Original Data')
	df1 = pd.read_csv(filepath)
	data = st.dataframe(df1)

	with st.sidebar.form(key='df1', clear_on_submit=True):
		add_col1 = st.text_input('country')
		add_col2 = st.number_input('number_of_guesses', min_value=0)
		submit = st.form_submit_button('Submit')
		if submit:
			new_data = {'country': add_col1, 'number_of_guesses': add_col2}

			df1 = pd.concat([df1, pd.DataFrame([new_data])], ignore_index=True)
			df1.to_csv(filepath, index=False)

	st.header('After Update')
	st.dataframe(df1)



if __name__ == '__main__':
	main()