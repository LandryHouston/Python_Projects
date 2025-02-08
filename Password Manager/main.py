from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

FONT_NAME = 'Calibri'

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = ''.join(password_list)
    password_input.delete(0, 'end')
    password_input.insert(0, password)
    pyperclip.copy(password)


def search_password():
    website = website_input.get().lower()
    try:
        with open('passwords.json', 'r') as f:
            data = json.load(f)
            data_lower = {key.lower(): value for key, value in data.items()}
            if website in data_lower:
                # Create a new window to display the credentials
                info_window = Toplevel(window)
                info_window.title(f"{website.capitalize()} Credentials")

                email = data_lower[website]['email']
                password = data_lower[website]['password']

                # Hide the window before positioning
                info_window.withdraw()
                # Wait for window to be fully rendered, then center it
                info_window.update()

                x_pos = (info_window.winfo_screenwidth() // 2) - (info_window.winfo_width() // 2)
                y_pos = (info_window.winfo_screenheight() // 2) - (info_window.winfo_height() // 2)
                # Set the geometry of the window
                info_window.geometry(f'+{x_pos+40}+{y_pos+100}')

                # Show the window after positioning
                info_window.deiconify()

                # Display the information in the new window
                email_label = Label(info_window, text=f"Email/Username: {email}")
                email_label.grid(column=0, row=0, sticky='W', padx=40, pady=(40, 20))

                password_label = Label(info_window, text=f"Password: {password}")
                password_label.grid(column=0, row=1, sticky='W', padx=40, pady=(0, 40))

                copy_email_button = Button(info_window, text="Copy Email", command=lambda: pyperclip.copy(email))
                copy_email_button.grid(column=1, row=0, sticky="EW", padx=(0, 20), pady=(40, 20))

                copy_password_button = Button(info_window, text="Copy Password", command=lambda: pyperclip.copy(password))
                copy_password_button.grid(column=1, row=1, sticky="EW", padx=(0, 20), pady=(0, 40))
            else:
                messagebox.showerror(title="Password Manager", message=f"No credentials for {website} exists.")
    except:
        messagebox.showerror(title="Password Manager", message="No Data File Found")


def export():
    website, email, password = website_input.get(), email_input.get(), password_input.get()
    if not all([website, email, password]):
        messagebox.showerror(title="Password Manager", message="Website, Email, and Password are required fields.")
        return
    
    new_data = {website: {"email": email, "password": password}}
    
    try:
        with open('passwords.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
    
    data.update(new_data)
    
    with open('passwords.json', 'w') as f:
        json.dump(data, f, indent=4)

    website_input.delete(0, END)
    password_input.delete(0, END)
    website_input.focus()
    messagebox.showinfo(title="Password Manager", message="Password saved successfully!")


window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

# Hide the window before positioning
window.withdraw()
# Wait for window to be fully rendered, then center it
window.update()

# Calculate position to center the window
x_pos = (window.winfo_screenwidth() // 2) - (window.winfo_width() // 2)
y_pos = (window.winfo_screenheight() // 2) - (window.winfo_height() // 2)

# Set the geometry of the window
window.geometry(f'+{x_pos}+{y_pos}')

# Show the window after positioning
window.deiconify()

canvas = Canvas(height=200, width=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

website = Label(font=(FONT_NAME, 14))
website.config(text="Website:")
website.grid(column=0, row=1)

email_username = Label(font=(FONT_NAME, 14))
email_username.config(text="Email/Username:")
email_username.grid(column=0, row=2)

password = Label(font=(FONT_NAME, 14))
password.config(text="Password:")
password.grid(column=0, row=3)

website_input = Entry()
website_input.grid(column=1, row=1, sticky="EW", padx=(20, 20))
website_input.focus()

search_button = Button(text="Search", command=search_password)
search_button.grid(column=2, row=1, sticky="EW", padx=(0, 40))

email_input = Entry(width=35)
email_input.grid(column=1, row=2, columnspan=2, sticky="EW", padx=(20, 40))
email_input.insert(0, "LandryH@landryhouston.com")

password_input = Entry()
password_input.grid(column=1, row=3, sticky="EW", padx=(20, 20))

generate_password_button = Button(text="Generate Password", command=generate_password)
generate_password_button.grid(column=2, row=3, sticky="EW", padx=(0, 40))

add_button = Button(text="Add", width=36, command=export)
add_button.grid(column=1, row=4, columnspan=2, sticky="EW", padx=(20, 40))

window.mainloop()