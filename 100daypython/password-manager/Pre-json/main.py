from tkinter import *
from tkinter import messagebox
import random
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
def add_pw():

    with open("data.txt", "r") as file:
        data_lines = file.read().split("\n")
        data = {}
        for line in data_lines:
            if "|" in line:
                split_line = line.split(" | ")
                data[split_line[0]] = (split_line[1], split_line[2])

    if web_input.get() in data:
        user_input.delete(0, END)
        passw_input.delete(0, END)
        user_input.insert(0, data[web_input.get()][0])
        passw_input.insert(0, data[web_input.get()][1])
        messagebox.showinfo(title="Get Credentials", message="Credentials Found")
    elif web_input.get() != "" and user_input.get() != "" and passw_input.get() != "":
        with open("data.txt", "a") as update:
            update.write(f"\n{web_input.get()} | {user_input.get()} | {passw_input.get()}")
        user_input.delete(0, END)
        passw_input.delete(0, END)
        messagebox.showinfo(title="Save", message="Credentials Saved")
    else:
        messagebox.showinfo(title="Invalid Inputs", message="No Credientials Found\nIf adding: Entry box/boxes left blank")

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
web_input = Entry(width=40)
web_input.grid(row=2, column=1, columnspan=2)

user_input = Entry(width=40)
user_input.grid(row=3, column=1, columnspan=2)

passw_input = Entry(width=22)
passw_input.grid(row=4, column=1)

#buttons
gen_pass_button = Button(text="Generate Password", command=gen_pass)
gen_pass_button.grid(row=4, column=2)

add_button = Button(text="Get Credentials or Add Password", command=add_pw, width = 37)
add_button.grid(row=5, column=1, columnspan=2)

window.mainloop()
