import sqlite3 as sql
import uuid
from contextlib import contextmanager
import uuid as u
import datetime as dt



class Database_Bank:

    # ========================================
    # open or create database
    # make a method for create a connection
    # =======================================
    def __init__(self):
        db_file = "Main_bank.db"
        self.create_tables()

    @contextmanager
    def create_connection(self,db_file="Main_bank.db"):
        conn = sql.connect(db_file, check_same_thread=False, timeout=10)
        try:
            conn.execute("PRAGMA journal_mode=WAL")
            yield conn #for stop this method temporary when any method called
            conn.commit()
            # in our code , the [with] keyword will not save anything and commit it because will use our own context manager so the built-in context manager will be ignored , so we need to commit all transactions here manually
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
            #always will close the connection even the connection successeed or failed


    @contextmanager
    def auto_connect(self,current_connection=None):
        #we will deal with this method to create connection in other DB methods
        if current_connection is not None :
            #means we have connection
            yield current_connection
            #we don't need to use error handling or close the database or even use commit due to that the main method who has that connection will deal with all of these things , because its connection has been created by create_connection which has the handling errors
        else:
            #if there is no exist connection then create one by create_connection()
            with self.create_connection() as main_con:
                yield main_con
                #after yield the with keyword will end this method control and give the  control to create_connection() which is resposible of commit all changes and close the connection directly


    def create_tables(self):
            sql_create_user = """
                    CREATE TABLE IF NOT EXISTS bank_users (
                            account_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                            username TEXT NOT NULL unique,
                            first_name TEXT NOT NULL,
                            last_name TEXT NOT NULL,
                            password TEXT NOT NULL,
                            balance INTEGER NOT NULL default 0
                            )

                    """
            sql_create_admin = """
                    create table if not exists admin (
                    admin_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    admin_username TEXT NOT NULL,
                    password TEXT NOT NULL)
                    """

            sql_transaction_table = """
                    CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    account_id INTEGER NOT NULL,           
                    action_type TEXT NOT NULL,           
                    description TEXT,                    
                    amount INTEGER default 0,              
                    timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (account_id) REFERENCES bank_users (account_id)
            ) 
                    """
            with self.auto_connect() as main_con:
                main_con.execute(sql_create_user)
                main_con.execute(sql_create_admin)
                main_con.execute(sql_transaction_table)
                main_con.execute("PRAGMA foreign_keys = ON;")
                #this to make sure that sqlite will active the foreign key

    def clear_table(self,table_name):
        sql_command =f"DELETE FROM {table_name}"
        with self.auto_connect() as main_con:
            try:
                main_con.execute(sql_command)
                return True
            except Exception:
                return False

    def execute_any_command(self,command_format,table_name,parameters=(),conn=None):
        sql_command= command_format.format(table_name)
        with self.auto_connect(conn) as main_con:
            try:
               return main_con.execute(sql_command,parameters).fetchall()

            except Exception:
                return False



    #===============================
    # users DML methods
    #===============================

    def register_user(self,username,first_name,last_name,password,balance=0,conn=None):
        sql_insert_user = """
        INSERT INTO bank_users (username,first_name,last_name,password,balance) values (?,?,?,?,?)
        """
        balance_cents= int(100 * balance)
        with self.auto_connect(conn) as active_con:
            active_con.execute(sql_insert_user, (username,first_name,last_name,password,balance_cents))

    def check_if_user_exists(self,account_id,conn=None): #by ID
        sql_command = """
        SELECT 1 FROM bank_users WHERE account_id = ? LIMIT 1
        """
        with self.auto_connect(conn) as active_con:
            is_exist = active_con.execute(sql_command, (account_id,)).fetchone()
            return is_exist is not None

    def check_username_existence(self,username,conn=None): #by username
        sql_command = """
        SELECT 1 FROM bank_users WHERE username = ?
        """
        with self.auto_connect(conn) as active_con:
            is_exist = active_con.execute(sql_command, (username,)).fetchone()
            #will return 1 if any record found , will return None if nothing found
            return is_exist is not None #conditional statement [True or False]

    def get_all_users(self,conn=None):
        sql_command = """
        SELECT * FROM bank_users
        """
        with self.auto_connect(conn) as active_con:
            all_data = active_con.execute(sql_command).fetchall()
            return all_data

    def find_user_by_username(self,username,conn=None):
        SQl_command ="SELECT * FROM bank_users WHERE username = ?"
        with self.auto_connect(conn) as active_con:
            return active_con.execute(SQl_command, (username,)).fetchone()

    def find_user_by_id(self,account_id,conn=None):
        sql_command = """
        SELECT * FROM bank_users WHERE account_id = ?
        """
        with self.auto_connect(conn) as active_con:
            cur = active_con.execute(sql_command, (account_id,))
            selected_user = cur.fetchone()
            return selected_user

    def get_balance_in_cents(self,account_id,conn=None):
        sql_command = """ SELECT balance FROM bank_users WHERE account_id = ? """
        with self.auto_connect(conn) as active_con:
            return active_con.execute(sql_command, (account_id,)).fetchone()

    def remove_user_by_id(self,account_id,conn=None):
        sql_command="""
        DELETE FROM bank_users WHERE account_id = ?
        """
        with self.auto_connect(conn) as active_con:
            active_con.execute(sql_command, (account_id,))
            return True

    def update_user_by_id(self,account_id,all_changes,ref_id=None,conn=None):
        allowed_changes =["username","first_name","last_name","password"]
        sql_command = """
        UPDATE bank_users SET username = ?,first_name = ?,last_name = ?,password = ?,balance = ? WHERE account_id = ?
        """

        #check all entered changes are valid and stored it in new dictionary as accepted
        accepted_changes = {type_of_change:new_value  for type_of_change,new_value in all_changes.items() if type_of_change in allowed_changes}
        #if one of these changes are not allowed it will be ignored and only stored the valid

        if not accepted_changes:
            raise ValueError("some changes are not allowed")

        if ref_id is None:
           ref_id= str(uuid.uuid4())

        update_columns = ",".join([f"{col}=?" for col in accepted_changes.keys()])
        #this will return first_name=?,last_name=?
        SQL_command = f"UPDATE bank_users SET {update_columns} WHERE account_id = ?"
        #this will make the command complete
        new_values = list(accepted_changes.values())
        new_values.append(account_id)
        # will save the values only in list then we convert it to tuple

        with self.auto_connect(conn) as active_con:
            active_con.execute(SQL_command,(tuple(new_values)))
            #we passed it as tuple because sqlite3 accept only the typle values
            for column , new_values in accepted_changes.items():
                info_of_changes = f"Updated {column} to {new_values} for account {account_id}"
                self.add_to_transactions_log(ref_id,account_id,column,info_of_changes,0,conn=active_con)

            return True


    def deposit_money(self,account_id,amount,ref_id=None,conn=None,skip_desc=False):
        action = "Deposit"
        if ref_id is None:
            ref_id = str(uuid.uuid4())
        amount_in_cents = int(100 * amount)
        if amount_in_cents <=0:
            return False
        with self.auto_connect(conn) as active_con:
            the_current_balance=self.get_balance_in_cents(account_id,conn=conn)
            sql_command = """update bank_users set balance = balance + ? where account_id = ?"""
            if active_con.execute(sql_command, (amount_in_cents,account_id)).rowcount>0:
                if not skip_desc:
                    self.add_to_transactions_log(ref_id,account_id,action,f"The ammount {amount} JOD has been deposited for account {account_id}",amount,conn=active_con)
                return True
            return False

    def withdraw_money(self,account_id,amount,ref_id=None,conn=None,skip_desc=False):
        amount_in_cents = int(100 * amount)
        if ref_id is None:
            ref_id = str(uuid.uuid4())
        if amount_in_cents <= 0:
            return False
        with self.auto_connect(conn) as active_con:
            the_current_balance=self.get_balance_in_cents(account_id,conn=active_con)
            if amount_in_cents > the_current_balance[0]:
                return False
            sql_command = """update bank_users set balance = balance - ? where account_id = ?"""
            valid_withdraw = active_con.execute(sql_command, (amount_in_cents,account_id))
            if valid_withdraw.rowcount>0:
                if not skip_desc:
                    self.add_to_transactions_log(ref_id,account_id,"Withdraw",f"The amount {amount} JOD has been withdrawn from account {account_id}",amount,conn=active_con)
                return True
            # we used active_con to make sure the callee method with use the current connection deposite of it is exist connection or new connection

    def transfer_money(self,sender_id,receiver_id,amount,ref_id=None,conn=None):
        # we don't convert the amount here to cents by multiplied by 100 , because we already will convert it in the other methods [withdraw , deposit]
        if ref_id is None:
            ref_id = str(uuid.uuid4())

        if sender_id == receiver_id:
            return False
        with self.auto_connect(conn) as active_con:
            #pass to method the current connection and current ref_id
            if not self.withdraw_money(sender_id,amount,ref_id,conn=active_con,skip_desc=True):
                self.add_to_transactions_log(ref_id,sender_id,"Failed Transfer",f"The account {sender_id} doesn't has enough balance",amount,conn=None)
                return False # failed
            if not self.deposit_money(receiver_id,amount,ref_id,conn=active_con,skip_desc=True):
                raise Exception("transfer money failed")
            #we raise an error here to let the connection method to catch that error and make rollback all changes

            #otherwise return true refer to [the transfer completed successfully]
            self.add_to_transactions_log(ref_id,sender_id,"Transfer",f"The amount {amount} JOD has been sent to account no. {receiver_id}",amount,conn=active_con)
            self.add_to_transactions_log(ref_id,receiver_id,"Transfer",f"The amount {amount} JOD has been received from account no. {sender_id}",amount,conn=active_con)
            return True


    #=======================================
    # transactions methods
    #=======================================

    def add_to_transactions_log(self,ref_id,acc_id,action_type,description,amount=0,conn=None):
        sql_insert_transaction = """
        INSERT INTO transactions (account_id,action_type,description,amount,reference_id) values (?,?,?,?,?)
        """
        #database will add the time automatically
        with self.auto_connect(conn) as active_con:
            active_con.execute(sql_insert_transaction, (acc_id,action_type,description,amount,ref_id))

    def get_transactions_log(self):
        sql_get_transactions = """
        SELECT * FROM transactions ORDER BY timestamp DESC
        """
        with self.auto_connect() as active_con:
            result = active_con.execute(sql_get_transactions).fetchall()
            return result

    def get_user_history(self,account_id,conn=None):
        sql_get_user_history = "SELECT * FROM transactions WHERE account_id = ? ORDER BY timestamp DESC"
        with self.auto_connect(conn) as active_con:
            return active_con.execute(sql_get_user_history,(account_id,)).fetchall()

    def get_full_process_by_ref_id(self,ref_id,conn=None):
        sql_get_full_process_by_ref_id = "SELECT * FROM transactions WHERE reference_id = ?"
        with self.auto_connect(conn) as active_con:
            result = active_con.execute(sql_get_full_process_by_ref_id,(ref_id,)).fetchall()
            return result



    #=================================
    # Admin DML
    #=================================

    def add_admin(self,username,password,conn=None):
        sql_command = "INSERT INTO admin (admin_username,password) VALUES (?,?)"
        with self.auto_connect(conn) as active_con:
            active_con.execute(sql_command,(username,password))
            return True

    def get_all_admins(self,conn=None):
        sql_command = "SELECT * FROM admin"
        with self.auto_connect(conn) as active_con:
            return active_con.execute(sql_command).fetchall()

    def get_admin_by_username(self,username,conn=None):
        sql_command = "SELECT * FROM admin WHERE admin_username = ?"
        with self.auto_connect(conn) as active_con:
            result = active_con.execute(sql_command,(username,)).fetchone()
            return result





