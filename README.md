# 🏦Bank Management System
**This Bank Management System is a comprehensive financial application built using Python and Streamlit, designed to simulate real-world banking operations through a secure and interactive web interface. The system features a dual-interface architecture, providing distinct dashboards for both Administrators and Users to ensure a structured management flow.**
## What can you do ? 
**``Admin Dashboard`` allows you to:**

1- See all users in the system.  
2- Add new user.  
3- Modify user's data.  
4- Monitor all system transactions, filter by UUID Reference IDs, or track specific user history.  

***

**``User Dashboard`` allows you to:**  
1- Login if you have an account.  
2- Sign up if you don't have an account.  
3- Profile Management: View and update personal profile details. 
4- Financial Operations: Check real-time balance and perform secure P2P transfers with a confirmation dialog.
5- Personal Ledger: Access a complete history of all personal transactions.


## 🛠️Built with  
1-**Language:** Python.  
2-**Front-end:** Streamlit.  
3- **Database:** Sqlite3.  
4- **Data Handling:** Pandas.  
5- **For date and time:** datetime , time

## ⚙️Installation and set-up  
1- Open your IDE (PyCharm or VS CODE).  
2- Open the terminal in your IDE.  
3- Execute this command   
```git clone https://github.com/Aseelkhanfar19/Bank-Management-System```  
4- Navigate to the inner folder by ```cd Bank-Management-System/bankProject```  
5- Install Requirements: Run the following command to install all necessary libraries  
```pip install -r requirements.txt```   
6- Run the System: Start the application by executing   
```streamlit run GUI.py```  
### 💡Pro Tip: For the best experience, open the inner bankProject folder directly as your main project directory in your IDE. This ensures that all internal file paths and the SQLite database (Main_bank.db) are recognized correctly. 
### The directory in your IDE should be:
### ✅ ```bankProject```  
### ❌ ```Wallet-System-main\bankProject```.
### 1️⃣ After extract the ZIP file reach this folder below  
![The inner directory](bankProject/Screenshots/Screenshot%202026-03-15%20224314.png)  
### 2️⃣ Then Drag it to IDE 
![IDE Setup Guide](bankProject/Screenshots/InnerFolder.png)



## 🔑Demo Credentials  
**Note: Since the database uses dummy data for testing purposes, you can use the following accounts to explore the system's functionalities without needing to register a new account.**  
### Admin accounts:
**username:** ```admin``` |  **password:** ```1234```   
**username:** ```aseel``` |  **password:** ```1234``` 
### Users accounts:
**username:** ```ja_06```    |  **password:** ```5555```   
**username:** ```vanc_22```  |  **password:** ```1234```  
**username:** ```aseel_05``` |  **password:** ```123```   
**username:** ```el_4```     |  **password:** ```1234``` 
### ⚠️NOTE: You can see all other users by admin dashboard -> first tab -> see all user button

## 📂Project Structure
```databaseManager.py```  The core backend engine containing the Database_Bank class, which manages all SQL logic, context managers, and atomic transactions.  
```main.py```  File for test and run the database methods directly on terminal without UI.  
```GUI.py```  The main application entry point that handles page navigation.  
```pages/``` A directory containing the individual scripts for the Admin and User dashboards.  
```pages/admin_dashboard.py```  Login form as an admin.  
```pages/tabs_controller.py``` Admin profile to control and monitor all data.  
```pages/user_dashboard.py``` Where you logged in as a normal user if you have an account.  
```pages/user_profile.py``` User profile.  

## 🚀Future Improvements
**As part of my ongoing learning journey in Computer Science, I have identified several strategic areas for future enhancement. These improvements aim to optimize system performance, strengthen security protocols, and ensure the scalability of the application.**  

```Audit Logging:``` Add an issued_by column to the transaction and modification logs to distinguish between actions performed by an Admin versus those by the User.  
```Enhanced Security:``` Implement stronger password constraints (Complexity Requirements) and a mandatory password rotation policy (e.g., every 12 months).  
```Session Control:``` Prevent concurrent logins to ensure a user can only be active on one device at a time, protecting against double-spending or unauthorized access.    
```Automated Notifications:``` Integrate SMS and Email APIs to notify users instantly about transfers, balance changes, or new login attempts.  
```Unified Role-Based Access Control (RBAC):```  Refactor the database logic to use a unified User model with a role_type attribute (e.g., Admin vs User).  
```Soft Delete Feature:``` Replace permanent account deletion with an **Active/Inactive** status to preserve historical data and transaction integrit.  
```Data Encryption:``` Upgrade the database security by hashing passwords and encrypting sensitive financial records.


