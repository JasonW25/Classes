from tkinter import *
from tkinter import messagebox
import random
import json

# import pyperclip

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def gen_pass():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    pass_letters = [random.choice(letters) for _ in range(nr_letters)]
    pass_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    pass_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = pass_letters + pass_numbers + pass_symbols
    random.shuffle(password_list)

    password = "".join(password_list)

    passw_input.delete(0, END)
    passw_input.insert(0, password)
    # pyperclip.copy(password)
# ---------------------------- SAVE PASSWORD ------------------------------- #
def check():

    try:
        with open("data.json", "r") as file:
            data = json.load(file)

    except FileNotFoundError:
         messagebox.showinfo(title="Get Credentials", message="No Credentials Found")

    else:
        if web_input.get() in data:
            user_input.delete(0, END)
            passw_input.delete(0, END)
            user_input.insert(0, data[web_input.get()]["email"])
            passw_input.insert(0, data[web_input.get()]["password"])
            messagebox.showinfo(title="Get Credentials", message="Credentials Found")
        else:
            messagebox.showinfo(title="Get Credentials", message="No Credentials Found")

def add_pw():
    if web_input.get() != "" and user_input.get() != "" and passw_input.get() != "":
        new_data = {
                web_input.get(): {
                    "email": user_input.get(),
                    "password": passw_input.get()
                    }
                }
        try:
            with open("data.json", "r") as update:
                data = json.load(update)    
                data.update(new_data)

            with open("data.json", "w") as update:
                json.dump(data, update, indent=4)
        except FileNotFoundError:
            with open("data.json", "w") as update:
                json.dump(new_data, update, indent=4)
        finally:
            user_input.delete(0, END)
            passw_input.delete(0, END)
            messagebox.showinfo(title="Save", message="Credentials Saved")
    else:
        messagebox.showinfo(title="Invalid Inputs", message="Entry box/boxes left blank")

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20, bg="white")

#image
lock_img = PhotoImage(file="logo.png")
canvas = Canvas(width=200, height=200, bg="white", highlightthickness=0,)
canvas.create_image(100, 100, image=lock_img)
canvas.grid(row=1, column=1)

#labels
web_label = Label(text="Website", bg="white")
web_label.grid(row=2, column=0)

user_label = Label(text="Username/Email", bg="white")
user_label.grid(row=3, column=0)

passw_label = Label(text="Password", bg="white")
passw_label.grid(row=4, column=0)

#input boxes
web_input = Entry(width=22)
web_input.grid(row=2, column=1)

user_input = Entry(width=40)
user_input.grid(row=3, column=1, columnspan=2)

passw_input = Entry(width=22)
passw_input.grid(row=4, column=1)

#buttons
check_button = Button(text="Check", command=check, width=15)
check_button.grid(row=2, column=2)

gen_pass_button = Button(text="Generate Password", command=gen_pass)
gen_pass_button.grid(row=4, column=2)

add_button = Button(text="Add Credentials", command=add_pw, width = 37)
add_button.grid(row=5, column=1, columnspan=2)

window.mainloop()
