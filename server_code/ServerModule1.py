import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, timezone
import anvil.server
from anvil import tables, app
import random
import anvil.email
import base64
# from PIL import Image,ImageDraw
from io import BytesIO
#import datetime

@anvil.server.callable
def get_user_for_login(login_input):
  user_by_username = app_tables.wallet_users.get(users_username=login_input)
  if login_input.isdigit():
    phone_number = int(login_input)
    user_by_phone = app_tables.wallet_users.get(users_phone=phone_number)
    return user_by_phone
    # Continue with the rest of your code
  else:
    print("Invalid phone number. Please enter a numeric value.")
  user_by_email = app_tables.wallet_users.get(users_email=login_input)
  if user_by_username:
            return user_by_username
  if user_by_email:
            return user_by_email 
  else:
            return None

@anvil.server.callable
def add_info(username, email, address, phone, aadhar, pan, password):
    user_row = app_tables.wallet_users.add_row(
        users_username=username,
        users_email=email,
        users_address=address,
        users_phone=phone,
        users_aadhar=int(aadhar),              
        users_pan=pan,
        users_password=password,   
        users_usertype='customer',
        users_confirm_email=True,
        users_user_limit=(100000),
        users_last_login = datetime.now()
    )
    return user_row

@anvil.server.callable
def get_acc_data(phone):
    user_accounts = app_tables.wallet_users_account.search(phone=phone)
    return [acc['account_number'] for acc in user_accounts]

@anvil.server.callable
def get_user_account_numbers(phone):
    user_accounts = app_tables.wallet_users_account.search(phone=phone)
    return [acc['account_number'] for acc in user_accounts]

@anvil.server.callable
def get_username(phone):
    user = app_tables.wallet_users.get(phone=phone)
    if user:
        return user['username']
    else:
        return "Username Not Found"      
      
@anvil.server.callable
def get_currency_code():
    currencies = app_tables.wallet_currency.search()
    return [f"{currency['currency_code']}" for currency in currencies]


###

@anvil.server.callable
def get_user_by_phone(phone_number):
    try:
        phone_number = int(phone_number)  # Convert the phone_number to an integer
        users = app_tables.wallet_users.search(users_phone=phone_number)

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
def get_user_bank_name(phone):
  bank_names = app_tables.wallet_users_account.search(phone=phone)
  return bank_names
@anvil.server.callable
def get_username(phone):
  user = app_tables.wallet_users.get(phone=phone)
  return user['username'] 
@anvil.server.callable
def get_user_currency(phone):
  currency= app_tables.wallet_users_balance.search(phone=phone)
  return currency

@anvil.server.callable
def get_wallet_transactions():
    return app_tables.wallet_users_transaction.search()

@anvil.server.callable
def get_transaction_proofs():
    # Fetch proof data from the 'transactions' table
    transaction_proofs = app_tables.wallet_users_transaction.search()
    return transaction_proofs

@anvil.server.callable
def get_transactions():
    return app_tables.wallet_users_transaction.search()

@anvil.server.callable
def get_user_data():
    # Fetch user data from the 'users' table
    users_data = app_tables.wallet_users.search()

    # Create a list to store user information
    user_list = []

    # Iterate through each user's data
    for user_row in users_data:
        # Check the 'banned' column to determine if the user is active or non-active
        if user_row['banned'] is None:
            status = 'Active'
        else:
            status = 'Non-Active'

        # Check the 'inactive' column to determine if the user is inactive
        if user_row['inactive'] is None:
            activity_status = 'Active'
        else:
            activity_status = 'Inactive'

        # Append user information to the list
        user_info = {
            'username': user_row['username'],
            'banned': user_row['banned'],
            'inactive': user_row['inactive'],
            'status': status,  # Include the 'status' information based on the 'banned' column
            'activity_status': activity_status  # Include the 'activity_status' information based on the 'inactive' column
        }
        user_list.append(user_info)

    return user_list

