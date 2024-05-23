import os
import shutil
import mysql.connector
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk

# Ensure the logos folder exists
if not os.path.exists("logos"):
    os.makedirs("logos")

# Function to connect to the MySQL database and fetch data
def fetch_data():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='rso'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM organizations")
        rows = cursor.fetchall()

        for row in tree.get_children():
            tree.delete(row)

        for row in rows:
            tree.insert("", "end", values=row)

        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error connecting to database: {err}")

# Function to fetch members of the selected organization
def fetch_members(org_id):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='rso'
        )
        cursor = conn.cursor()
        cursor.execute("SELECT mem_id, name, position FROM members WHERE mem_org = %s", (org_id,))
        rows = cursor.fetchall()

        for row in member_tree.get_children():
            member_tree.delete(row)

        for row in rows:
            member_tree.insert("", "end", values=row)

        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        messagebox.showerror("Error", f"Error fetching members: {err}")

# Function to handle the selection of an organization in the treeview
def on_tree_select(event):
    selected_item = tree.selection()
    if selected_item:
        org_id = tree.item(selected_item)["values"][0]
        fetch_members(org_id)
        edit_button.config(state=NORMAL)
        delete_button.config(state=NORMAL)
    else:
        edit_button.config(state=DISABLED)
        delete_button.config(state=DISABLED)

# Function to handle the selection of a member in the treeview
def on_member_select(event):
    selected_item = member_tree.selection()
    if selected_item:
        edit_member_button.config(state=NORMAL)
        delete_member_button.config(state=NORMAL)
    else:
        edit_member_button.config(state=DISABLED)
        delete_member_button.config(state=DISABLED)

# Function to center the popup window
def center_window(window, width=300, height=200):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    window.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

# Function to add a new organization to the database
def add_organization():
    def browse_image():
        nonlocal img_path
        filepath = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif")]
        )
        if filepath:
            img_path = filepath
            image = Image.open(filepath)
            image = image.resize((150, 150), Image.Resampling.LANCZOS)
            img_preview = ImageTk.PhotoImage(image)
            img_label.config(image=img_preview)
            img_label.image = img_preview

    def save_organization():
        org_name = org_name_entry.get()
        if org_name and img_path:
            try:
                # Save the image to the logos folder
                img_filename = os.path.basename(img_path)
                img_save_path = os.path.join("logos", img_filename)
                shutil.copy(img_path, img_save_path)

                # Save organization data to the database
                conn = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='',
                    database='rso'
                )
                cursor = conn.cursor()
                cursor.execute("INSERT INTO organizations (org_name, org_logo) VALUES (%s, %s)", (org_name, img_save_path))
                conn.commit()

                cursor.close()
                conn.close()

                messagebox.showinfo("Success", "Organization added successfully")
                popup.destroy()
                fetch_data()  # Refresh the table with new data
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error adding organization: {err}")
        else:
            messagebox.showwarning("Input Error", "Please enter an organization name and select an image")

    img_path = None
    popup = Toplevel(root)
    popup.title("Add Organization")
    popup.configure(bg="#e0f7fa")
    center_window(popup)

    Label(popup, text="Organization Name:", bg="#e0f7fa").pack(pady=10)
    org_name_entry = Entry(popup)
    org_name_entry.pack(pady=10)

    Label(popup, text="Organization Image:", bg="#e0f7fa").pack(pady=10)
    img_label = Label(popup)
    img_label.pack(pady=10)

    browse_button = Button(popup, text="Browse Image", command=browse_image, bg="#00796b", fg="white")
    browse_button.pack(pady=10)

    save_button = Button(popup, text="Save", command=save_organization, bg="#00796b", fg="white")
    save_button.pack(pady=10)

