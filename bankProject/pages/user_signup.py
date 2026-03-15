import streamlit as st
from databaseManager import Database_Bank


this_session =Database_Bank()


#--- to make the form in center----
_,cen,_ =st.columns([1,3,1])

with cen:
    st.title("Register Form")
    #----to display a msg----
    msg_space = st.empty()
    # check the inputs values
#design the form of the register page
    def signup_page():
        def signup_btn():
            try: #will catch any error like redundant username
                if username_input:
                    if fname_input and lname_input:
                        if password_input and confirm_password_input:
                            if password_input == confirm_password_input:
                                this_session.register_user(username_input,fname_input,lname_input,password_input)
                                msg_space.success("Registered successfully")
                            else:
                                msg_space.warning("Passwords don't match , please try again")
                        else:
                            msg_space.warning("Password is required")
                    else:
                        msg_space.warning("Please enter your first name and last name")
                elif not username_input:
                    msg_space.warning("Please enter your username")
            except Exception as e:
                msg_space.warning("Username is exist, choose another one")
        with st.form("reg",clear_on_submit=True) as form:
            username_input = st.text_input("Username",key="username")
            fname_input = st.text_input("First Name",key="fname")
            lname_input = st.text_input("Last Name",key="lname")
            password_input = st.text_input("Password.",key="password" ,type="password")
            confirm_password_input = st.text_input("Confirm password",key="confirm_password",type="password")
            sign_btn=st.form_submit_button("Register",use_container_width=True)
            sign_in_btn =st.form_submit_button("Sign in",use_container_width=True)
            back_btn = st.form_submit_button("Back to homepage",use_container_width=True)
            if sign_btn:
                signup_btn()
            if sign_in_btn:
                st.switch_page("pages/user_dashboard.py")
            if back_btn:
                st.switch_page("GUI.py")


    signup_page()

