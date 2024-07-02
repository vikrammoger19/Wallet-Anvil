from ._anvil_designer import signupTemplate
from anvil import *
import anvil.facebook.auth
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import re

class signup(signupTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.card_4.visible = False
    self.phone_card.visible = False
    self.aadhar_card.visible = False
    self.pan_card.visible= False 
    self.pass_card.visible = False 

  def text_box_8_change(self, **event_args):
    # Convert the text in text_box_8 to uppercase as user types
    self.text_box_8.text = self.text_box_8.text.upper()

  def link_1_click(self, **event_args):
    open_form('login')

  def primary_color_1_click(self, **event_args):
    existing_user = anvil.server.call('get_user_by_phone', str(self.text_box_3.text).strip())

    if existing_user:
        self.card_4.visible = True
        self.text_box_3.text = ''
    else:
        count = 0
        phone_number = str(self.text_box_3.text).strip()
        if self.validate_phone_number(phone_number):
            count += 1
            self.label_15.text = "Phone number is correct"
            self.label_15.foreground = "#008000"
        else:
            self.phone_card.visible = True
            self.label_15.text = "Invalid Phone Number"
            self.label_15.foreground = "#990000"
            self.text_box_3.text = ''
            self.text_box_3.focus()

        aadhar = self.text_box_7.text.strip()
        if aadhar.isdigit() and len(aadhar) == 12:
            count += 1
            self.label_16.text = "Aadhar details correct"
            self.label_16.foreground = "#008000"
        else:
            self.aadhar_card.visible = True
            self.label_16.text = "Please verify the entered Aadhar details"
            self.label_16.foreground = "#990000"
            self.text_box_7.text = ''
            self.text_box_7.focus()

        pan = self.text_box_8.text.strip().upper()
        if self.is_pan_card_detail(pan):
            count += 1
            self.label_14.text = "Pan card is valid"
            self.label_14.foreground = "#008000"
        else:
            self.pan_card.visible = True
            self.label_14.text = "Please verify the entered pan card details"
            self.label_14.foreground = "#990000"
            self.text_box_8.text = ''
            self.text_box_8.focus()

        password = self.text_box_5.text.strip()
        if self.validate_password(password):
            self.label_17.text = "Password meets criteria"
            self.label_17.foreground = "#008000"
            if password == self.text_box_6.text.strip():
                count += 1
            else:
                self.pass_card.visible = True
                self.label_17.text = "Passwords don't match"
                self.label_17.foreground = "#990000"
                self.text_box_5.text = ''
                self.text_box_5.focus()
                self.text_box_6.text = ''
                self.text_box_6.focus()
        else:
            self.pass_card.visible = True
            self.label_17.text = "Password must have at least 1 number, 1 character, 1 symbol, and be at least 8 characters long."
            self.label_17.foreground = "#990000"
            self.text_box_5.text = ''
            self.text_box_6.text = ''
            self.text_box_5.focus()

        # Check for empty fields and set placeholder text
        self.check_empty_fields()

        # Proceed with account creation if all validations pass
        if count == 5:
            anvil.server.call(
                'add_info',
                self.text_box_1.text.strip(),
                self.text_box_2.text.strip(),
                self.drop_down_1.selected_value,
                phone_number,
                aadhar,
                pan,
                self.text_box_6.text.strip()
            )
            alert("Thank you " + self.text_box_1.text.strip() + ", for signing up! Your account has been successfully created")
            open_form('login')

  def check_empty_fields(self):
    fields = [
        (self.text_box_1, 'First Name'),
        (self.text_box_2, 'Last Name'),
        (self.text_box_3, 'Phone Number'),
        (self.text_box_7, 'Aadhar Number'),
        (self.text_box_8, 'PAN Card'),
        (self.text_box_5, 'Password'),
        (self.text_box_6, 'Confirm Password')
    ]

    for field, placeholder in fields:
        if not field.text.strip():
            field.placeholder = f"* {placeholder}"
            field.foreground = "#FF0000"  # Set text color to red

  def link_1_click(self, **event_args):
    open_form('Home')

  def is_pan_card_detail(self, text):
    return len(text) == 10 and text[:5].isalpha() and text[5:9].isdigit() and text[9].isalpha()

  def validate_phone_number(self, phone_number):
    pattern = r'^[6-9]\d{9}$'
    return bool(re.match(pattern, phone_number))

  def validate_password(self, password):
    pattern = r'^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    return bool(re.match(pattern, password))

  def button_1_click(self, **event_args):
    user_email = self.text_box_2.text
    
    # Check if the email exists in the database
    matching_users = app_tables.wallet_users.search(users_email=user_email)
    
    if matching_users:
        # Email exists, generate OTP (Commented out to skip OTP generation)
        # otp = anvil.server.call('generate_otp')
        
        # Call the server function to send OTP via email (Commented out to skip sending OTP)
        # anvil.server.call('send_otp_email', user_email, otp)
        
        # Inform the user that the OTP has been sent (Commented out to skip OTP alert)
        # alert("OTP has been sent to your email.")
        
        # Hide text_box_2 and label_4, and show text_box_9 (Commented out to skip OTP entry)
        # self.text_box_9.visible = True
        # self.label_3.visible = True
        alert("Email verified successfully. Please proceed with the registration.")
        
    else:
        # Email doesn't exist, display an error message
        alert("Email not found. Please enter a valid email address.")

  def text_box_9_pressed_enter(self, **event_args):
    # Skip OTP validation
    # otp_entered = self.text_box_9.text.strip()
    # if anvil.server.call('verify_otp', otp_entered):
    #     self.label_3.text = "OTP validation successful."
    #     self.label_3.foreground = "#008000"  # Green color
    # else:
    #     self.label_3.text = "Invalid OTP. Please try again."
    #     self.label_3.foreground = "#FF0000"  # Red color

    # Hide text_box_9 and proceed with account creation
    # self.text_box_9.visible = False
    # self.label_3.visible = False
    self.label_3.text = "OTP validation skipped."
    self.label_3.foreground = "#008000"  # Green color
