import datetime as dt
import time

import streamlit as st
import pandas as pd
from databaseManager import Database_Bank
user_session = Database_Bank()


tab1,tab2,tab3,tab4= st.tabs(["User Info","My balance","Change password","Transactions"])
edit_mode_btn = "Save"
un_edit_mode = "Edit User Profile"
sucess_msg = "Sucess"
failed_msg = "Failed"
if "sucess_flag" not in st.session_state:
    st.session_state["sucess_flag"] = False


#add keys to save btns mode and switch between them
def add_new_keys():
    if "btn_name" not in st.session_state:
        st.session_state["btn_name"] = un_edit_mode
    if "edit_mode" not in st.session_state:
        st.session_state["edit_mode"] = False
add_new_keys()

#for enable and disable input
input_state = not st.session_state["edit_mode"]

#just alert when user refresh the page
@st.dialog("We can't find your data")
def alert_msg():
    st.write("This session has ended , you need to logout and login again")
    if st.button("Logout"):
        st.switch_page("pages/user_dashboard.py")


#this key is necessary for get data from database
#Reserve a place in Session to store user info from DB
if "updated_data" not in st.session_state:
    st.session_state["updated_data"] = None

#Fetch data from DB
def update_data():
    updated = user_session.find_user_by_id(st.session_state.user_ID)
    st.session_state["updated_data"] = updated
    # return user_session.find_user_by_id(st.session_state.user_ID)

#check if user logged in or not
#This key is from user_dashboard.py and want to check before start display data
if "user_ID" in st.session_state: #as long as user logging in
    update_data()
    user_id, u_name, first_name, last_name, pass_word, balance = st.session_state["updated_data"]
if "user_ID" not in st.session_state:
    alert_msg()
    st.stop()

if "display_msg" not in st.session_state:
    st.session_state["display_msg"] = ""

#------------------------
#this method will be called if the user click on edit or save , while modifying data
def edit_user_profile():
    # if user click on edit
    if st.session_state["btn_name"] == un_edit_mode:
        st.session_state["edit_mode"] = True
        st.session_state["btn_name"] = edit_mode_btn

    # if user clicked on save
    elif st.session_state["btn_name"] == edit_mode_btn:
        try:
            #we added key to each input below to use it and compare with
            entered_name = st.session_state["new_username"]
            entered_first_name = st.session_state["my_name"]
            entered_last_name = st.session_state["new_last_name"]



            if entered_first_name == "" or entered_last_name == "" or entered_name == "":
                st.error("Username , First name and Last name should not be empty !")
            else:
                saved_data = user_session.find_user_by_id(st.session_state.user_ID)
                not_changes = []
                the_new_data ={
                    "username": entered_name,
                    "first_name": entered_first_name,
                    "last_name": entered_last_name
                }
                mapping = {"username": 1, "first_name": 2, "last_name": 3}
                for key, values in the_new_data.items():
                    indexed_name = mapping[key]
                    if str(values) == str(saved_data[indexed_name]):
                        not_changes.append(key)
                for k in not_changes:
                    the_new_data.pop(k)
                if the_new_data:
                    user_session.update_user_by_id(display_id,the_new_data)
                st.session_state["updated_data"] = user_session.find_user_by_id(display_id)
                st.session_state["edit_mode"] = False
                st.session_state["btn_name"] = un_edit_mode
                st.session_state["display_msg"] = sucess_msg
        except Exception as e:
            st.write(e)
            st.session_state["display_msg"] = failed_msg
            return 0





#confirm the transfer
@st.dialog("Transfer Info")
def transfer_confirmation(sender_id,target_ID,first_name_rec,lasr_name_rec,diposited_amount):
    if "Transfer_Date" not in st.session_state:
        st.session_state["Transfer_Date"] = dt.datetime.now().strftime("%d/%m/%Y")
    if "Transfer_Time" not in st.session_state:
        st.session_state["Transfer_Time"] = dt.datetime.now().strftime("%H:%M:%S")

    Account_id="Account ID: "+ " " + str(target_ID)
    st.write(Account_id)
    fullName = "Full Name: " + str(first_name_rec) + "  " + str(lasr_name_rec)
    st.write(fullName)
    desired_amount = "Amount: " + "" + str(diposited) + " JOD "
    st.write(desired_amount)
    date ="Date:  " + st.session_state["Transfer_Date"]
    time = "Time:  " + st.session_state["Transfer_Time"]
    st.write(str(date))
    st.write(str(time))
    if st.button("Confirm"):
        #here will return a true value and store it inside st.session
        respond=user_session.transfer_money(sender_id,target_ID,diposited_amount)
        del st.session_state["Transfer_Date"]
        del st.session_state["Transfer_Time"]
        if respond:
            st.session_state["sucess_flag"] = True
            st.rerun()

        elif not respond:
            st.session_state["sucess_flag"] = False
            st.rerun()




