import streamlit as st
import random
from openai import OpenAI
import re
import os
import pandas as pd

#read dataset df1


def upd_df1(): #i need st.session_state.guesses and st.session_state.country
    country = st.session_state.country
    guesses = st.session_state.guesses

    filepath = os.path.join(os.getcwd(), 'df1.csv')
    df1 = pd.read_csv(filepath)

    new_data = {'country': country, 'number_of_guesses': guesses}
    df1 = pd.concat([df1, pd.DataFrame([new_data])], ignore_index=True)
    df1.to_csv(filepath, index=False)


def aiChat_start():
    #giving the Key
    client = OpenAI(api_key="sk-svcacct-MsSVPSi-ZLeCMMsNMJebn_K9otA6E5OPWEuk3_c1YS-mIoIS9SrahXzwv46Yo3bT3BlbkFJAG6_9HElJ0l835lTrQ3m3aMBG8T5m1hHC1LViVb604ZwDJEMRbd-0IuaF10U2AA")
    # Model selection
    model = "gpt-4o-mini"
    
    # First prompt: ask the LLM to select a country
    first_prompt = """
    Your task is to play a guessing game. Choose a random country that the user will try to guess.
    Respond only with the name of the country in lower letters.
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
    

def aiChat_awnser(guess):
    #giving the Key
    client = OpenAI(api_key="sk-svcacct-MsSVPSi-ZLeCMMsNMJebn_K9otA6E5OPWEuk3_c1YS-mIoIS9SrahXzwv46Yo3bT3BlbkFJAG6_9HElJ0l835lTrQ3m3aMBG8T5m1hHC1LViVb604ZwDJEMRbd-0IuaF10U2AA")
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

left, right = st.columns(2)
if left.button("New Game", use_container_width=True):
    left.markdown("Okay new game")
    reset_session()
if right.button("help", icon="😃", use_container_width=True):
    right.markdown("okay here is your hint")
    right.markdown(st.session_state.country)

st.page_link("pages/statistics.py", label="Statistics")

if st.session_state.game == True:
    with st.chat_message("assistant"):
        st.markdown('Guess the Country I am thinking of')
        st.markdown('I will awnser your quesiotns with Yes or No and dont write in capital letters')
        st.markdown('When you know the country Type only the country in lower letters like: "brazil" ')
        st.markdown('If you win you will get a COOKIE')
else:
    with st.chat_message("assistant"):
        st.success(f'Congratulations! You guessed the country in {st.session_state.guesses} guesses.')
        st.markdown('You earned Your COOKIE')
        upd_df1()
        

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
            #No Capital letters
            if re.search(r'[A-Z]', guess):
                with st.chat_message("assistant"):
                    msg = 'Please enter a valid Text.'
                    st.error(msg)
                    st.session_state.history.append({'role': 'assistant', 'content': msg})
            
            st.session_state.guesses += 1
            user_msg = f'Guess #{st.session_state.guesses}: {guess}'
            st.session_state.history.append({"role": "user", "content": user_msg})
            
            with st.chat_message("user"):
                st.markdown(user_msg)

            #Check the guess

            if guess == st.session_state.country:
                st.session_state.game = False
                st.rerun()
            else:
                with st.chat_message("assistant"):
                    st.write(aiChat_awnser(guess))
        
                
                    
            
                        
            # else:
            #     if guess < st.session_state.secret_number:
            #         msg = f'{guess} is too low. Try again!'
            #     else:
            #         msg = f'{guess} is too high. Try again!'
                
            #     st.session_state.history.append({'role': 'assistant', 'content': msg})
            #     with st.chat_message("assistant"):
            #         st.markdown(msg)

