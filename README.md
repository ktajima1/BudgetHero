# BudgetHero - Personal Budgeting Application

## Group Members
Keigo Tajima

## Project Description
A Personal Budgeting Application that enables users to track financial spending in multiple currency types

## Dependencies
- sqlalchemy
- requests
- matplotlib
- pandas
- seaborn
- tkcalendar

# Installation
To install dependencies, run: `pip install -r requirements.txt`  

# Run Application
To run the application, first navigate to the config.py file in the root folder. Search for CURRENCY_API_KEY where it should say "your_api_key here". Obtain an API key from 
https://app.currencyapi.com/login by making a free account. Look for the field "Default key" which should start with "cur_live_" and replace CURRENCY_API_KEY with the key. Run `app.py` located in the root folder in Pycharm or run `python app.py` in the terminal.
# Prepopulate Database
To prepopulate the database, run `populate_db.py` located in the root folder in Pycharm or run `python populate_db.py` to create 5 users, 5 categories, and 500 transactions (100 transactions per user). The five users have username:password [user1 : 11111P@ss], [user2 : 22222P@ss], [user3 : 33333P@ss], [user4 : 44444P@ss], and [user5 : 55555P@ss]
# File Structure Overview: 
Files in the Backend folder handle all backend logic. Database models are located in the models/ folder, repository files handle database interactions, and service files handle business logic. Frontend files are split into components and views. Components are reusable interfaces and views put together GUI widgets and components to create a simple GUI for users.

# Known Bugs or Limitations: 
- Deleting categories deletes all transactions in the category for EVERY user
- The dashboard lacks a “View Transactions” page to view all transactions
- The currency conversion feature only offers currency conversion service on the specific page. The feature is not utilized by other features as intended in the original design
- graphs generated in "View Graphs" are not sized properly and require manual window resizing to fit graphs onto the app window
- After creating a brand new user, creating a new transaction not within the last two months causes the dashboard graph to display "January 1970"