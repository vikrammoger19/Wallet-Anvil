from ._anvil_designer import ViewprofileTemplate
from anvil import *
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil import alert, open_form
import re
import base64
from datetime import datetime
class Viewprofile(ViewprofileTemplate):
    def __init__(self, user=None,password=None, **properties):
        
        self.init_components(**properties)
        self.user = user
        self.password = password
        self.check_profile_pic()
        self.edit_mode = False  # Initial edit mode is set to False
        self.label_1.text=self.user['users_username']
        self.label_8.text=self.user['users_email']
        dt = datetime.fromisoformat(str(self.user['users_last_login']))

        # Extract date and time without fractional seconds and timezone
        formatted_date_time = dt.strftime("%Y-%m-%d %H:%M:%S")
        self.label_12.text=formatted_date_time
        if user:
            #self.label_8.text = f"Welcome to Green Gate Financial, {user['users_username']}"
            self.display_user_profile(user)  # Display user profile on form load

    def toggle_edit_mode_components(self):
        # Show/hide text boxes based on edit mode
        for i in range(1, 5):
            textbox = getattr(self, f'text_box_{i}')
            textbox.visible = self.edit_mode

        self.button_11.text = "Edit" if not self.edit_mode else "Save"

    def display_user_profile(self, user):
        # Fetch and display data for the logged-in user
        # You can customize this based on your table structure
        user_data = app_tables.wallet_users.get(users_phone=user['users_phone'])
        self.text_box_1.text = f"{user_data['users_email']}"
        self.text_box_2.text = f"{user_data['users_phone']}"
        self.text_box_3.text = f"{user_data['users_pan']}"
        self.text_box_4.text = f"{user_data['users_aadhar']}"
        self.text_box_5.text = f"{user_data['users_username']}"
        self.text_box_6.text = f"{user_data['users_address']}"



    def button_11_click(self, **event_args):
        if not self.edit_mode:
            # Toggle to edit mode
            self.edit_mode = True
            self.toggle_edit_mode_components()
        else:
            # Save changes and toggle back to view mode
            user_data = app_tables.wallet_users.get(users_phone=self.user['users_phone'])
            count=0
            
            phone_number= self.text_box_2.text
            if self.validate_phone_number(phone_number):
                  count=count+1
            aadhar_card = self.text_box_4.text
            if len(str(aadhar_card)) == 12:
                  count=count+1 
            converted_text = self.text_box_3.text 
            if self.is_pan_card_detail(converted_text):
                  count=count+1
                   
            if user_data is not None and count==3:
              user_data['users_email'] = self.text_box_1.text
              user_data['users_phone'] = self.text_box_2.text
              user_data['users_aadhar'] = self.text_box_4.text
              user_data['users_pan']= self.text_box_3.text
              user_data['users_address'] = self.text_box_6.text
              user_data['users_username'] = self.text_box_5.text
                
              alert("User details updated successfully.", title="Success")
            else:
              alert("Please check the entered details to proceed")

            # Toggle back to view mode
            self.edit_mode = False
            self.display_user_profile(self.user)
            self.button_11.text = "Edit" if not self.edit_mode else "Save"
      
    def validate_phone_number(self, phone_number):
      pattern = r'^[6-9]\d{9}$'
      if re.match(pattern, str(phone_number)):
        return True  
      else:
        return False    # Remove leading/trailing whitespace
        
    def is_pan_card_detail(self, text):
        if (
            len(text) == 10 and
            text[:5].isalpha() and
            text[5:9].isdigit() and
            text[9].isalpha()
        ):
          return True
        else:
          return False

    def text_box_3_change(self, **event_args):
      current_text = self.text_box_3.text
      converted_text = current_text.upper()
      self.text_box_3.text = converted_text

    def text_box_2_pressed_enter(self, **event_args):
      phone_number = self.text_box_2.text.strip()

    def button_2_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("Reset_password",user=self.user)

    def link_3_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer.transactions",user=self.user)

    def link_4_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer.transfer",user=self.user)

    def link_7_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer.service",user=self.user)

    def link_13_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("Home",user=self.user,password=self.password)

    def link_1_click(self, **event_args):
      """This method is called when the link is clicked"""
      open_form("customer",user=self.user,password=self.password)


    def file_loader_1_change(self, file, **event_args):
      """This method is called when a new file is loaded into this FileLoader"""
      uploaded_file = self.file_loader_1.file
      print(uploaded_file)
      self.file_loader_1.text = ''
      if uploaded_file:
          # Check if the file is an image by inspecting the content type or file extension
          if uploaded_file.content_type.startswith("image/"):
            resized_image = anvil.server.call('resizing_image',uploaded_file)
            user_data = app_tables.wallet_users.get(users_phone=self.user['users_phone'])
            user_data.update(users_profile_pic=resized_image['media_obj'])
            
            self.image_1.source=resized_image['media_obj']
            
            # print(f"Uploaded image: {uploaded_file.name}")
          else:
            print("Uploaded file is not an image.")

    def check_profile_pic(self):
      print(self.user,self.password)
      print(self.user['users_email'],type(self.user['users_email']))
      user_data = app_tables.wallet_users.get(users_email=str(self.user['users_email'])) #changed
      if user_data:
        existing_img = user_data['users_profile_pic']
        if existing_img != None:
          self.image_1.source = existing_img
        else: 
          print('no pic')
      else:
        print('none')
        
    def button_3_click(self, **event_args):
      """This method is called when the button is clicked"""
      if self.user['users_profile_pic'] != None:
        user_data = app_tables.wallet_users.get(users_phone=self.user['users_phone'])
        user_data.update(users_profile_pic=None)
        self.image_1.source = '_/theme/account.png'

    def text_box_5_pressed_enter(self, **event_args):
      """This method is called when the user presses Enter in this text box"""
      pass

    def text_box_3_pressed_enter(self, **event_args):
      """This method is called when the user presses Enter in this text box"""
      pass

    def button_1_click(self, **event_args):
      """This method is called when the link is clicked"""
      pass

    def link_2_click(self, **event_args):
      open_form('customer.walletbalance',user=self.user,password=self.password)

    def link_10_click(self, **event_args):
      open_form('customer.deposit',user=self.user)

    def link_5_click(self, **event_args):
      open_form('customer.withdraw',user=self.user)

    def link_6_click(self, **event_args):
      open_form('customer.auto_topup',user=self.user)

    def link_8_click(self, **event_args):
      open_form('customer.settings',user=self.user)
