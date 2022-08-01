import streamlit as st
from streamlit_chat import message as st_message
# from transformers import BlenderbotTokenizer
# from transformers import BlenderbotForConditionalGeneration
from transformers import pipeline

# context = '''
# نحن شركة متخصصة فى مجال الزكاء الاصطناعى.
# نقدم العديد من الخدمات كالحلول للشركات و تدريبات فى مجال الزكاء الاصطناعى.
# التدريبات المتاحة الان هى ETE و computer vision.
# سعر ال ETE 4500 جنيه مصرى بدلا من 5000 جنيه.
# وسعر ال computer vision 6000 جنيه مصرى بدلا من 6500 جنيه مصرى.
# '''


@st.cache(allow_output_mutation=True)
def load_model():
    model = pipeline('question-answering',model='ZeyadAhmed/AraElectra-Arabic-SQuADv2-QA')
    return model
qa = load_model()

context = st.text_area("please enter your article")

if "history" not in st.session_state:
    st.session_state.history = []

# st.title('Ask a question about Electro-pi')
# qa = load_model()
# user_message = st.session_state.input_text



def generate_answer():
    user_message = st.session_state.input_text
    # inputs = tokenizer(st.session_state.input_text, return_tensors="pt")
    # result = model.generate(**inputs)

    try:
        message_bot = qa(question= user_message, context= context)
        print(message_bot)

        if message_bot['score'] <= 0.2:
            message_bot = "electrobot: sorry i didn't get that"
            st.session_state.history.append({"message": user_message, "is_user": True})
            st.session_state.history.append({"message": message_bot, "is_user": False})
        else:    
            st.session_state.history.append({"message": user_message, "is_user": True})
            st.session_state.history.append({"message": message_bot['answer'], "is_user": False})
    except:
        print("Empty")

st.text_input("Talk to the bot", key="input_text", on_change=generate_answer)
print('3')
for chat in st.session_state.history:
#     print('4')
    try:
        st_message(**chat)  # unpacking
    except:
        print("ERROR")
        continue
