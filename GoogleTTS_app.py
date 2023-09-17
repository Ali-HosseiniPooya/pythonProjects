from tkinter import *
from tkinter import messagebox
from gtts import gTTS
import enchant
import requests

# Settings
root = Tk()
root.geometry('500x200')
root.title('Google Text-To-Speech (en-US)')
root.resizable(width=False, height=False)
color = 'light pink'
root.configure(bg=color)

# Variables
userInput = StringVar()

# Frames
top_first = Frame(root, width=500, height=100, bg=color)
top_first.pack(side=TOP)
top_second = Frame(root, width=500, height=100, bg=color)
top_second.pack(side=BOTTOM)

# Functions
def check_connection():
    try:
        requests.get('https://www.google.com/')
    except:
        raise requests.HTTPError

def check_box():
   messagebox.askquestion("Warning","Do you want to continue?", icon ='warning')

def check_lang(text):
     dictionary = enchant.Dict("en_US")
     if (not dictionary.check(text)):
          raise Exception()

def convert(textInput):
    userTextInput = textInput.get()
    check_box()

    try:
        check_lang(userTextInput)
        check_connection() 
        obj = gTTS(text = userTextInput, lang = 'en', tld = 'us', slow = False)
        obj.save('GoogleTTS_file.mp3')

    except requests.HTTPError:
        messagebox.showerror("Connection Error", "No internet connection.")

    except ValueError:
        messagebox.showerror("Invalid input", "The textbox is empty!")

    except Exception:
        messagebox.showerror("Invalid language", "The text language isn't English\nor maybe you are misspelled!")
   
# Buttons
btn_start = Button(top_second, text="Convert", width=20,
    highlightbackground=color, command = lambda: convert(userInput)).pack(side=LEFT, padx=10, pady=40)

# Labels and entries
Label(top_first, text="Text:", bg=color).pack(side=LEFT, pady=40, padx=5)
Entry(top_first,width=60, highlightbackground=color, textvariable=userInput).pack(side=LEFT)

root.mainloop()