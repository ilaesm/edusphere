import streamlit as st
import openai
def main():
    st.set_page_config(layout='wide', page_title="HealthMint Wellness App", page_icon=":sleep:")
    st.sidebar.caption('Please fill out the following information:')        # session state
    if 'age' not in st.session_state:
        st.session_state['age'] = 1
        st.session_state['subjects'] = "Math"

    # user inputs (using stored values as initial values)
    st.session_state['age'] = st.sidebar.number_input('Age', min_value=1, value=st.session_state['age'])
    st.session_state['subjects'] = st.sidebar.multiselect(
        'Which of the following do you study?',
        ["Math", "English", "Biology", "Physics", "Chemistry", "History", "Marketing", "Economics", "Psychology", "Computer Science"],
        default=st.session_state.get("subjects", []))


    col1, col2 = st.columns(2)
    with col1:
        with open("logo.svg", "r") as file:
            svg_logo = file.read()
        st.markdown(svg_logo, unsafe_allow_html=True)
    st.divider()
    st.subheader("Hi, I'm EduAI, your Virtual Tutor, ready to assist with everything school related")
    openai.api_key = st.sidebar.text_input('Please enter your OpenAI API Key', type="password")
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-3.5-turbo"

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Hi"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            for response in openai.ChatCompletion.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            ):
                full_response += response.choices[0].delta.get("content", "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        st.session_state.messages.append({"role": "assistant", "content": full_response})
if __name__ == "__main__":
    main()