# Function to add a new member to the database
def add_member():
    def save_member():
        org_info = org_dropdown.get()
        org_id = org_info.split(" - ")[0]
        member_name = member_name_entry.get()
        position = position_entry.get()
        if member_name and position and org_id:
            try:
                conn = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='',
                    database='rso'
                )
                cursor = conn.cursor()
                cursor.execute("INSERT INTO members (name, position, mem_org) VALUES (%s, %s, %s)", (member_name, position, org_id))
                conn.commit()

                cursor.close()
                conn.close()

                messagebox.showinfo("Success", "Member added successfully")
                popup.destroy()
                # fetch_data()  # Optionally, refresh the table or other UI elements
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error adding member: {err}")
        else:
            messagebox.showwarning("Input Error", "Please fill all fields")

    def load_organizations():
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='rso'
            )
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM organizations")
            rows = cursor.fetchall()

            for row in rows:
                org_dropdown['values'] = (*org_dropdown['values'], f"{row[0]} - {row[1]}")

            cursor.close()
            conn.close()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error loading organizations: {err}")

    popup = Toplevel(root)
    popup.title("Add Member")
    popup.configure(bg="#e0f7fa")
    center_window(popup, 400, 300)  # Adjusted size for the "Add Member" form

    Label(popup, text="Organization:", bg="#e0f7fa").pack(pady=10)
    org_dropdown = ttk.Combobox(popup)
    org_dropdown.pack(pady=10)

    Label(popup, text="Member Name:", bg="#e0f7fa").pack(pady=10)
    member_name_entry = Entry(popup)
    member_name_entry.pack(pady=10)

    Label(popup, text="Position:", bg="#e0f7fa").pack(pady=10)
    position_entry = Entry(popup)
    position_entry.pack(pady=10)

    save_button = Button(popup, text="Save", command=save_member, bg="#00796b", fg="white")
    save_button.pack(pady=10)

    load_organizations()

# Function to edit an existing organization
def edit_organization():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select an organization to edit")
        return

    org_id = tree.item(selected_item)["values"][0]
    org_name = tree.item(selected_item)["values"][1]
    img_path = None  # Initialize img_path to None

    def browse_image():
        nonlocal img_path
        filepath = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif")]
        )
        if filepath:
            img_path = filepath
            image = Image.open(filepath)
            image = image.resize((150, 150), Image.Resampling.LANCZOS)
            img_preview = ImageTk.PhotoImage(image)
            img_label.config(image=img_preview)
            img_label.image = img_preview

    def update_organization():
        new_name = org_name_entry.get()
        if new_name:
            try:
                # Save the image if a new one was selected
                if img_path:
                    img_filename = os.path.basename(img_path)
                    img_save_path = os.path.join("logos", img_filename)
                    shutil.copy(img_path, img_save_path)
                else:
                    img_save_path = None

                conn = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='',
                    database='rso'
                )
                cursor = conn.cursor()
                if img_save_path:
                    cursor.execute("UPDATE organizations SET org_name = %s, org_logo = %s WHERE org_id = %s", (new_name, img_save_path, org_id))
                else:
                    cursor.execute("UPDATE organizations SET org_name = %s WHERE org_id = %s", (new_name, org_id))
                conn.commit()

                cursor.close()
                conn.close()

                messagebox.showinfo("Success", "Organization updated successfully")
                popup.destroy()
                fetch_data()  # Refresh the table with new data
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error updating organization: {err}")
        else:
            messagebox.showwarning("Input Error", "Please enter a new organization name")

    popup = Toplevel(root)
    popup.title("Edit Organization")
    popup.configure(bg="#e0f7fa")
    center_window(popup, 400, 300)  # Adjusted size for the "Edit Organization" form

    Label(popup, text="Organization Name:", bg="#e0f7fa").pack(pady=10)
    org_name_entry = Entry(popup)
    org_name_entry.insert(0, org_name)
    org_name_entry.pack(pady=10)

    Label(popup, text="Organization Image:", bg="#e0f7fa").pack(pady=10)
    img_label = Label(popup)
    img_label.pack(pady=10)

    # Load and display the existing image if available
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='rso'
    )
    cursor = conn.cursor()
    cursor.execute("SELECT org_logo FROM organizations WHERE org_id = %s", (org_id,))
    org_logo = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    if org_logo and os.path.exists(org_logo):
        image = Image.open(org_logo)
        image = image.resize((150, 150), Image.Resampling.LANCZOS)
        img_preview = ImageTk.PhotoImage(image)
        img_label.config(image=img_preview)
        img_label.image = img_preview

    browse_button = Button(popup, text="Browse Image", command=browse_image, bg="#00796b", fg="white")
    browse_button.pack(pady=10)

    save_button = Button(popup, text="Save", command=update_organization, bg="#00796b", fg="white")
    save_button.pack(pady=10)