@anvil.server.callable
def update_daily_limit(name, emoney_value):
    user_row = app_tables.users.get(username=name)  # Use get() instead of search() if username is unique

    if user_row is not None:
        user_row['user_limit'] = emoney_value
        user_row.update()
        return "Daily limit updated successfully"
    else:
        return "User not found"
@anvil.server.callable
def user_detail(name, no):
    user_row = app_tables.wallet_users.get(username=name)
    
    if user_row is not None:
        try:
            # Try to convert 'no' to a numeric type
            numeric_no = float(no)
            user_row['daily_limit'] = numeric_no
            user_row.update()
            return "Daily limit updated successfully"
        except ValueError:
            return "Invalid daily limit value. Please provide a numeric value."
    else:
        return "User not found"


# anvil.server.call('get_username', self.user['phone'])
@anvil.server.callable
def get_username(phone_number):
    user = app_tables.wallet_users.get(users_phone=phone_number)
    return user['users_username'] if user else None

@anvil.server.callable
def get_inr_balance(phone):
  balance = app_tables.wallet_users_balance.search(users_balance_phone=phone)
  return balance

@anvil.server.callable
def get_balance_using_phone_number(phone_number, currency_type):
    # Convert the phone_number to a numeric type
    phone_number = int(phone_number)
    # Use query to filter rows based on both 'phone' and 'currency_type'
    account = app_tables.wallet_users_balance.search(
        phone=phone_number,
        currency_type=currency_type
    )
    try:
        return account[0]
    except IndexError:
        # If IndexError occurs (empty list), return a default value
        return {'balance': None, 'phone': phone_number, 'currency_type': currency_type}

@anvil.server.callable
def update_balance_transaction(phone_number, new_balance, currency_type):
    print(f"Updating balance for {phone_number} with new balance {new_balance} in currency {currency_type}")
    phone_number = int(phone_number)
    balances = app_tables.wallet_users_balance.search(
        phone=phone_number,
        currency_type=currency_type
    )
    # Iterate through the list of balances or choose the appropriate row based on your criteria
    for balance in balances:
        # Convert new_balance to the appropriate type (number)
        new_balance = float(new_balance)
        balance.update(balance=new_balance)
    # If you want to handle the case where no rows matched the query
    if not balances:
        print("Adding a new row...")
        # Create a new row with the provided information
        app_tables.wallet_users_balance.add_row(phone=phone_number, balance=new_balance, currency_type=currency_type)
    else:
        print("Row already exists.")
    print("Update complete.")



@anvil.server.callable
def update_depositor_balance(depositor_phone_number, new_balance, currency_type):
    # Convert the depositor_phone_number to a numeric type
    depositor_phone_number = int(depositor_phone_number)
    # Use search to get all rows matching the query for depositor
    depositor_balances = app_tables.wallet_users_balance.search(
        phone=depositor_phone_number,
        currency_type=currency_type
    )
    # Iterate through the list of depositor_balances or choose the appropriate row based on your criteria
    for depositor_balance in depositor_balances:
        new_balance = float(new_balance)
        depositor_balance.update(balance=new_balance)
    # If you want to handle the case where no rows matched the query for depositor
    if not depositor_balances:
        # Create a new row with the provided information for depositor
        app_tables.wallet_users_balance.add_row(phone=depositor_phone_number, balance=new_balance, currency_type=currency_type)


@anvil.server.callable
def update_receiver_balance(receiver_phone_number, new_balance, currency_type):
    # Convert the receiver_phone_number to a numeric type
    receiver_phone_number = int(receiver_phone_number)
    # Use search to get all rows matching the query for receiver
    receiver_balances = app_tables.wallet_users_balance.search(
        phone=receiver_phone_number,
        currency_type=currency_type
    )
    # Iterate through the list of receiver_balances or choose the appropriate row based on your criteria
    for receiver_balance in receiver_balances:
        new_balance = float(new_balance)
        receiver_balance.update(balance=new_balance)
    # If you want to handle the case where no rows matched the query for receiver
    if not receiver_balances:
        # Create a new row with the provided information for receiver
        app_tables.wallet_users_balance.add_row(phone=receiver_phone_number, balance=new_balance, currency_type=currency_type)

