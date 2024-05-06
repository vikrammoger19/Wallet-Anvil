from ._anvil_designer import admin_viewTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime
import re


class admin_view(admin_viewTemplate):
    def __init__(self, user_data=None, phone_number=None,user=None, **properties):
        self.user = user
        self.phone_number = phone_number
        self.init_components(**properties)
        # self.check_profile_pic()
        self.edit_mode = False  # Initialize edit_mode attribute to False
        
        if phone_number is not None:
            self.text_box_4.text = phone_number  # Set textbox13 to display the phone number

            # Fetch all rows from wallet_users_balance table based on phone number
            user_balances = app_tables.wallet_users_balance.search(phone=phone_number)
            if user_balances:
                # Initialize balances for each currency type
                usd_balance = euro_balance = inr_balance = swiss_balance = None
                
                # Iterate over all matching rows
                for balance_row in user_balances:
                    # Check currency type and update corresponding balances
                    if balance_row['currency_type'] == 'USD':
                        usd_balance = balance_row['balance']
                    elif balance_row['currency_type'] == 'EUR':
                        euro_balance = balance_row['balance']
                    elif balance_row['currency_type'] == 'INR':
                        inr_balance = balance_row['balance']
                    elif balance_row['currency_type'] == 'GBP':
                        swiss_balance = balance_row['balance']
                
                # Update text boxes with the retrieved balances
                self.label_10.text = str(usd_balance) if usd_balance is not None else "0"
                self.label_11.text = str(euro_balance) if euro_balance is not None else "0"
                self.label_12.text = str(inr_balance) if inr_balance is not None else "0"
                self.label_13.text = str(swiss_balance) if swiss_balance is not None else "0"
            else:
                # Set default value of 0 for all text boxes if no balances found
                self.label_10.text = "0"
                self.label_11.text = "0"
                self.label_12.text = "0"
                self.label_13.text = "0"
            
            user_data = app_tables.wallet_users.get(phone=phone_number)
            if user_data is not None:
                # Set text boxes with the retrieved user data
                self.text_box_1.text = user_data['username']  # Replace 'column1' with actual column names
                self.text_box_2.text = user_data['email']
                self.text_box_3.text = user_data['password']
                self.text_box_5.text = user_data['aadhar']
                self.text_box_6.text = user_data['pan']
                self.text_box_4.text = user_data['phone']
                self.text_box_7.text = user_data['address']
                self.label_8.text= user_data['username']
                self.text_box_8.text= user_data['country']
            else:
                # Set default value for text boxes if no user data found
                self.text_box_1.text = ""
                self.text_box_2.text = ""
                self.text_box_3.text = ""
                self.text_box_4.text = ""
                self.text_box_5.text = ""
                self.text_box_6.text = ""
                self.text_box_7.text = ""
                self.text_box_8.text = ""

            # Set button text based on the hold state
            self.set_button_text()

    def button_5_click(self, **event_args):
      username = self.text_box_1.text
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
        username = self.text_box_1.text
        user_to_update = app_tables.wallet_users.get(username=username)
    
        # Get the current hold state from the database
        current_state = user_to_update['hold'] if user_to_update else None
    
        # Set the button text based on the current hold state
        self.button_5.text = "Unfreeze" if current_state else "Freeze"

    def button_2_click(self, **event_args):
      """This method is called when the button is clicked"""
      # Check if all text boxes 8, 9, 10, and 11 contain 0
      
      if (self.label_10.text == "0" and
          self.label_11.text == "0" and
          self.label_12.text == "0" and
          self.label_13.text == "0"):
          
          # Get the phone number from the form
          phone_number = self.phone_number
          
          row_to_delete = app_tables.wallet_users.get(phone=phone_number)
          if row_to_delete is not None:
              username = row_to_delete['username']  # Get the username before deleting the row
              row_to_delete.delete()
              
              # Log the deletion action
              self.log_action(username, ["User deleted"])
              
              # Optionally, display an alert to inform the user
              alert("Row deleted from wallet_users table.", title="Status")
      else:
          # If any of the text boxes contain values other than 0, inform the user
          alert("Values in text boxes 8, 9, 10, or 11 are not all 0.", title="Status")


    def toggle_edit_mode(self):
        # Toggle between view and edit modes
        self.edit_mode = not self.edit_mode
        self.text_box_1.enabled = self.edit_mode
        self.text_box_2.enabled = self.edit_mode
        self.text_box_3.enabled = self.edit_mode
        self.text_box_4.enabled = self.edit_mode
        self.text_box_5.enabled = False  # Aadhar (not editable during edit mode)
        self.text_box_6.enabled = False  # Pan (not editable during edit mode)
        self.text_box_7.enabled = self.edit_mode
        self.text_box_8.enabled = self.edit_mode

        # Change button_1 text based on the mode
        self.button_1.text = 'Save Changes' if self.edit_mode else 'Edit'
        
    def is_valid_phone(self, phone):
        # Check if the phone number is not empty and has exactly 10 digits
        return bool(phone and re.match(r'^\d{10}$', str(phone)))
        
    def button_1_click(self, **event_args):
        if self.edit_mode:
            # Validate phone number
            if not self.is_valid_phone(self.text_box_4.text):
                alert("Please enter a valid 10-digit phone number.", title="Error")
                return

            # Save changes to the database
            username = self.text_box_1.text
            user_to_update = app_tables.wallet_users.get(username=username)

            if user_to_update is not None:
                changes_made = []
                # Check and log changes made by the admin
                if user_to_update['email'] != self.text_box_2.text:
                    changes_made.append(f"User '{username}' Email updated to '{self.text_box_2.text}'")
                if user_to_update['password'] != self.text_box_3.text:
                    changes_made.append(f"User '{username}' Password updated")
                if user_to_update['phone'] != self.text_box_4.text:
                    changes_made.append(f"User '{username}' Phone number updated to '{self.text_box_4.text}'")
                if user_to_update['address'] != self.text_box_7.text:
                    changes_made.append(f"User '{username}' Address updated to '{self.text_box_7.text}'")
                if user_to_update['country'] != self.text_box_8.text:
                    changes_made.append(f"User '{username}' country updated to '{self.text_box_8.text}'")

                user_to_update.update(
                    email=self.text_box_2.text,
                    password=self.text_box_3.text,
                    phone=self.text_box_4.text,
                    aadhar=self.text_box_5.text,
                    pan=self.text_box_6.text,
                    address=self.text_box_7.text,
                    country=self.text_box_8.text
                )

                # Log changes to 'actions' table if changes were made
                if changes_made:
                    self.log_action(username, changes_made)

                alert("Changes saved successfully.", title="Success")

                # Toggle back to view mode after saving changes
                self.toggle_edit_mode()
        else:
            # Toggle to edit mode
            self.toggle_edit_mode()

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
      pass
