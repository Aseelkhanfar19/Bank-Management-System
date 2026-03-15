import streamlit as st
from databaseManager import Database_Bank as my_db

session = my_db()

st.set_page_config("Admin Dashboard")
if "admin_name"  not in st.session_state:
    st.session_state["admin_name"] = ""
col1, col2, col3 = st.columns([2,6,2])
with col2:


    st.subheader("This is admin Dashboard")
    st.write("please login to continue")
    admin_username = st.text_input("Username")
    admin_password = st.text_input("Password" ,type="password")
    btn= st.button("Login",use_container_width=True)
    back_btn = st.button("Back to main page ",use_container_width=True)
    if btn:
        try:
            id, us , pas = session.get_admin_by_username(admin_username)
            if admin_username == us and admin_password == pas:
                st.success("Login Successful")
                st.session_state["admin_name"] = admin_username
                st.switch_page("pages/tabs_controller.py")
            else:
                st.error("Login Failed")
        except Exception as e:
            st.error(e)

    if back_btn:
        st.switch_page("GUI.py")
