from twilio.rest import Client
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.core.audio import SoundLoader 

#from kivymd.app import MDApp
#from kivymd.vix.label import MDLabel
#from kivymd.vix.screen import Screen

import sqlite3
import random
from sqlite3 import Error
# import mysql.connector
from kivy.properties import StringProperty
import pandas as pd
import numpy as np
from database import *
#from kivyauth.google_auth import initialize_google, login_google, logout_google

grate_list = list()

class Welcome(Screen):
    pass

class About(Screen):
    pass

class Create(Screen):

    firstname = ObjectProperty(None)
    lastname = ObjectProperty(None)
    phone = ObjectProperty(None)
    username = ObjectProperty(None)
    password = ObjectProperty(None)
    passwordCheck = ObjectProperty(None)
    
    def submit(self):
        """make this function check password congruency, ensure necessary spaces are filled in,
        and username/phone number isn't already in use"""
        firstname = self.firstname.text
        lastname = self.lastname.text
        phoneNum = self.phone.text
        username = self.username.text
        password = self.password.text
        passwordCheck = self.passwordCheck.text

        if (phoneNum != "") and (username != "") and (password != ""):
            for index, row in df_main.iterrows():
                if (username not in row['username']):
                    if (phoneNum not in row['phonenumber']) and (len(phoneNum) == 10) and phoneNum.isdigit(): 
                        if (password == passwordCheck):
                            #update_main(username, password, firstname, lastname, phoneNum)
                            df_main.loc[len(df_main), 'firstname'] = firstname
                            df_main.loc[len(df_main)-1, 'lastname'] = lastname
                            df_main.loc[len(df_main)-1, 'phonenumber'] = phoneNum
                            df_main.loc[len(df_main)-1, 'username'] = username
                            df_main.loc[len(df_main)-1, 'password'] = password
                            self.reset()
                        else:
                            pass_match()
                    else:
                        num_invalid()

        else:
            empty_input()
        
        confirm_loc_serv()
    
    def reset(self):
        self.firstname.text = ""
        self.lastname.text = ""
        self.phone.text = ""
        self.username.text = ""
        self.password.text = ""
        self.passwordCheck.text = ""
    


class Login(Screen):
    
    username = ObjectProperty(None)
    password = ObjectProperty(None)

    def submit(self):
        confirm_loc_serv()
        username = self.username.text
        password = self.password.text
        for index, row in df_main.iterrows():
            if username == row['username']:
                if df_main.loc[index, 'password']:
                    #lets you go to menu
                    self.reset()
                else:
                    show_invalid()
            else:
                show_invalid()

    def reset(self):
        self.username.text = ""
        self.password.text = ""


class Menu(Screen):
    pass

class Evaluation(Screen):
    yes_count = NumericProperty(0)
    def yes(self):
        self.yes_count += 1
    def submit(self):
        show_success()
        if self.yes_count > 0:
            show_covid_message()
            self.reset()
    def reset(self):
        self.yes_count = 0


class PhysicalGame(Screen):
    pass

class Cardio(Screen):
    pass

class HIIT(Screen):
    pass

class Core(Screen):
    pass

class Strength(Screen):
    pass

class Sport(Screen):
    def sportplace(self):
        show_sportplace_message

class Yoga(Screen):
    pass

class Dance(Screen):
    def spotify(self):
        show_spotify_message()
    def youtube(self):
        show_youtube_message()

class PhysicalEval(Screen):
    grateful = ObjectProperty(None)
    def submitaches(self):
        show_ache_message()
    def submitback(self):
        show_back_message()
    def submitfat(self):
        show_fat_message()
    def submitsore(self):
        show_sore_message()
    def submitstood(self):
        show_stood_message()
    def submitmove(self):
        show_move_message()
    def submitdep(self):
        show_dep_message()
    def submitenergy(self):
        show_energy_message()
    def submitscreen(self):
        show_screen_message()
    def submit_all(self):
        grateful = self.ids.grateful.text
        show_success()
        self.reset()
    def reset(self):
        grate_list.append(self.grateful.text)
        print(grate_list)
        self.grateful.text = ""

class GrateLog(Screen):
    pass

class MentalGame(Screen):
    def play_sound_rainforest(self): 
        sound = SoundLoader.load('rainforest.m4a') 
        if sound: 
            sound.play()
    def open_calm(self):
        show_calm_message()         

class Food(Screen):
    pass            