# Function to edit an existing member
def edit_member():
    selected_item = member_tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a member to edit")
        return

    member_id = member_tree.item(selected_item)["values"][0]
    member_name = member_tree.item(selected_item)["values"][1]
    position = member_tree.item(selected_item)["values"][2]

    def update_member():
        new_name = member_name_entry.get()
        new_position = position_entry.get()
        if new_name and new_position:
            try:
                conn = mysql.connector.connect(
                    host='localhost',
                    user='root',
                    password='',
                    database='rso'
                )
                cursor = conn.cursor()
                cursor.execute("UPDATE members SET name = %s, position = %s WHERE mem_id = %s", (new_name, new_position, member_id))
                conn.commit()

                cursor.close()
                conn.close()

                messagebox.showinfo("Success", "Member updated successfully")
                popup.destroy()
                fetch_members(tree.item(tree.selection())["values"][0])  # Refresh the members table with new data
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error updating member: {err}")
        else:
            messagebox.showwarning("Input Error", "Please fill all fields")

    popup = Toplevel(root)
    popup.title("Edit Member")
    popup.configure(bg="#e0f7fa")
    center_window(popup, 400, 300)

    Label(popup, text="Member Name:", bg="#e0f7fa").pack(pady=10)
    member_name_entry = Entry(popup)
    member_name_entry.insert(0, member_name)
    member_name_entry.pack(pady=10)

    Label(popup, text="Position:", bg="#e0f7fa").pack(pady=10)
    position_entry = Entry(popup)
    position_entry.insert(0, position)
    position_entry.pack(pady=10)

    save_button = Button(popup, text="Save", command=update_member, bg="#00796b", fg="white")
    save_button.pack(pady=10)

# Function to delete an existing organization
def delete_organization():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select an organization to delete")
        return

    org_id = tree.item(selected_item)["values"][0]

    def confirm_delete():
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='rso'
            )
            cursor = conn.cursor()
            cursor.execute("DELETE FROM organizations WHERE org_id = %s", (org_id,))
            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "Organization deleted successfully")
            popup.destroy()
            fetch_data()  # Refresh the table with new data
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error deleting organization: {err}")

    popup = Toplevel(root)
    popup.title("Confirm Delete")
    popup.configure(bg="#e0f7fa")
    center_window(popup)

    Label(popup, text="Are you sure you want to delete this organization?", bg="#e0f7fa").pack(pady=10)

    confirm_button = Button(popup, text="Yes", command=confirm_delete, bg="#d32f2f", fg="white")
    confirm_button.pack(pady=10)

    cancel_button = Button(popup, text="No", command=popup.destroy, bg="#00796b", fg="white")
    cancel_button.pack(pady=10)

# Function to delete an existing member
def delete_member():
    selected_item = member_tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select a member to delete")
        return

    member_id = member_tree.item(selected_item)["values"][0]

    def confirm_delete():
        try:
            conn = mysql.connector.connect(
                host='localhost',
                user='root',
                password='',
                database='rso'
            )
            cursor = conn.cursor()
            cursor.execute("DELETE FROM members WHERE mem_id = %s", (member_id,))
            conn.commit()

            cursor.close()
            conn.close()

            messagebox.showinfo("Success", "Member deleted successfully")
            popup.destroy()
            fetch_members(tree.item(tree.selection())["values"][0])  # Refresh the members table with new data
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error deleting member: {err}")

    popup = Toplevel(root)
    popup.title("Confirm Delete")
    popup.configure(bg="#e0f7fa")
    center_window(popup)

    Label(popup, text="Are you sure you want to delete this member?", bg="#e0f7fa").pack(pady=10)

    confirm_button = Button(popup, text="Yes", command=confirm_delete, bg="#d32f2f", fg="white")
    confirm_button.pack(pady=10)

    cancel_button = Button(popup, text="No", command=popup.destroy, bg="#00796b", fg="white")
    cancel_button.pack(pady=10)

