from tkinter import *  # GUI
from tkinter import messagebox  # popups
from random import randint, choice, shuffle
import pyperclip  # adiciona um texto na área de transferência
import json  # Usa e cria API's json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
letters = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v",
           "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R",
           "S", "T", "U", "V", "W", "X", "Y", "Z"]
numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
symbols = ["!", "@", "#", "$", "%", "&", "*", "(", ")", "_", "-", "<", ">", ".", "+"]


def password_generator():
    if len(password_entry.get()) == 0:
        new_password_list = [choice(letters) for _ in range(randint(8, 10))]
        new_password_list += [choice(numbers) for _ in range(randint(2, 4))]
        new_password_list += [choice(symbols) for _ in range(randint(2, 4))]

        shuffle(new_password_list)

        new_password = "".join(new_password_list)
        password_entry.insert(0, new_password)
        pyperclip.copy(text=new_password)  # adiciona a senha na área de transferência


# ---------------------------- SAVE DATA ------------------------------- #


def save_data():
    name = name_entry.get().strip().capitalize()
    email = email_entry.get().strip()
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    new_data = {name: {
        "Name": name,
        "Email": email,
        "User": username,
        "Password": password,
    }}

    if len(name) == 0 or len(email) == 0 or len(username) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty")
    else:
        try:
            with open("data.json", mode="r") as file:
                # Reading old data
                data = json.load(file)
        except FileNotFoundError:
            with open("data.json", mode="w") as file:
                # Save updated data
                json.dump(new_data, file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open("data.json", mode="w") as file:
                # Save updated data
                json.dump(data, file, indent=4)
        finally:
            name_entry.delete(0, END)
            email_entry.delete(0, END)
            username_entry.delete(0, END)
            password_entry.delete(0, END)
            email_entry.insert(0, "example@mail.com")  # Texto padrão
            username_entry.insert(0, "None")
            name_entry.focus()


# -------------------------- SAVE PASSWORD ----------------------------- #
def search():
    try:
        with open("data.json", "r") as file:
            search_file = json.load(file)
            search_data = name_entry.get().capitalize()
            search_name = search_file[search_data]["Name"]
            search_user = search_file[search_data]["User"]
            search_email = search_file[search_data]["Email"]
            search_password = search_file[search_data]["Password"]
    except KeyError:
        if len(search_data) == 0:
            messagebox.showinfo(title="Oops", message="Empty Field")
        else:
            messagebox.showinfo(title="Oops", message=f"Website '{search_data}' Not Found")
    except FileNotFoundError:
        messagebox.showinfo(title="Oops", message="No data registered")
    else:
        pyperclip.copy(search_password)
        messagebox.showinfo(title=search_data, message=f"Name: {search_name}\nEmail: {search_email}"
                                                       f"\nUser: {search_user}\nPassword: {search_password}\n\npassword copied!")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title('Password Manager')
window.config(padx=50, pady=20)

# Logo
img_logo = PhotoImage(file='logo.png')
canvas = Canvas(width=200, height=200)
canvas.create_image(80, 100, image=img_logo)
canvas.grid(row=0, column=1, columnspan=2, sticky="we")  # "sticky" Posição do elemento na coluna (pontos cardeais)

# Labels
name_text = Label(text='Name:')
name_text.grid(row=1, column=0)
email_text = Label(text='Email:')
email_text.grid(row=2, column=0)
username_text = Label(text='Username:')
username_text.grid(row=3, column=0)
password_text = Label(text='Password:')
password_text.grid(row=4, column=0)

# Entries
name_entry = Entry(width=21)
name_entry.grid(row=1, column=1, sticky="w")  # columnspan: quantas colunas irá ocupar
name_entry.focus()  # Cursor ficará ativo de início.
email_entry = Entry(width=40)
email_entry.grid(row=2, column=1, columnspan=2, sticky="w")
email_entry.insert(0, "example@mail.com")  # Texto padrão
username_entry = Entry(width=40)
username_entry.grid(row=3, column=1, columnspan=2, sticky="w")
username_entry.insert(0, "None")
password_entry = Entry(width=21)
password_entry.grid(row=4, column=1, sticky="w")

# Buttons
search_button = Button(text='Search', width=14, command=search)
search_button.grid(row=1, column=1, columnspan=2, sticky="e")
password_generate_button = Button(text='Generate Password', width=14, command=password_generator)
password_generate_button.grid(row=4, column=1, columnspan=2, sticky="e")
add_button = Button(text='Add', width=30, command=save_data)
add_button.grid(row=5, column=1, columnspan=2, sticky="we")

window.mainloop()