#Profile
with tab1:
    col1, col2, col3 = st.columns([2, 6, 1])

    with col1:
        for _ in range(2):
            st.space()
        lft,_,_= st.columns([3,1,1])
        with lft:
            st.image(r"image\user_icon.webp")
            if st.button("Logout"):
                st.session_state["edit_mode"] = False
                st.session_state["btn_name"] = un_edit_mode
                if "user_ID" not in st.session_state:
                    del st.session_state["user_ID"]
                st.switch_page("pages/user_dashboard.py")

    def print_msg():
        if st.session_state["display_msg"]==sucess_msg:
            pass
            if st.session_state["display_msg"] == "":
                st.rerun()
        elif st.session_state["display_msg"]==failed_msg:
            st.error("this username is already taken")
    with col2:
        print_msg()
        with st.form("user_pro",enter_to_submit=True):
            current_display_name = st.session_state.get("my_name",first_name)
            st.subheader(f"{current_display_name}'s profile")

            display_id=st.text_input("Acoount ID:",value=user_id,disabled=True)
            displayed_name=st.text_input("username:",value=u_name,disabled=input_state,key="new_username")
            displayed_fname= st.text_input("First name:",value=st.session_state["updated_data"][2],disabled=input_state,key="my_name")
            displayed_lname=st.text_input("Last name:",value=last_name,disabled=input_state,key="new_last_name")
            save_info_btn=st.form_submit_button(st.session_state["btn_name"],use_container_width=True,on_click=edit_user_profile)

#Balance and Transfer
with tab2:

    col1, col2, col3 = st.columns([3, 6, 1])
    with col1:
        @st.fragment(run_every=5)
        def update_balance():
            balance_in_jod=user_session.get_balance_in_cents(user_id)[0]/100
            balance_with_currency=f"{balance_in_jod:.2f} JOD "
            my_current_balance = st.text_input("Current Balance:", value=balance_with_currency, disabled=True)

        update_balance()



    with col2:
        process_message=st.empty()
        def processes_msg(result,msg):
            if result:
                process_message.success(msg)
            else:
                process_message.error(msg)

            time.sleep(3)
            process_message.empty()


        with st.form("balance_wid",clear_on_submit=True) as form:
            diposited = st.number_input("Amount",key="dipo",min_value=0.0,max_value=500.0,step=1.0)
            target_ID = st.number_input("Reciever ID",key="target_ID",min_value=0)
            to_user_id = st.empty()
            if st.form_submit_button("Transfer",use_container_width=True):
                if st.session_state["dipo"] > user_session.get_balance_in_cents(user_id)[0]/100:
                    processes_msg(False,"You don't have enough money to transfer")
                else:
                    if target_ID != user_id:
                        if diposited >0 and target_ID >0:
                            reciever_info = user_session.find_user_by_id(target_ID)
                            if reciever_info: # if not None
                                rec_id, rec_u_name, rec_fname, rec_lame, pa_rec, b_rec = reciever_info
                                if transfer_confirmation(user_id,rec_id,rec_fname,rec_lame,diposited):
                                    st.rerun()

                            else:
                                processes_msg(False,"This account ID is not found")
                        else :
                            processes_msg(False,"Amount and account ID are required")

                    else:
                        processes_msg(False,"You cannot transfer money to yourself")

    if st.session_state["sucess_flag"]:
        process_message.success("You have successfully transfer money ")
        st.session_state["sucess_flag"] = False

#change password
with tab3:
    # st.write(pass_word)
    msg_space = st.empty()
    def msg_appear(the_result,msg):
        if the_result:
            msg_space.success(msg)
        else:
            msg_space.error(msg)
        time.sleep(3)
        msg_space.empty()


    with st.form("Change password",enter_to_submit=True,clear_on_submit=True):
        current_password = st.text_input("Password:",key="cur_password")
        new_password_inp= st.text_input("New Password:",key="new_password")
        conf_pass=st.text_input("Confirm Password:",key="conf_pass")

        change_pass_btn = st.form_submit_button("Change password")
        reset_btn = st.form_submit_button("Reset")
        if change_pass_btn:
            if st.session_state["cur_password"] != pass_word:
                msg_appear(False,"The password you entered is incorrect")
            else:
                if st.session_state["new_password"]:
                    if st.session_state["new_password"] != st.session_state["conf_pass"]:
                        msg_appear(False,"The confirm password you entered does not match the new password")
                    else:
                        if st.session_state["cur_password"] != st.session_state["new_password"]:
                            user_session.update_user_by_id(user_id,{"password":st.session_state["new_password"]})
                            msg_appear(True,"Password has been changed")
                        else:
                            msg_appear(False,"Your old password can't be your new password")
                else:
                    msg_appear(False,"Please enter your new password")

#Display Transaction log
with tab4:

    @st.fragment(run_every=5)
    def automatically_refresh():
        columns_names = ["ID", "account no.", "Type", "Description", "Amount", "Time", "Ref ID"]
        fetched_data=user_session.get_user_history(user_id)
        user_transactions=pd.DataFrame(fetched_data,columns=columns_names)
        st.dataframe(user_transactions,use_container_width=True,hide_index=True,
                     column_order=("Ref ID","Description","Time"),
                     column_config={
                         "Ref ID": st.column_config.TextColumn("Ref ID", width="small"),
                         "Description": st.column_config.TextColumn("Description", width="large"),
                         "Time": st.column_config.TextColumn("Time", width="medium"),
                     })
    automatically_refresh()














