#cSpell:disable
'''
A password manager app in a tkinter GUI interface
'''

from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle, sample
import pyperclip


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
    ''' Saves login information in a txt file'''
    
    # save info entered in entries
    tosave1 = website_entry.get()
    tosave2 = info_entry.get()
    tosave3 = password_entry.get()
    line = f'{tosave1} | {tosave2} | {tosave3}'
    
    # check all entries exist
    if len(tosave1) == 0 or len(tosave2) == 0 or len(tosave3) == 0:
        messagebox.showerror(title= 'oops', icon='warning', message='Please fill in all entries')

    else:
        # confirmation before saving (output is boolean)
        is_ok = messagebox.askokcancel(title='Save info', message=f'These are the details entered:\nWebsite: {tosave1}\nEmail: {tosave2} \nPassword: {tosave3} \n\nProceed to save?')

        # save the line in a txt file
        if is_ok:
            with open('data.txt', 'a') as f:
                f.write(f'{line}\n')

            # clear entry for new information
            website_entry.delete(0, END)
            password_entry.delete(0, END)
            info_entry.delete(0, END)
        
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('Password Manager')
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo = PhotoImage(file='logo.png')
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




window.mainloop()