class Alert(Screen):
    username = ObjectProperty(None)
    def redbtn(self):
        show_success()
        username = self.username.text
        for index, row in df_user.iterrows():
            if username == row['username'] and row['time'] <= 14:
                contact = df_user.loc[index, 'contact']
                for index, row in df_main.iterrows():
                    if contact == row['username']:
                        send_text(df_main.loc[index, 'phonenumber'])

class WindowManager(ScreenManager):
    pass

def show_invalid():
    """
    Pop-up shown if the login information is incorrect.
    """
    box = BoxLayout(orientation = 'vertical', padding = (10))
    box.add_widget(Label(text = "The username you inputted either does \nnot exist in out database or the pass\n word you inputted is incorrect."))
    btn1 = Button(text = "Ok")
    box.add_widget(btn1)
    popup = Popup(title="Invalid Login", title_size= (30), title_align = 'center', content = box,size_hint=(None, None), size=(430, 200), auto_dismiss = True)
    btn1.bind(on_press = popup.dismiss)
    popup.open()

def show_success():
    """
    Pop-up shown if action successfully completed.
    """
    box = BoxLayout(orientation = 'vertical', padding = (10))
    box.add_widget(Label(text = ""))
    btn1 = Button(text = "Ok")
    box.add_widget(btn1)
    popup = Popup(title="Action Successful", title_size= (30), title_align = 'center', content = box,size_hint=(None, None), size=(430, 200), auto_dismiss = True)
    btn1.bind(on_press = popup.dismiss)
    popup.open()

def user_taken():
    """
    Pop-up shown if the username inputted in the 
    create account window is already in use.
    """
    box = BoxLayout(orientation = 'vertical', padding = (10))
    box.add_widget(Label(text = "That username is already in use.\nPlease try another."))
    btn1 = Button(text = "Ok")
    box.add_widget(btn1)
    popup = Popup(title="Username Error", title_size= (30), title_align = 'center', content = box,size_hint=(None, None), size=(430, 200), auto_dismiss = True)
    btn1.bind(on_press = popup.dismiss)
    popup.open()

def num_invalid():
    """
    Pop-up shown if the number inputted in the 
    create account window is already in use.
    """
    box = BoxLayout(orientation = 'vertical', padding = (10))
    box.add_widget(Label(text = "The phone number you inputted is either already in use or\nit is invalid. Do you already have an account?\nIf not please ensure the number inputted is correct."))
    btn1 = Button(text = "Ok")
    box.add_widget(btn1)
    popup = Popup(title="Phone Number Input Invalid", title_size= (30), title_align = 'center', content = box,size_hint=(None, None), size=(430, 200), auto_dismiss = True)
    btn1.bind(on_press = popup.dismiss)
    popup.open()

def pass_match():
    """
    Pop-up shown if the passwords inputted in the 
    create account window do not match.
    """
    box = BoxLayout(orientation = 'vertical', padding = (10))
    box.add_widget(Label(text = "The passwords inputted do not match.\nPlease ensure that they match."))
    btn1 = Button(text = "Ok")
    box.add_widget(btn1)
    popup = Popup(title="Password Error", title_size= (30), title_align = 'center', content = box,size_hint=(None, None), size=(430, 200), auto_dismiss = True)
    btn1.bind(on_press = popup.dismiss)
    popup.open()

def empty_input():
    """
    Pop-up shown if the passwords inputted in the 
    create account window do not match.
    """
    box = BoxLayout(orientation = 'vertical', padding = (10))
    box.add_widget(Label(text = "You left required spaces blank. Please make\nsure to input a username, phone number, and\npassword."))
    btn1 = Button(text = "Ok")
    box.add_widget(btn1)
    popup = Popup(title="Empty Input Error", title_size= (30), title_align = 'center', content = box,size_hint=(None, None), size=(430, 200), auto_dismiss = True)
    btn1.bind(on_press = popup.dismiss)
    popup.open()

def show_covid_message():
    """
    Pop-up shown if the user clicks yes to any symptom to say they shoud get tested for covid
    """
    box = BoxLayout(orientation = 'vertical', padding = (10))
    box.add_widget(Label(text = "You should get tested for Covid-19"))
    btn1 = Button(text = "Ok")
    box.add_widget(btn1)
    popup = Popup(title="Covid Notification", title_size= (30), title_align = 'center', content = box,size_hint=(None, None), size=(430, 200), auto_dismiss = True)
    btn1.bind(on_press = popup.dismiss)
    popup.open()

