#cSpell:disable
'''
A password manager app in a tkinter GUI interface
'''

from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle, sample
import pyperclip, json


FONT = ('Arial', 10, 'normal')

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+', '?', '^', '-', '~']

    password_list = [char for char in sample(letters, randint(8, 10))]
    password_list += [char for char in sample(numbers, randint(2, 4))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]

    shuffle(password_list)

    password = ''.join(password_list)
    password_entry.insert(0, password)

    # copies the password to the clipboard
    pyperclip.copy(password)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_all():
    ''' Saves login information in a json file'''
    
    # save data entered
    website = website_entry.get()
    username = info_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            'email': username,
            'password': password
        }
    }
    
    # check all entries exist
    if len(website) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showerror(title= 'Error', icon='warning', message='Please fill in all entries')

    else:
        # confirmation before saving (output is boolean)
        is_ok = messagebox.askokcancel(title='Save info', message=f'These are the details entered:\nWebsite: {website}\nEmail: {username} \nPassword: {password} \n\nProceed to save?')

        # save data in json file
        if is_ok:
            try:
                # open the json file and read existing data into a dictionary
                with open('data.json', 'r') as f:
                    data = json.load(f)

            except FileNotFoundError:
                # create a new json file and add new data
                with open('data.json', 'w') as f:
                    json.dump(new_data, f, indent=4)

            else:
                # add new data to the dictionary 
                data.update(new_data)

                # save the new data to the json file
                with open('data.json', 'w') as f:
                    json.dump(data, f, indent=4)

            finally:
                # clear entry for new information
                website_entry.delete(0, END)
                password_entry.delete(0, END)
                info_entry.delete(0, END)

# ---------------------------- UI SETUP ------------------------------- #
def find_password():
    ''' Finds an entry in the password database and returns it'''
    
    try:
        # read in the password database
        with open('data.json', 'r') as f:
            data = json.load(f)

        # search and display website info if available
        info = data[website_entry.get().lower()]
        messagebox.showinfo(title=website_entry.get(), message=f"Email/Username: {info['email']}\nPassword: {info['password']}")

    except FileNotFoundError:
        messagebox.showerror(title='Error', message='No data file found')

    except KeyError:
        messagebox.showerror(title='Error', message=f'No details for {website_entry.get()} exists')


# ---------------------------- SEARCH DATA ---------------------------- #
window = Tk()
window.title('Password Manager')
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo = PhotoImage(file='appImages/logo.png')
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

# labels
website_label = Label(text='Website:', font=FONT)
website_label.grid(column=0, row=1)

info_label = Label(text= 'Email/Username:', font=FONT)
info_label.grid(column=0, row=2)

password_label = Label(text='Password:', font=FONT)
password_label.grid(column=0, row=3)

# entries
website_entry = Entry(width=54)
website_entry.focus()
website_entry.grid(column=1, row=1, columnspan=2)

info_entry = Entry(width=54)
info_entry.grid(column=1, row=2, columnspan=2)

password_entry = Entry(width=33)
password_entry.grid(column=1, row=3)

# buttons
password_button = Button(command=generate_password)
password_button.config(text='Generate Password', font=FONT)
password_button.grid(column=2, row=3)

add_button = Button(width=40, command=save_all)
add_button.config(text='Add', font=FONT)
add_button.grid(column=1, row=4, columnspan=2)

search_button = Button(width=14, command=find_password)
search_button.config(text='Search', font=FONT)
search_button.grid(column=2, row=1)


window.mainloop()