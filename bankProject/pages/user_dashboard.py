import streamlit as st
from databaseManager import Database_Bank


current_session = Database_Bank()

# to store the id of user , to later use in user_profile.py to fetch user data there
if "user_ID" not in st.session_state:
    st.session_state.user_ID = 0



_,col2,_=st.columns([2,5,2])

with col2:
    st.title("User Dashboard")
    with st.form(" ",width=500,enter_to_submit=True,clear_on_submit=True) as form:
        st.subheader("Login")
        error_msg = st.empty()
        def check_data():
            try:
                if username and password:
                    user_id, u_name, first_name, last_name, pass_word, balance = current_session.find_user_by_username(username)
                    if password == pass_word and username == u_name:
                        st.session_state.user_ID = user_id
                        st.switch_page("pages/user_profile.py")
                    else:
                        error_msg.error("Incorrect username or Password")
                elif username or password:
                    error_msg.error("username and password are required")

            except Exception:
                error_msg.error("Incorrect username or Password")

        username = st.text_input("Username")
        password = st.text_input("Password",type="password")
        login_btn=st.form_submit_button("Login",use_container_width=True,on_click=check_data())
        signup_btn=st.form_submit_button("Sign Up",use_container_width=True)
        back_btn = st.form_submit_button("Back to homepage", use_container_width=True)
        if back_btn:
            st.switch_page("GUI.py")
        if signup_btn:
            st.switch_page("pages/user_signup.py")