def show_ache_message():
    """
    Pop-up shown if the user clicks yes to any symptom to take care of their physical health - motivates to get moving
    """
    box = BoxLayout(orientation = 'vertical', padding = (10))
    box.add_widget(Label(text = "You should move more"))
    box.add_widget(Label(text = "Try going for a walk"))
    btn1 = Button(text = "Ok")
    box.add_widget(btn1)
    popup = Popup(title="Wellness Notification", title_size= (30), title_align = 'center', content = box,size_hint=(None, None), size=(430, 200), auto_dismiss = True)
    btn1.bind(on_press = popup.dismiss)
    popup.open()

def show_back_message():
    """
    Pop-up shown if the user clicks yes to any symptom to take care of their physical health - motivates to get moving
    """
    box = BoxLayout(orientation = 'vertical', padding = (10))
    box.add_widget(Label(text = "Do the Yoga in our fitness section"))
    btn1 = Button(text = "Ok")
    box.add_widget(btn1)
    popup = Popup(title="Wellness Notification", title_size= (30), title_align = 'center', content = box,size_hint=(None, None), size=(430, 200), auto_dismiss = True)
    btn1.bind(on_press = popup.dismiss)
    popup.open()

def show_fat_message():
    """
    Pop-up shown if the user clicks yes to any symptom to take care of their physical health - motivates to get moving
    """
    box = BoxLayout(orientation = 'vertical', padding = (10))
    box.add_widget(Label(text = "Drink a five-hour energy"))
    btn1 = Button(text = "Ok")
    box.add_widget(btn1)
    popup = Popup(title="Wellness Notification", title_size= (30), title_align = 'center', content = box,size_hint=(None, None), size=(430, 200), auto_dismiss = True)
    btn1.bind(on_press = popup.dismiss)
    popup.open()

def show_sore_message():
    """
    Pop-up shown if the user clicks yes to any symptom to take care of their physical health - motivates to get moving
    """
    box = BoxLayout(orientation = 'vertical', padding = (10))
    box.add_widget(Label(text = "Not sore enough do another workout"))
    btn1 = Button(text = "Ok")
    box.add_widget(btn1)
    popup = Popup(title="Wellness Notification", title_size= (30), title_align = 'center', content = box,size_hint=(None, None), size=(430, 200), auto_dismiss = True)
    btn1.bind(on_press = popup.dismiss)
    popup.open()

def show_stood_message():
    """
    Pop-up shown if the user clicks yes to any symptom to take care of their physical health - motivates to get moving
    """
    box = BoxLayout(orientation = 'vertical', padding = (10))
    box.add_widget(Label(text = "Why not?"))
    btn1 = Button(text = "Ok")
    box.add_widget(btn1)
    popup = Popup(title="Wellness Notification", title_size= (30), title_align = 'center', content = box,size_hint=(None, None), size=(430, 200), auto_dismiss = True)
    btn1.bind(on_press = popup.dismiss)
    popup.open()

def show_move_message():
    """
    Pop-up shown if the user clicks yes to any symptom to take care of their physical health - motivates to get moving
    """
    box = BoxLayout(orientation = 'vertical', padding = (10))
    box.add_widget(Label(text = "Why not?"))
    btn1 = Button(text = "Ok")
    box.add_widget(btn1)
    popup = Popup(title="Wellness Notification", title_size= (30), title_align = 'center', content = box,size_hint=(None, None), size=(430, 200), auto_dismiss = True)
    btn1.bind(on_press = popup.dismiss)
    popup.open()

def show_dep_message():
    """
    Pop-up shown if the user clicks yes to any symptom to take care of their physical health - motivates to get moving
    """
    box = BoxLayout(orientation = 'vertical', padding = (10))
    box.add_widget(Label(text = "Reach out to a friend"))
    btn1 = Button(text = "Ok")
    box.add_widget(btn1)
    popup = Popup(title="Wellness Notification", title_size= (30), title_align = 'center', content = box,size_hint=(None, None), size=(430, 200), auto_dismiss = True)
    btn1.bind(on_press = popup.dismiss)
    popup.open()

def show_energy_message():
    """
    Pop-up shown if the user clicks yes to any symptom to take care of their physical health - motivates to get moving
    """
    box = BoxLayout(orientation = 'vertical', padding = (10))
    box.add_widget(Label(text = "Makes sense"))
    btn1 = Button(text = "Ok")
    box.add_widget(btn1)
    popup = Popup(title="Wellness Notification", title_size= (30), title_align = 'center', content = box,size_hint=(None, None), size=(430, 200), auto_dismiss = True)
    btn1.bind(on_press = popup.dismiss)
    popup.open()

