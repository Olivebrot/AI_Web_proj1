import streamlit as st
import random

def reset_session():
    st.session_state.secret_number = random.randint(1, 100)
    st.session_state.guesses = 0
    st.session_state.history = []

# Initialize session state variables if not already set
if 'secret_number' not in st.session_state:
    reset_session()

st.title('Guess My Number')

with st.chat_message("assistant"):
    st.markdown('I have a number between 1 and 100. Can you guess it?')
    st.markdown('I will tell you if you are too high or too low.')

# Display chat messages from history on app rerun
for message in st.session_state.history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Capture user input
if guess := st.chat_input('Enter your guess:', key='guess'):
    try: #If t
        guess = int(guess)
    except ValueError:
        with st.chat_message("assistant"):
            msg = 'Please enter a valid number.'
            st.error(msg)
            st.session_state.history.append({'role': 'assistant', 'content': msg})  # Corrected 'historz' typo
    else:
        st.session_state.guesses += 1  # Corrected 'guessses' typo
        user_msg = f'Guess #{st.session_state.guesses}: {guess}'
        st.session_state.history.append({"role": "user", "content": user_msg})
        
        with st.chat_message("user"):
            st.markdown(user_msg)

        # Check the guess
        if guess == st.session_state.secret_number:
            with st.chat_message("assistant"):
                st.success(f'Congratulations! You guessed the number in {st.session_state.guesses} guesses.')
                if st.button("Start over"):
                    reset_session()  # Reset the game if the button is clicked
        else:
            if guess < st.session_state.secret_number:
                msg = f'{guess} is too low. Try again!'
            else:
                msg = f'{guess} is too high. Try again!'
            
            st.session_state.history.append({'role': 'assistant', 'content': msg})
            with st.chat_message("assistant"):
                st.markdown(msg)
