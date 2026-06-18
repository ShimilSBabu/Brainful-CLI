import streamlit as st
import requests

fastapi_endpoint = "http://127.0.0.1:8080/run_cli_agent"

st.title("Smart CLI Agent", text_alignment="center")
# st.header("Smart CLI Agent", text_alignment="center", divider="gray")
st.subheader("Where Believed Agent-Human Borders Blur..!", text_alignment="center")
# st.header("Smart CLI Agent")

user_id = st.text_input(
    "User ID", 
    help="Enter your User ID.",
    placeholder="Eg:- User_1"
    )
user_query = st.text_input(
    "Query", 
    help="Enter your Query.",
    placeholder="Eg:- List all jpeg files in this directory.")

if user_query:
    if st.button("Click Me", width="content"):
        fastapi_endpoint+=f"?state_input_user_query={user_query}&thread_id={user_id}"
        message = requests.get(
            fastapi_endpoint,
            stream=False
        )
        print(f"response({type(message.text)}): {message.text}")
        st.markdown("### Output")
        st.success(f"The result is\n{message.text.replace("\n", "\n\n")}")