def show_screen_message():
    """
    Pop-up shown if the user clicks yes to any symptom to take care of their physical health - motivates to get moving
    """
    box = BoxLayout(orientation = 'vertical', padding = (10))
    box.add_widget(Label(text = "Well duh.. same bruh"))
    btn1 = Button(text = "Ok")
    box.add_widget(btn1)
    popup = Popup(title="Wellness Notification", title_size= (30), title_align = 'center', content = box,size_hint=(None, None), size=(430, 200), auto_dismiss = True)
    btn1.bind(on_press = popup.dismiss)
    popup.open()

def show_calm_message():
    """
    Asks the user for permission to open the Calm App
    """
    box = BoxLayout(orientation = 'vertical', padding = (10))
    box.add_widget(Label(text = "Sano Health is asking for permission to open Calm App"))
    btn1 = Button(text = "Allow")
    btn2 = Button(text = "Deny")
    box.add_widget(btn1)
    box.add_widget(btn2)
    popup = Popup(title="Calm Notification", title_size= (30), title_align = 'center', content = box,size_hint=(None, None), size=(430, 200), auto_dismiss = True)
    btn1.bind(on_press = popup.dismiss)
    btn2.bind(on_press = popup.dismiss)
    popup.open()

def show_spotify_message():
    """
    Asks the user for permission to open the Spotify App
    """
    box = BoxLayout(orientation = 'vertical', padding = (10))
    box.add_widget(Label(text = "Sano Health is asking for permission to open Spotify"))
    btn1 = Button(text = "Allow")
    btn2 = Button(text = "Deny")
    box.add_widget(btn1)
    box.add_widget(btn2)
    popup = Popup(title="Spotify Notification", title_size= (30), title_align = 'center', content = box,size_hint=(None, None), size=(430, 200), auto_dismiss = True)
    btn1.bind(on_press = popup.dismiss)
    btn2.bind(on_press = popup.dismiss)
    popup.open()

def confirm_loc_serv():
    """
    notifies user of shared location
    """
    box = BoxLayout(orientation = 'vertical', padding = (10))
    box.add_widget(Label(text = "SanoHealth uses location services for our\ncovid contract-tracing functionality"))
    btn1 = Button(text = "Allow")
    btn2 = Button(text = "Deny")
    box.add_widget(btn1)
    box.add_widget(btn2)
    popup = Popup(title="Location Request", title_size= (30), title_align = 'center', content = box,size_hint=(None, None), size=(430, 200), auto_dismiss = True)
    btn1.bind(on_press = popup.dismiss)
    btn2.bind(on_press = popup.dismiss)
    popup.open()

def show_youtube_message():
    """
    Asks the user for permission to open the Youtube App
    """
    box = BoxLayout(orientation = 'vertical', padding = (10))
    box.add_widget(Label(text = "Sano Health is asking for permission to open Youtube"))
    btn1 = Button(text = "Allow")
    btn2 = Button(text = "Deny")
    box.add_widget(btn1)
    box.add_widget(btn2)
    popup = Popup(title="Youtube Notification", title_size= (30), title_align = 'center', content = box,size_hint=(None, None), size=(430, 200), auto_dismiss = True)
    btn1.bind(on_press = popup.dismiss)
    btn2.bind(on_press = popup.dismiss)
    popup.open()

def show_sportplace_message():
    """
    Asks the user for permission to open the Maps App
    """
    box = BoxLayout(orientation = 'vertical', padding = (10))
    box.add_widget(Label(text = "Sano Health is asking for permission to open Maps"))
    btn1 = Button(text = "Allow")
    btn2 = Button(text = "Deny")
    box.add_widget(btn1)
    box.add_widget(btn2)
    popup = Popup(title="Sports Near You Notification", title_size= (30), title_align = 'center', content = box,size_hint=(None, None), size=(430, 200), auto_dismiss = True)
    btn1.bind(on_press = popup.dismiss)
    btn2.bind(on_press = popup.dismiss)
    popup.open()

def buttonClose(self):
    self.popup.dismiss

def send_text(phoneNum):
    # Your Account SID from twilio.com/console
    account_sid = "<insert>"
    # Your Auth Token from twilio.com/console
    auth_token  = "<insert>"

    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to="+1" + phoneNum,     # replace number with number from database
        from_="<insert>",   # free trial number
        body="Someone you've been in contact with has contracted COVID-19. Please take the necessary health precautions to prevent the spread.")

    print(message.sid)

kv = Builder.load_file("mymain.kv")

class MyMainApp(App):
    def build(self):
        return kv

if __name__ == "__main__":
    MyMainApp().run()