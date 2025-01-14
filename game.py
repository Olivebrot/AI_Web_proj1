import streamlit as st
import random
from openai import OpenAI
import re
import os
import pandas as pd


def upd_df1(): #updates the dataset where every game ever played is stored
    country = st.session_state.country
    guesses = st.session_state.guesses

    filepath = os.path.join(os.getcwd(), 'df1.csv')
    df1 = pd.read_csv(filepath)
    
    #it only incluedes country and number of guesses
    new_data = {'country': country, 'number_of_guesses': guesses}
    df1 = pd.concat([df1, pd.DataFrame([new_data])], ignore_index=True)
    df1.to_csv(filepath, index=False)


def aiChat_start(): #in the beginning of every session this has to run for the first prompt
        #giving the Key
    client = OpenAI(api_key=st.secrets["openai"]["api_key"])
    # Model selection
    model = "gpt-4o-mini"

    country_txt = """Afghanistan, Albania, Algeria, Andorra, Angola, Antigua and Barbuda, Argentina, Armenia, Australia, Austria, Azerbaijan, The Bahamas,
                    Bahrain, Bangladesh, Barbados,Belarus, Belgium, Belize, Benin, Bhutan, Bolivia, Bosnia and Herzegovina, Botswana, Brazil, Brunei, 
                    Bulgaria, Burkina Faso, Burundi, Cabo Verde, Cambodia, Cameroon, Canada, Central African Republic, Chad, Chile, China, Colombia, Comoros, 
                    Congo, Democratic Republic of the, Congo, Republic of the, Costa Rica, Côte dIvoire, Croatia, Cuba, Cyprus, Czech Republic, Denmark, Djibouti,
                    Dominica, Dominican Republic, East Timor, Ecuador, Egypt, El Salvador, Equatorial Guinea, Eritrea,Estonia, Eswatini, Ethiopia, Fiji, Finland, 
                    France, Gabon, The Gambia, Georgia, Germany, Ghana, Greece, Grenada, Guatemala, Guinea, Guinea-Bissau, Guyana, Haiti, Honduras, Hungary, Iceland, 
                    India, Indonesia, Iran, Iraq, Ireland, Israel, Italy, Jamaica, Japan, Jordan, Kazakhstan, Kenya, Kiribati, South Korea, North Korea, South, Kosovo,
                    Kuwait, Kyrgyzstan, Laos, Latvia, Lebanon, Lesotho, Liberia, Libya, Liechtenstein, Lithuania, Luxembourg, Madagascar, Malawi, Malaysia,
                    Maldives, Mali, Malta, Marshall Islands, Mauritania, Mauritius, Mexico, Micronesia, Federated States of, Moldova, Monaco, Mongolia, Montenegro, Morocco,
                    Mozambique, Myanmar, Namibia, Nauru, Nepal, Netherlands, New Zealand, Nicaragua, Niger, Nigeria, North Macedonia, Norway, Oman, Pakistan, Palau, Panama, 
                    Papua New Guinea, Paraguay, Peru, Philippines, Poland, Portugal, Qatar, Romania, Russia, Rwanda, Saint Kitts and Nevis, Saint Lucia, Saint Vincent and the Grenadines,
                    Samoa, San Marino, Sao Tome and Principe, Saudi Arabia, Senegal, Serbia, Seychelles, Sierra Leone, Singapore, Slovakia, Slovenia, Solomon Islands, Somalia, South Africa,
                    Spain, Sri Lanka, Sudan, Sudan, South, Suriname, Sweden, Switzerland, Syria, Taiwan, Tajikistan, Tanzania, Thailand, Togo, Tonga, Trinidad and Tobago, Tunisia,
                    Turkey, Turkmenistan, Tuvalu, Uganda, Ukraine, United Arab Emirates, United Kingdom, United States, Uruguay, Uzbekistan, Vanuatu, Vatican City, Venezuela, Vietnam,
                    Yemen, Zambia, Zimbabwe"""
    
    # First prompt: ask the LLM to select a country
    first_prompt = f"""
    Your task is to play a guessing game. Choose a random country that the user will try to guess.
    Respond only with the name of the country in lower letters.
    choose one country out of those:{country_txt}
    """

    # Ask the LLM to select the country
    chat_completion = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": first_prompt}]
    )
    
    # Extract the selected country from the LLM's response
    country = chat_completion.choices[0].message.content.strip()
    
    
    
    # Store the initial state in session for further use
    st.session_state.country = country  # Save the chosen country
    

def aiChat_awnser(guess): #combines the awnser of the first prompt with the question of latest question of the user
    #giving the Key
    client = OpenAI(api_key=st.secrets["openai"]["api_key"])
    # Model selection
    model = "gpt-4o-mini"

    # Second prompt setup: LLM's instruction for the game phase
    second_prompt = f"""
    Your task is to play a guessing game where the user tries to guess the country "{st.session_state.country}".
    You can only answer "Yes" or "No" to the user's questions.
    The Question of the User: "{guess}"
    """
    
    st.session_state.rules = second_prompt  # Save the rules

    # Ask the LLM to select the country
    chat_completion = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": second_prompt}]
    )

    awnser = chat_completion.choices[0].message.content.strip()
    return awnser


def reset_session():
    aiChat_start()
    st.session_state.guesses = 0
    st.session_state.history = []
    st.session_state.game = True

# Initialize session state variables if not already set
if 'country' not in st.session_state:
    reset_session()

st.title('Mystery Country Guessing Game')

#creates two buttons one to restart the game and one for dev to know the awnser
left, right = st.columns(2)
if left.button("New Game", use_container_width=True):
    left.markdown("Okay new game")
    reset_session()
if right.button("help", icon="😃", use_container_width=True):
    right.markdown("okay here is your hint")
    right.markdown(st.session_state.country)

#links the game page to the statsitics page
st.page_link("pages/statistics.py", label="Statistics")

#the first text and beginning of each session starting from the assistant
#two modes game is going = true or game ended = false
if st.session_state.game == True:
    with st.chat_message("assistant"):
        st.markdown('Guess the Country I am thinking of')
        st.markdown('I will awnser your questions with Yes or No')
        st.markdown('When you know the country Type only the country in lower letters like: "brazil" ')
        st.markdown('If you win you will get a COOKIE')
else:
    with st.chat_message("assistant"):
        st.success(f'Congratulations! You guessed the country in {st.session_state.guesses} guesses.')
        st.markdown('You earned Your COOKIE')
        upd_df1() #updates the csv
        

# Display chat messages from history on app rerun
for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Capture user input
if st.session_state.game == True:
    if guess := st.chat_input('Enter your guess:', key='guess'):
        try: #if try runs else runs as well!
            guess = str(guess)
        except ValueError:
            with st.chat_message("assistant"):
                msg = 'Please enter a valid Text.'
                st.error(msg)
                st.session_state.history.append({'role': 'assistant', 'content': msg})
        else:
            
            #add a guess to the guesses and save it
            st.session_state.guesses += 1
            user_msg = f'Guess #{st.session_state.guesses}: {guess}'
            st.session_state.history.append({"role": "user", "content": user_msg})
            
            #writes teh save down in the chat
            with st.chat_message("user"):
                st.markdown(user_msg)

            #Check the guess

            if guess == st.session_state.country:
                st.session_state.game = False
                st.rerun()
            else:#if guess wrong gbt awnsers with yes or no
                with st.chat_message("assistant"):
                    st.write(aiChat_awnser(guess))
        
                
                    
           

