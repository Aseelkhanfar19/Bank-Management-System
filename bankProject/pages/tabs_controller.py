import pandas as pd
import streamlit as st
from databaseManager import Database_Bank

current_session = Database_Bank()
st.subheader(st.session_state["admin_name"])






#body of the page


#create tabs in body
tab1,tab2,tab3,tab5= st.tabs(["See all users","add new user","Transactions","modify user"])


#show all user
with tab1:
    hide_btn =None #this will be toggle and for use it outside the if condition
    st.title("Users Info")
    user_table = st.empty()
    btn_place = st.empty()
    cols_names = ["ID ","username", "First name", "Last Name", "Password", "Balance"]



    btn = btn_place.button("show all users",use_container_width=True)
    if btn:
        row = current_session.get_all_users()
        pd_data = pd.DataFrame(row, columns=cols_names)
        user_table.table(pd_data)
        hide_btn=btn_place.button("Close",use_container_width=True)
    if hide_btn:
        user_table.empty()

#add new user
with tab2:
    st.title("Add new user")
    empty_place = st.empty()
    user_name = st.text_input("Enter username")
    first_name = st.text_input("First Name")
    last_name = st.text_input("Last Name")
    user_password = st.text_input("Enter password",type="password")
    confirm_password = st.text_input("Confirm password",type="password")
    add_btn = st.button("Finish", use_container_width=True)
    if add_btn:
        if user_name and last_name:
            if (confirm_password and user_password) and (user_password == confirm_password) and user_name:
                current_session.register_user(user_name,first_name,last_name,user_password)
                empty_place.success("you added new user successfully")
            elif user_password != confirm_password:
                empty_place.error("password do not match")
            else:
                empty_place.error("enter password and confirm password")
        else:
            empty_place.error("username and last is required")

#Transactions monitor
with tab3:
    if "transactions_records" not in st.session_state:
        st.session_state["transactions_records"] = current_session.get_transactions_log()
    st.header("Transactions Monitor")
    view_mode = st.radio("View Mode",["All","Process reference number","User transactions"],horizontal=True)
    search_bar = st.empty()
    transactions_table = st.empty() #will display table here
    columns_names = ["ID","account no.","Type","Description","Amount","Time","Ref ID"]
    if view_mode == "Process reference number":
        result = search_bar.text_input("Reference Number",placeholder="example 67vf3092-r731-468d-c5de-kf18b3e9ade5")
        if result:
            st.session_state["transactions_records"] = current_session.get_full_process_by_ref_id(result)

    elif view_mode == "User transactions":
        result = search_bar.text_input("User Transactions",placeholder="Enter account number..")
        if result:
            st.session_state["transactions_records"]=current_session.get_user_history(result)






    @st.fragment(run_every=5)
    def display_all_transactions():
        if st.session_state["transactions_records"]:
            if view_mode == "All":
                st.session_state["transactions_records"]=current_session.get_transactions_log()
            trans=st.session_state["transactions_records"]
            pd_trans=pd.DataFrame(trans, columns=columns_names)
            transactions_table.dataframe(pd_trans,use_container_width=True,hide_index=True,
                                         column_order=("Ref ID","account no.","Type","Description","Time"))

display_all_transactions()

#modify user
with tab5:
    rst_space = st.empty()
    reset_btn = rst_space.button("Reset")
    if reset_btn:
        if st.session_state.show_inputs and st.session_state.user_data:
            st.session_state.user_data = ""
            st.session_state.show_inputs = False
    if "show_inputs" not in st.session_state:
        st.session_state.show_inputs = False
    # list_of_keys=["id","user_name","fname","lname","password","balance"]
    #
    #
    #
    # #define keys in session
    # for key in list_of_keys:
    #     if key not in st.session_state:
    #         st.session_state[key] = ""
    space_msg=st.empty()
    col_1,col_2,col_3,col_4,col_5,col_6 = st.columns(6)
    #-----------------------
    with col_1:
        userID_space = st.empty()
    with col_2:
        username_space = st.empty()
    with col_3:
        first_name_space = st.empty()
    with col_4:
        last_name_space = st.empty()
    with col_5:
        password_space = st.empty()
    with col_6:
        balance_space = st.empty()
    #------------------------
    saved_btn = st.empty()
    search_inp_space = st.empty()
    search_space = st.empty()

    def get_info_from_database(user_id):
        return current_session.find_user_by_id(user_id)

    div = st.empty() #for divider


    search_bar = search_inp_space.text_input("", placeholder="Enter user ID..")
    con_btn =search_space.button("Continue",use_container_width=True) #place for continue button



    if con_btn:

        #update the state only when the info got data from db
        saved_info = get_info_from_database(search_bar)

        #save them in the st.session
        #if we get info then we show the info as inputs
        if saved_info:
            st.session_state.user_data = saved_info
            st.session_state.show_inputs = True

        #if the user not found then no data will display
        else:
            space_msg.error("user not found")
            st.session_state.show_inputs = False




    if st.session_state.show_inputs:
        saved_info = st.session_state.user_data #grap the info again from session and store it in this var
        id_input = userID_space.text_input("ID" , disabled=True,value=str(saved_info[0]))
        username_input = username_space.text_input("Username", value=str(saved_info[1]))
        firstname_input = first_name_space.text_input("First Name",value=str(saved_info[2]))
        last_name_input = last_name_space.text_input("Last Name",value=str(saved_info[3]))
        password_input = password_space.text_input("Password",value=str(saved_info[4]))
        balance_input = balance_space.text_input("Balance",value=str(saved_info[5]),disabled=True)
        save_changes = saved_btn.button("Save changes",use_container_width=True)
        if save_changes:
            # this list to store everything didn't changed while updating user info , we will use this list to remove the not changed values from the_new_data dic
            not_changes=[]

            the_new_data ={
                "username": username_input,
                "first_name": firstname_input,
                "last_name": last_name_input,
                "password": password_input
            }
            # dictionary for the expected updated data
            # this dictionary will pass it to DB methods for updating info


            for key,value in the_new_data.items():
                if value in saved_info:
                    # every value has not been changed will append it to the not_changes list
                    not_changes.append(key)

            for key in not_changes:
                the_new_data.pop(key)
                # now will remove every not changed value from dictionary before passing it to the database to reduce the updating process in database


            current_session.update_user_by_id(int(id_input),the_new_data)
            #now the only changed values will pass to DB
            space_msg.success("Changes saved !")


back_btn = st.button("Back to homepage",use_container_width=True)
if back_btn:
    st.switch_page("GUI.py")