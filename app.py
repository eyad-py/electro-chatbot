import streamlit as st
from streamlit_chat import message as st_message
from transformers import pipeline


# @st.experimental_singleton
@st.cache(allow_output_mutation=True)

def load_model():
    model = pipeline('question-answering',model='ZeyadAhmed/AraElectra-Arabic-SQuADv2-QA')
    return model
qa = load_model()

context = st.text_area("please enter your article")

if "history" not in st.session_state:
    st.session_state.history = []



def generate_answer():
    user_message = st.session_state.input_text


    try:
        message_bot = qa(question= user_message, context= context)

        if message_bot['score'] <= 0.2:
            message_bot = "sorry i didn't get that"
            st.session_state.history.append({"message": user_message, "is_user": True})
            st.session_state.history.append({"message": message_bot, "is_user": False})
            st.session_state.input_text = ""
            
        else:    
            st.session_state.history.append({"message": user_message, "is_user": True})
            st.session_state.history.append({"message": message_bot['answer'], "is_user": False})
            st.session_state.input_text = ""

    except:
        print("Empty")



st.text_input("Talk to the bot", key="input_text",on_change = generate_answer)

count = 0
for chat in st.session_state.history:
    chat['key']=count
    count +=1
    st_message(**chat)  # unpacking
