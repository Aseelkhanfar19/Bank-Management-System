import streamlit as st

st.set_page_config(page_title='Bank Management',page_icon="🏦")

col1, col2, col3 = st.columns([1,5,1])
with col2:
    st.header("I'm a/an")
    option = st.selectbox(" ",['Select..','User','Admin'],)
    if option == 'User':
        st.switch_page("pages/user_dashboard.py")
    elif option == 'Admin':
        st.switch_page("pages/admin_dashboard.py")