# Create the main window
root = Tk()
root.title("RSO Registration System")
root.configure(bg="#e0f7fa")

# Center the main window
center_window(root, 1000, 600)

# Create a frame for the buttons
button_frame = Frame(root, bg="#e0f7fa")
button_frame.pack(pady=10)

# Create a button to add a new organization
add_button = Button(button_frame, text="Add Organization", command=add_organization, bg="#00796b", fg="white")
add_button.grid(row=0, column=0, padx=10)

# Create a button to add a new member
add_member_button = Button(button_frame, text="Add Member", command=add_member, bg="#00796b", fg="white")
add_member_button.grid(row=0, column=1, padx=10)

# Create a button to edit an organization
edit_button = Button(button_frame, text="Edit Organization", command=edit_organization, bg="#00796b", fg="white", state=DISABLED)
edit_button.grid(row=0, column=2, padx=10)

# Create a button to delete an organization
delete_button = Button(button_frame, text="Delete Organization", command=delete_organization, bg="#d32f2f", fg="white", state=DISABLED)
delete_button.grid(row=0, column=3, padx=10)

# Create a button to edit a member
edit_member_button = Button(button_frame, text="Edit Member", command=edit_member, bg="#00796b", fg="white", state=DISABLED)
edit_member_button.grid(row=0, column=4, padx=10)

# Create a button to delete a member
delete_member_button = Button(button_frame, text="Delete Member", command=delete_member, bg="#d32f2f", fg="white", state=DISABLED)
delete_member_button.grid(row=0, column=5, padx=10)

# Create a frame for the treeview and the member treeview
main_frame = Frame(root, bg="#e0f7fa")
main_frame.pack(pady=10, fill=BOTH, expand=True)

# Create a treeview to display the organizations
tree_frame = Frame(main_frame, bg="#e0f7fa")
tree_frame.pack(side=LEFT, fill=BOTH, expand=True)
tree_scroll = Scrollbar(tree_frame)
tree_scroll.pack(side=RIGHT, fill=Y)

tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, columns=("ID", "Name"), show="headings")
tree.column("ID", anchor=CENTER, width=50)
tree.column("Name", anchor=W, width=300)
tree.heading("ID", text="ID", anchor=CENTER)
tree.heading("Name", text="Organization Name", anchor=W)
tree.pack(fill=BOTH, expand=True)
tree_scroll.config(command=tree.yview)

# Bind the treeview selection event
tree.bind("<<TreeviewSelect>>", on_tree_select)

# Create a treeview to display the members
member_frame = Frame(main_frame, bg="#e0f7fa")
member_frame.pack(side=RIGHT, fill=BOTH, expand=True)
member_scroll = Scrollbar(member_frame)
member_scroll.pack(side=RIGHT, fill=Y)

member_tree = ttk.Treeview(member_frame, yscrollcommand=member_scroll.set, columns=("ID", "Name", "Position"), show="headings")
member_tree.column("ID", anchor=CENTER, width=50)
member_tree.column("Name", anchor=W, width=150)
member_tree.column("Position", anchor=W, width=150)
member_tree.heading("ID", text="ID", anchor=CENTER)
member_tree.heading("Name", text="Name", anchor=W)
member_tree.heading("Position", text="Position", anchor=W)
member_tree.pack(fill=BOTH, expand=True)
member_scroll.config(command=member_tree.yview)

# Bind the member treeview selection event
member_tree.bind("<<TreeviewSelect>>", on_member_select)

# Fetch data when the UI is run
fetch_data()

# Start the GUI event loop
root.mainloop()
