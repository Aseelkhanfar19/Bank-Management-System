from databaseManager import Database_Bank
session = Database_Bank() #for user1
# we used this for inquery about the metadata and the constraints
# print(session.execute_any_command("PRAGMA table_info({})", "transactions"))

# for all_log in session.get_transactions_log():
#     print(*all_log,sep=" | ")
# for row in session.get_user_history(3):
#     print(*row,sep=' | ')

# print("the log by ref ID")
#
# for row in session.get_full_process_by_ref_id("8af4e53f-27b2-4bd5-9ddc-f05cbeb525ec"):
#     print(*row,sep=' | ')

print(session.get_all_users())









