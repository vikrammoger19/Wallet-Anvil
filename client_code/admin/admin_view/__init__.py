from ._anvil_designer import admin_viewTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime
import re
import base64

class admin_view(admin_viewTemplate):
    def __init__(self, user_data=None, phone_number=None, user=None, **properties):
        self.user = user
        if self.user is not None:
            self.label_6566.text = self.user

        self.phone_number = phone_number
        self.init_components(**properties)
        self.check_profile_pic()
        self.populate_balances()
        self.edit_mode = False

        if phone_number is not None:
            self.label_401.text = phone_number

            user_data = app_tables.wallet_users.get(phone=phone_number)
            if user_data is not None:
                self.label_100.text = user_data['username']
                self.label_201.text = user_data['email']
                self.label_501.text = user_data['aadhar']
                self.label_601.text = user_data['pan']
                self.label_401.text = user_data['phone']
                self.label_701.text = user_data['address']
                self.label_801.text = user_data['country']
                
                # Set the status label
                self.set_status_label(user_data['inactive'])

            else:
                self.label_100.text = ""
                self.label_201.text = ""
                self.label_401.text = ""
                self.label_501.text = ""
                self.label_601.text = ""
                self.label_701.text = ""
                self.label_801.text = ""
                self.label_901.text = ""

            self.set_button_text()

    def set_status_label(self, inactive_status):
        if inactive_status:
            self.label_901.text = "Inactive"
            self.label_901.foreground = "red"
        else:
            self.label_901.text = "Active"
            self.label_901.foreground = "green"


    def populate_balances(self):
      try:
          # Retrieve balances for the current user based on phone number
          user_phone = self.phone_number
          user_balances = app_tables.wallet_users_balance.search(phone=user_phone)
  
          # Print the retrieved data for debugging
          print("Retrieved balances:", list(user_balances))
  
          # Check if no balances are found
          if not list(user_balances):
              self.label_1000.text = "User doesn't have any balance"
              return
  
          # Initialize index for card and components
          card_index = 1
          label_index = 1  # Start from label_1
          country_label_index = 50  # Start from label_50 for country
          image_index = 1
  
          # Iterate over user balances and update card components
          for balance in user_balances:
              currency_type = balance['currency_type']
              balance_amount = balance['balance']
  
              # Lookup the currency icon, symbol, and country in the wallet_currency table
              currency_record = app_tables.wallet_currency.get(currency_code=currency_type)
              currency_icon = currency_record['currency_icon'] if currency_record else None
              country = currency_record['country'] if currency_record else None
  
              # Get card and components for the current index
              card = getattr(self, f'card_{card_index}', None)
              label_curr_type = getattr(self, f'label_{label_index}', None)
              label_balance = getattr(self, f'label_{label_index + 1}', None)
              label_country = getattr(self, f'label_{country_label_index}', None)
              image_icon = getattr(self, f'image_icon_{image_index}', None)
  
              # Debugging output for components
              print(f"Card {card_index}: {card}")
              print(f"Label Curr Type {label_index}: {label_curr_type}")
              print(f"Label Balance {label_index + 1}: {label_balance}")
              print(f"Label Country {country_label_index}: {label_country}")
              print(f"Image Icon {image_index}: {image_icon}")
  
              if card and label_curr_type and label_balance and image_icon and label_country:
                  # Update card components with balance data
                  label_curr_type.text = currency_type
                  label_balance.text = f"{balance_amount} "
                  label_country.text = country
                  label_balance.icon = f"fa:{currency_type.lower()}"
                  
  
                  # Ensure image_icon exists and update if it does
                  if image_icon:
                      image_icon.source = currency_icon
  
                  # Set card visibility to True
                  card.visible = True
  
                  # Increment indices for the next iteration
                  card_index += 1
                  label_index += 2
                  country_label_index += 1
                  image_index += 1
  
          # Set visibility of remaining cards to False if no data
          while card_index <= 12:
              card = getattr(self, f'card_{card_index}', None)
              if card:
                  card.visible = False
              card_index += 1
  
      except Exception as e:
          # Print any exception that occurs during the process
          print("Error occurred during population of balances:", e)


    def fetch_and_display_balance(self, currency_type):
        if not currency_type:
            # If the text box is empty, display all balances
            self.populate_balances()
            return

        try:
            # Convert the currency type to uppercase
            currency_type = currency_type.upper()

            # Retrieve balance for the entered currency type
            user_phone = self.phone_number
            balance_record = app_tables.wallet_users_balance.get(phone=user_phone, currency_type=currency_type)

            if balance_record:
                balance_amount = balance_record['balance']

                # Lookup the currency icon, symbol, and country in the wallet_currency table
                currency_record = app_tables.wallet_currency.get(currency_code=currency_type)
                currency_icon = currency_record['currency_icon'] if currency_record else None
                country = currency_record['country'] if currency_record else None

                # Update card_1 components with balance data
                self.label_1.text = currency_type
                self.label_2.text = f"{balance_amount}"
                self.label_2.icon = f"fa:{currency_type.lower()}"
                self.label_50.text = country
                self.image_icon_1.source = currency_icon

                # Set card_1 visibility to True
                self.card_1.visible = True
            else:
                # If no balance found, hide card_1
                self.card_1.visible = False

            # Hide all other cards
            for i in range(2, 13):
                card = getattr(self, f'card_{i}', None)
                if card:
                    card.visible = False

        except Exception as e:
            # Print any exception that occurs during the process
            print("Error occurred during fetching and displaying balance:", e)
    def button_5_click(self, **event_args):
      username = self.label_100.text
      user_to_update = app_tables.wallet_users.get(username=username)
      
      if user_to_update is not None:
          # Check the current state of 'hold' column
          current_state = user_to_update['hold']
      
          # If 'hold' is None or 'true', user is considered frozen, otherwise unfrozen
          new_state = not current_state
      
          # Update the 'hold' column in the 'users' table
          user_to_update.update(hold=new_state if new_state else None)
          
          # Update the 'banned' column based on freeze/unfreeze action
          user_to_update.update(banned=True if new_state else None)
      
          # Update button text based on the new state
          self.set_button_text()
      
          # Display alert based on the action
          alert_message = "User is frozen." if new_state else "User is unfrozen."
          alert(alert_message, title="Status")
      
          # Log the action
          self.log_action(username, [alert_message])
          print("Button 5 Clicked and action logged")  # Debug statement

    def set_button_text(self):
        username = self.label_100.text
        user_to_update = app_tables.wallet_users.get(username=username)
    
        # Get the current hold state from the database
        current_state = user_to_update['hold'] if user_to_update else None
    
        # Set the button text based on the current hold state
        self.button_5.text = "Unfreeze" if current_state else "Freeze"

    def button_2_click(self, **event_args):
      """This method is called when the button is clicked"""
      # Check if the user has balances
      if not self.has_balances():
          # Get the phone number from the form
          phone_number = self.phone_number
          
          # Retrieve the user based on phone number
          user_to_delete = app_tables.wallet_users.get(phone=phone_number)
          
          if user_to_delete is not None:
              username = user_to_delete['username']  # Get the username before deleting the row
              user_to_delete.delete()
              
              # Log the deletion action
              self.log_action(username, ["User deleted"])
              
              # Open the admin.account_management form
              open_form('admin.account_management', user=self.user)
              
              # Optionally, display an alert to inform the user
              alert("User deleted successfully.", title="Status")
      else:
          # If the user has balances, inform the admin that they cannot delete the user
          alert("User has balances. Please clear the balances before deleting.", title="Status")

    def has_balances(self):
        """Check if the user has balances."""
        # Retrieve balances for the current user based on phone number
        user_phone = self.phone_number
        user_balances = app_tables.wallet_users_balance.search(phone=user_phone)
        
        # Check if any balances exist for the user
        return bool(list(user_balances))

    # def toggle_edit_mode(self):
    #     # Toggle between view and edit modes
    #     self.edit_mode = not self.edit_mode
    #     self.text_box_1.enabled = self.edit_mode
    #     self.text_box_2.enabled = self.edit_mode
    #     # self.text_box_3.enabled = self.edit_mode
    #     self.text_box_4.enabled = self.edit_mode
    #     self.text_box_5.enabled = False  # Aadhar (not editable during edit mode)
    #     self.text_box_6.enabled = False  # Pan (not editable during edit mode)
    #     self.text_box_7.enabled = self.edit_mode
    #     self.text_box_8.enabled = self.edit_mode

    #     # Change button_1 text based on the mode
    #     self.button_1.text = 'Save Changes' if self.edit_mode else 'Edit'
        
    def is_valid_phone(self, phone):
        # Check if the phone number is not empty and has exactly 10 digits
        return bool(phone and re.match(r'^\d{10}$', str(phone)))
        
    # def button_1_click(self, **event_args):
    #     if self.edit_mode:
    #         # Validate phone number
    #         if not self.is_valid_phone(self.label_401.text):
    #             alert("Please enter a valid 10-digit phone number.", title="Error")
    #             return

    #         # Save changes to the database
    #         username = self.text_box_1.text
    #         user_to_update = app_tables.wallet_users.get(username=username)

    #         if user_to_update is not None:
    #             changes_made = []
    #             # Check and log changes made by the admin
    #             if user_to_update['email'] != self.text_box_2.text:
    #                 changes_made.append(f"User '{username}' Email updated to '{self.text_box_2.text}'")
    #             if user_to_update['password'] != self.text_box_3.text:
    #                 changes_made.append(f"User '{username}' Password updated")
    #             if user_to_update['phone'] != self.text_box_4.text:
    #                 changes_made.append(f"User '{username}' Phone number updated to '{self.text_box_4.text}'")
    #             if user_to_update['address'] != self.text_box_7.text:
    #                 changes_made.append(f"User '{username}' Address updated to '{self.text_box_7.text}'")
    #             if user_to_update['country'] != self.text_box_8.text:
    #                 changes_made.append(f"User '{username}' country updated to '{self.text_box_8.text}'")

    #             user_to_update.update(
    #                 email=self.text_box_2.text,
    #                 password=self.text_box_3.text,
    #                 phone=self.text_box_4.text,
    #                 aadhar=self.text_box_5.text,
    #                 pan=self.text_box_6.text,
    #                 address=self.text_box_7.text,
    #                 country=self.text_box_8.text
    #             )

    #             # Log changes to 'actions' table if changes were made
    #             if changes_made:
    #                 self.log_action(username, changes_made)

    #             alert("Changes saved successfully.", title="Success")

    #             # Toggle back to view mode after saving changes
    #             self.toggle_edit_mode()
    #     else:
    #         # Toggle to edit mode
    #         self.toggle_edit_mode()

    def log_action(self, username, changes):
        # Log the action in the 'actions' table
        
        action = ", ".join(changes)
        app_tables.actions.add_row(username=username, changes=action, date=datetime.now())
        print("Action logged:", action)

    def button_3_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('admin.account_management',user=self.user)

    def button_8_click(self, **event_args):
      """This method is called when the button is clicked"""
      open_form('Login')

    def link_8_copy_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('admin',user=self.user)

    def link_3_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('admin.admin_view',user=self.user)

    def link_5_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('admin.audit_trail',user=self.user)

    def link_6_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('admin.admin_add_user',user=self.user)

    def link_7_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('admin.transaction_monitoring',user=self.user)

    def link_2_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('admin.account_management',user=self.user)
    # def file_loader_1_change(self, file, **event_args):
    #   """This method is called when a new file is loaded into this FileLoader"""
    #   uploaded_file = self.file_loader_1.file
    #   print(uploaded_file)
    #   self.file_loader_1.text = ''
    #   if uploaded_file:
    #       # Check if the file is an image by inspecting the content type or file extension
    #       if uploaded_file.content_type.startswith("image/"):
    #         resized_image = anvil.server.call('resizing_image',uploaded_file)
    #         user_data = app_tables.wallet_users.get(phone=self.user['phone'])
    #         user_data.update(profile_pic=resized_image['base_64'])
            
    #         self.image_1.source=resized_image['media_obj']
    #         # print(f"Uploaded image: {uploaded_file.name}")
    #       else:
    #         print("Uploaded file is not an image.")

    # def check_profile_pic(self):
    #   # print(self.user,self.password)
    #   user_data = app_tables.wallet_users.get(username=str(self.user['username']),password=str(self.password))
    #   if user_data:
    #     existing_img = user_data['profile_pic']
    #     if existing_img != None:
    #       decoded_image_bytes = base64.b64decode(existing_img)
    #       profile_pic_blob = anvil.BlobMedia("image/png",decoded_image_bytes )
    #       self.image_1.source = profile_pic_blob
    #     else: 
    #       print('no pic')
        
    # def button_4_click(self, **event_args):
    #   """This method is called when the button is clicked"""
    #   if self.user['profile_pic'] != None:
    #     user_data = app_tables.wallet_users.get(phone=self.user['phone'])
    #     user_data.update(profile_pic=None)
    #     self.image_1.source = '_/theme/account.png'
    def link_1_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('admin.report_analysis',user=self.user)

    def link_4_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form('admin.user_support',user=self.user)

    def button_4_click(self, **event_args):
      """This method is called when the button is clicked"""
      # Get the phone number of the current user
      phone_number = self.phone_number
      
      # Open the admin.set_limit form and pass the phone number
      open_form('admin.set_limit', user=self.user, phone_number=phone_number)
  

    def display_user_activity(self, user_phone):
    # Retrieve user's balance information from the database
      user_balances = app_tables.wallet_users_balance.search(phone=user_phone)
    
    # Reset card visibility
      self.card_1.visible = False
      self.card_2.visible = False
      self.card_3.visible = False
      self.card_4.visible = False
    
    # Loop through each balance record
      for balance_record in user_balances:
        currency_type = balance_record['currency_type']
        balance_amount = balance_record['balance']
        
        # Update the corresponding label with the balance amount
        if currency_type == 'INR':
            self.card_1.visible = True
            self.label_10.text = str(balance_amount)
        elif currency_type == 'USD':
            self.card_2.visible = True
            self.label_11.text = str(balance_amount)
        elif currency_type == 'EUR':
            self.card_3.visible = True
            self.label_12.text = str(balance_amount)
        elif currency_type == 'GBP':
            self.card_4.visible = True
            self.label_13.text = str(balance_amount)
    def check_profile_pic(self):
      
      user_data = app_tables.wallet_users.get(phone=self.phone_number) #changed
      if user_data:
        existing_img = user_data['profile_pic'] if user_data['profile_pic'] else print('none')
        if existing_img != None:
          decoded_image_bytes = base64.b64decode(existing_img)
          profile_pic_blob = anvil.BlobMedia("image/png",decoded_image_bytes )
          self.image_1.source = profile_pic_blob
        else: 
          print('no pic')
      else:
        print('none')

    def button_7_click(self, **event_args):
      """This method is called when the button is clicked"""
      self.label_1000.visible = True
      self.card_51.visible = True
    
