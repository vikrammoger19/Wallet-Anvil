import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime
import anvil.server
from anvil import tables, app
import random
import uuid

@anvil.server.callable
def get_user_for_login(login_input):
  user_by_username = app_tables.wallet_users.get(username=login_input)
  if login_input.isdigit():
    phone_number = int(login_input)
    user_by_phone = app_tables.wallet_users.get(phone=phone_number)
    return user_by_phone
    # Continue with the rest of your code
  else:
    print("Invalid phone number. Please enter a numeric value.")
  user_by_email = app_tables.wallet_users.get(email=login_input)
  if user_by_username:
            return user_by_username
  if user_by_email:
            return user_by_email 
  else:
            return None

@anvil.server.callable
def add_info(email, username, password, pan, address, phone, aadhar):
    user_row = app_tables.wallet_users.add_row(
        email=email,
        username=username,
        password=password,
        pan=pan,
        address=address,
        phone=phone,
        aadhar=aadhar,
        usertype='customer',
        confirm_email=True,
        user_limit=(100000),
        last_login = datetime.now()
    )
    return user_row

# @anvil.server.callable
# def get_user_by_phone(phone_number):
#     # Convert the phone_number to a number before searching
#     phone_number = int(phone_number)
#     users = app_tables.wallet_users.search(phone=phone_number)
#     return users[0] if users else None

@anvil.server.callable
def get_user_by_phone(phone_number):
    try:
        phone_number = int(phone_number)  # Convert the phone_number to an integer
        users = app_tables.wallet_users.search(phone=phone_number)

        if users and len(users) > 0:
            return users[0]
        else:
            return None
    except ValueError:
        # Handle the case where the input cannot be converted to an integer
        return None
 

@anvil.server.callable
def get_wallet_transactions():
    return app_tables.wallet_users_transaction.search()

@anvil.server.callable
def get_user_bank_name():
  pass
@anvil.server.callable
def get_username(phone):
  print(phone)
  user = app_tables.wallet_users.get(phone=phone)

    # Check if any row was found
  if user:
      
      else:
          print("The 'username' column does not exist in the 'wallet_users' table.")
  else:
      print("No user found for the given phone number.")
  
    









#https://menu-email.anvil.app