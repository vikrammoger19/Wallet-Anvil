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
import anvil.http

class signup(signupTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)
        self.card_4.visible = False
        self.phone_card.visible = False
        self.aadhar_card.visible = False
        self.pan_card.visible = False
        self.pass_card.visible = False
        self.populate_country_dropdown()
        self.otp = None

    def populate_country_dropdown(self):
        # Retrieve countries from wallet_admins_add_currency table
        countries = [row['admins_add_currency_country'] for row in app_tables.wallet_admins_add_currency.search()]
        
        # Set items to drop_down_1
        self.drop_down_1.items = countries
        

    def primary_color_1_click(self, **event_args):
        # Check if phone number exists
        existing_user = anvil.server.call('get_user_by_phone', str(self.text_box_3.text).strip())
        if existing_user:
            self.card_4.visible = True
            self.text_box_3.text = ''
        else:
            # Validate email
            user_email = self.text_box_2.text.strip()
            if self.check_email_exists(user_email):
                alert("Email is already in use. Please use a different email.")
            else:
                # Validate other fields
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

                aadhar = str(self.text_box_7.text).strip()
                if len(aadhar) == 12 and aadhar.isdigit():
                    count += 1
                    self.label_16.text = "Aadhar details correct"
                    self.label_16.foreground = "#008000"
                else:
                    self.aadhar_card.visible = True
                    self.label_16.text = "Please verify the entered Aadhar details"
                    self.label_16.foreground = "#990000"
                    self.text_box_7.text = ''
                    self.text_box_7.focus()

                converted_text = self.text_box_8.text.strip().upper()
                if self.is_pan_card_detail(converted_text):
                    self.label_14.text = "Pan card is valid"
                    self.label_14.foreground = "#008000"
                    count += 1
                else:
                    self.pan_card.visible = True
                    self.label_14.text = "Please verify the entered pan card details"
                    self.label_14.foreground = "#990000"
                    self.text_box_8.text = ''
                    self.text_box_8.focus()

                password = self.text_box_5.text
                if self.validate_password(password):
                    count += 1
                    self.label_17.text = "Password meets criteria"
                    self.label_17.foreground = "#008000"

                    if self.text_box_5.text != '' and self.text_box_5.text == self.text_box_6.text:
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

                if self.drop_down_1.selected_value:
                    country_name = self.drop_down_1.selected_value
                    currency = self.get_currency_by_country(country_name)
                    count += 1
                else:
                    self.label_4.text = "Please select a country"
                    self.label_4.visible = True

                if count == 6:
                    # Proceed with signup
                    anvil.server.call(
                        'add_info',
                        self.text_box_1.text.strip(),
                        user_email,
                        self.drop_down_1.selected_value,
                        phone_number,
                        aadhar,
                        converted_text,
                        self.text_box_6.text.strip(),
                        currency
                    )
                    alert(f"Thank you {self.text_box_1.text.strip()}, for signing up! Your account has been successfully created.")
                    open_form('login')

    def get_currency_by_country(self, country_name):
        url = f"https://restcountries.com/v3.1/name/{country_name}"
        response = anvil.http.request(url, method="GET", json=True)
        
        if response:
            country_info = response[0]
            currency = list(country_info['currencies'].keys())[0]
            return currency
        else:
            return "Unknown"

    def link_1_click(self, **event_args):
        open_form('Home')

    def text_box_8_change(self, **event_args):
        current_text = self.text_box_8.text
        converted_text = current_text.upper()
        self.text_box_8.text = converted_text
      
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
  
    def validate_button_click(self, **event_args):
        phone_number = str(self.text_box_3.text).strip()  
    
    def validate_phone_number(self, phone_number):
        pattern = r'^[6-9]\d{9}$'
        if re.match(pattern, str(phone_number)):
            return True  
        else:
            return False 
        
    def text_box_9_pressed_enter(self, **event_args):
        # Skip OTP validation
        self.label_3.text = "OTP validation skipped."
        self.label_3.foreground = "#008000"  # Green color
          
    def validate_button_click(self, **event_args):
        password = self.text_box_5.text
        if self.validate_password(password):
            self.label_17.text = "Password is valid"
            self.label_17.foreground = "#008000"
        else:
            self.label_17.text = "Password must have at least 1 number, 1 character, 1 symbol, and be at least 8 characters long."
            self.label_17.foreground = "#FF0000"
  
    def validate_password(self, password):
        pattern = r'^(?=.*[0-9])(?=.*[a-zA-Z])(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
        if re.match(pattern, password):
            return True
        else:
            return False

    def check_email_exists(self, email):
        matching_users = app_tables.wallet_users.search(users_email=email)
        return len(matching_users) > 0

    def button_2_click(self, **event_args):
        """This method is called when the button is clicked"""
        pass
  
    def button_1_click(self, **event_args):
        user_email = self.text_box_2.text
        if self.check_email_exists(user_email):
            alert("Email is already in use. Please use a different email.")
        else:
            self.otp = self.send_otp_to_email(user_email)
            alert("OTP has been sent to your email.")
          
    def send_otp_to_email(self, email):
        import random
        otp = random.randint(100000, 999999)
        # Send email using Anvil's email service
        anvil.email.send(to=email,
                         subject="Your OTP Code",
                         text=f"Your OTP code is {otp}.")
        return otp

    def verify_button_click(self, **event_args):
        entered_otp = self.text_box_9.text.strip()
        if entered_otp == str(self.otp):
            alert("OTP verified successfully!")
            # Proceed with account creation or next step
        else:
            alert("Invalid OTP. Please try again.")