@anvil.server.callable
def get_currency_balance(user_phone, currency_type):
    # Retrieve the balance for the given user and currency type
    user_rows = app_tables.wallet_users_balance.search(phone=user_phone, currency_type=currency_type)
    
    if len(user_rows) > 0:
        # Assuming there's only one row per user and currency type, return the balance
        return user_rows[0]['balance']
    else:
        return None 
      
@anvil.server.callable
def send_otp_email(email, otp):
    """
    Sends an OTP to the specified email address and stores it in the server session.
    """
    # Check if the email exists in the database
    if validate_email(email):
        # Compose email message
        subject = "Your One Time Password (OTP)"
        message = f"Your OTP is: {otp}"
        
        # Send email
        anvil.email.send(
            to=email,
            subject=subject,
            text=message
        )

        # Store the OTP in the server session
        anvil.server.session['stored_otp'] = otp

        print("OTP sent:", otp)
    else:
        print("Email not found. OTP not sent.")

@anvil.server.callable
def get_stored_otp():
    """
    Returns the stored OTP from the server session.
    """
    return anvil.server.session.get('stored_otp')
@anvil.server.callable
def validate_email(email):
    """
    Validates if the provided email exists in the database.
    """
    matching_users = app_tables.wallet_users.search(users_email=email)
    return bool(matching_users)

@anvil.server.callable
def generate_otp():
    """
    Generates a 6-digit OTP.
    """
    return ''.join(random.choice('0123456789') for _ in range(6))

@anvil.server.callable
def resizing_image(file):
    try:
      # Open the image
      byte_stream = BytesIO(file.get_bytes())
      byte_stream.seek(0)
      with Image.open(byte_stream) as img:
          # dashboard_screen = self.manager.get_screen('dashboard')
          siz = img.size
          # print('size: ', siz)
          # resizing the image
          img = img.resize((250, 250), Image.Resampling.LANCZOS)
          # img.crop((0,200,250,250))
          mask = Image.new('L', (250, 250), 0)
          draw = ImageDraw.Draw(mask)
          draw.ellipse((0, 0, 250, 250), fill=255)
  
          # apply mask to image
          img.putalpha(mask)
          with BytesIO() as processed:
            img.save(processed,format="PNG")
            processed.seek(0)
            media_obj = anvil.BlobMedia(f"image/png", processed.read())
            processed.seek(0)
            for_base64 = processed.read()
            image_base64 = base64.b64encode(for_base64).decode('utf-8')
      return {'media_obj':media_obj,'base_64':image_base64}
    except Exception as e:
      print(e)


@anvil.server.callable
def update_active_status():
    # Get today's date
    today = datetime.now().date()
    
    # Query all users from wallet_users
    all_users = app_tables.wallet_users.search()
    
    # Iterate through each user
    for user in all_users:
        # Get the last login date for the user
        last_login = user['users_last_login']
        
        # Calculate the difference in days between last login and today
        if last_login is not None:
            days_difference = (today - last_login.date()).days
            
            # Check if the difference is greater than 90 days
            if days_difference > 90:
                # Update the active column to False
                user['users_inactive'] = True
            else:
                # Update the active column to True
                user['users_inactive'] = None
                
            # Save the changes to the table
            user.update()

@anvil.server.callable
def get_credit_debit(phone_number,default_currency):
  debit_details = app_tables.wallet_users_transaction.search(transaction_type='Debit',phone=phone_number,currency=default_currency)
  credit_details = app_tables.wallet_users_transaction.search(transaction_type='Credit',phone = phone_number,currency=default_currency)
  return {'debit_details':debit_details,'credit_details':credit_details}