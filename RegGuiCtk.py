import customtkinter
import json
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from RegDbSqlite import RegDbSqlite

class RegGuiCtk(customtkinter.CTk):

    def __init__(self, dataBase=RegDbSqlite('AppDb.db')):
        super().__init__()
        self.db = dataBase

        self.title('Registration Form for Mister and Miss Quezon City - District 1')
        self.geometry('1200x425')
        self.config(bg='#07124A')
        self.resizable(False, False)

        self.font1 = ('Arial', 20,)
        self.font2 = ('Arial', 12,)
        self.font3 = ('Arial Narrow', 10,)
        self.font4 = ('Arial', 20, 'bold')
        self.font5 = ('Helvetica', 20, 'bold')
        self.font6 = ('Helvetica', 12,)

        self.infosheet_label = self.newCtkLabel2('INFORMATION SHEET')
        self.infosheet_label.place(x=50, y=20)

        self.infosheet_label = self.newCtkLabel4('Welcome to MISTER AND MISS')
        self.infosheet_label.place(x=50, y=350)

        self.infosheet_label = self.newCtkLabel3('QUEZON CITY - DIST. 1')
        self.infosheet_label.place(x=50, y=370)

        # Data Entry Form
        # 'Barangay ID' Label and Entry Widgets
        self.idbarangay_label = self.newCtkLabel('Brgy. ID')
        self.idbarangay_label.place(x=50, y=50)
        self.idbarangay_entry = self.newCtkEntry()
        self.idbarangay_entry.place(x=50, y=70)

        # 'Name' Label and Entry Widgets
        self.name_label = self.newCtkLabel('Name')
        self.name_label.place(x=50, y=105)
        self.name_entry = self.newCtkEntry()
        self.name_entry.place(x=50, y=125)

        # 'Barangay' Label and Combo Box Widgets
        self.barangay_label = self.newCtkLabel('Barangay')
        self.barangay_label.place(x=50, y=160)
        self.barangay_cboxVar = StringVar()
        self.barangay_cboxOptions = ['Alicia', 'Bagong Pag-asa', 'Bahay Toro', 'Balingasa', 'Bungad', 'Damar', 'Damayan', 'Del Monte', 'Katipunan', 'Lourdes', 'Maharlika', 'Manresa', 'Mariblo', 'Masambong', 'N.S. Amoranto', 'Nayong Kanluran', 'San Isidro Labrador', 'San Jose', 'Santa Cruz', 'Santa Teresita', 'Sto. Cristo', 'Santo Domingo (Matalahib)', 'Siena', 'Talayan', 'Vasra', 'Veterans Village', 'West Triangle']
        self.barangay_cbox = self.newCtkComboBox(options=self.barangay_cboxOptions, 
                                    entryVariable=self.barangay_cboxVar)
        self.barangay_cbox.place(x=50, y=180)

        # 'Age' Label and Combo Box Widgets
        self.age_label = self.newCtkLabel('Age')
        self.age_label.place(x=50, y=215)
        self.age_cboxVar = StringVar()
        self.age_cboxOptions = ['18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30']
        self.age_cbox = self.newCtkComboBox(options=self.age_cboxOptions, 
                                    entryVariable=self.age_cboxVar)
        self.age_cbox.place(x=50, y=235)

        # 'Gender' Label and Combo Box Widgets
        self.gender_label = self.newCtkLabel('Gender')
        self.gender_label.place(x=50, y=270)
        self.gender_cboxVar = StringVar()
        self.gender_cboxOptions = ['Male', 'Female']
        self.gender_cbox = self.newCtkComboBox(options=self.gender_cboxOptions, 
                                    entryVariable=self.gender_cboxVar)
        self.gender_cbox.place(x=50, y=290)

        self.add_button = self.newCtkButton(text='Add Candidate',
                                onClickHandler=self.add_entry,
                                fgColor='#ada209',
                                hoverColor='#473c00',
                                borderColor='#ada209')
        self.add_button.place(x=350,y=380)

        self.new_button = self.newCtkButton(text='New Candidate',
                                onClickHandler=lambda:self.clear_form(True))
        self.new_button.place(x=465,y=380)

        self.update_button = self.newCtkButton(text='Update Candidate',
                                    onClickHandler=self.update_entry)
        self.update_button.place(x=580,y=380)

        self.delete_button = self.newCtkButton(text='Delete Candidate',
                                    onClickHandler=self.delete_entry,
                                    fgColor='#E40404',
                                    hoverColor='#AE0000',
                                    borderColor='#E40404')
        self.delete_button.place(x=695,y=380)

        self.export_button = self.newCtkButton(text='Export to CSV',
                                    onClickHandler=self.export_to_csv)
        self.export_button.place(x=810,y=380)

        self.import_button = self.newCtkButton(text='Import from CSV',
                                    onClickHandler=self.import_from_csv)
        self.import_button.place(x=925,y=380)

        self.export_to_json_button = self.newCtkButton(text='Export to JSON',
                                    onClickHandler=self.export_entries_to_json)
        self.export_to_json_button.place(x=1040,y=380)

        # Tree View for Database Entries
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self.style.configure('Treeview', 
                        font=self.font2, 
                        foreground='#fff',
                        background='#010329',
                        fieldlbackground='#313837')

        self.style.map('Treeview', background=[('selected', '#1A8F2D')])

        self.tree = ttk.Treeview(self, height=15)
        self.tree['columns'] = ('Barangay ID', 'Name', 'Barangay', 'Age', 'Gender')
        self.tree.column('#0', width=0, stretch=tk.NO)
        self.tree.column('Barangay ID', anchor=tk.CENTER, width=100)
        self.tree.column('Name', anchor=tk.CENTER, width=200)
        self.tree.column('Barangay', anchor=tk.CENTER, width=150)
        self.tree.column('Age', anchor=tk.CENTER, width=10)
        self.tree.column('Gender', anchor=tk.CENTER, width=10)

        self.tree.heading('Barangay ID', text='Barangay ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Barangay', text='Barangay')
        self.tree.heading('Age', text='Age')
        self.tree.heading('Gender', text='Gender')

        self.tree.place(x=350, y=20, width=795, height=350)
        self.tree.bind('<ButtonRelease>', self.read_display_data)

        self.add_to_treeview()

    # new Label Widget
    def newCtkLabel(self, text = 'CTK Label'):
        widget_Font=self.font2
        widget_TextColor='#FFF'
        widget_BgColor='#07124A'

        widget = customtkinter.CTkLabel(self, 
                                    text=text,
                                    font=widget_Font, 
                                    text_color=widget_TextColor,
                                    bg_color=widget_BgColor)
        return widget

    def newCtkLabel2(self, text = 'CTK Label'):
        widget_Font=self.font4
        widget_TextColor='#FFF'
        widget_BgColor='#07124A'

        widget = customtkinter.CTkLabel(self, 
                                    text=text,
                                    font=widget_Font, 
                                    text_color=widget_TextColor,
                                    bg_color=widget_BgColor)
        return widget

    def newCtkLabel3(self, text = 'CTK Label'):
        widget_Font=self.font5
        widget_TextColor='#FFF'
        widget_BgColor='#07124A'

        widget = customtkinter.CTkLabel(self, 
                                    text=text,
                                    font=widget_Font, 
                                    text_color=widget_TextColor,
                                    bg_color=widget_BgColor)
        return widget

    def newCtkLabel4(self, text = 'CTK Label'):
        widget_Font=self.font6
        widget_TextColor='#FFF'
        widget_BgColor='#07124A'

        widget = customtkinter.CTkLabel(self, 
                                    text=text,
                                    font=widget_Font, 
                                    text_color=widget_TextColor,
                                    bg_color=widget_BgColor)
        return widget

    # new Entry Widget
    def newCtkEntry(self, text = 'CTK Label'):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor='#FFF'
        widget_BorderColor='#0C9295'
        widget_BorderWidth=2
        widget_Width=250

        widget = customtkinter.CTkEntry(self,
                                    font=widget_Font,
                                    text_color=widget_TextColor,
                                    fg_color=widget_FgColor,
                                    border_color=widget_BorderColor,
                                    border_width=widget_BorderWidth,
                                    width=widget_Width)
        return widget

    # new Combo Box Widget
    def newCtkComboBox(self, options=['DEFAULT', 'OTHER'], entryVariable=None):
        widget_Font=self.font1
        widget_TextColor='#000'
        widget_FgColor='#FFF'
        widget_DropdownHoverColor='#0C9295'
        widget_ButtonColor='#0C9295'
        widget_ButtonHoverColor='#0C9295'
        widget_BorderColor='#0C9295'
        widget_BorderWidth=2
        widget_Width=250
        widget_Options=options

        widget = customtkinter.CTkComboBox(self,
                                        font=widget_Font,
                                        text_color=widget_TextColor,
                                        fg_color=widget_FgColor,
                                        border_color=widget_BorderColor,
                                        width=widget_Width,
                                        variable=entryVariable,
                                        values=options,
                                        state='readonly')
        
        # set default value to 1st option
        widget.set(options[0])

        return widget

    # new Button Widget
    def newCtkButton(self, text = 'CTK Button', onClickHandler=None, fgColor='#FFF', hoverColor='#524302', bgColor='#161C25', borderColor='#524302'):
        widget_Font=self.font3
        widget_TextColor='#000000'
        widget_FgColor=fgColor
        widget_HoverColor=hoverColor
        widget_BackgroundColor=bgColor
        widget_BorderColor=borderColor
        widget_BorderWidth=1
        widget_Cursor='hand2'
        widget_CornerRadius=0
        widget_Width=105
        widget_Height=8
        widget_Function=onClickHandler

        widget = customtkinter.CTkButton(self,
                                        text=text,
                                        command=widget_Function,
                                        font=widget_Font,
                                        text_color=widget_TextColor,
                                        fg_color=widget_FgColor,
                                        hover_color=widget_HoverColor,
                                        bg_color=widget_BackgroundColor,
                                        border_color=widget_BorderColor,
                                        border_width=widget_BorderWidth,
                                        cursor=widget_Cursor,
                                        corner_radius=widget_CornerRadius,
                                        width=widget_Width, height=widget_Height)
       
        return widget

    # Handles
    def add_to_treeview(self):
        candidates = self.db.fetch_candidates()
        self.tree.delete(*self.tree.get_children())
        for candidate in candidates:
            print(candidate)
            self.tree.insert('', END, values=candidate)

    def clear_form(self, *clicked):
        if clicked:
            self.tree.selection_remove(self.tree.focus())
            self.tree.focus('')
        self.idbarangay_entry.delete(0, END)
        self.name_entry.delete(0, END)
        self.barangay_cboxVar.set('Alicia')
        self.age_cboxVar.set('18')
        self.gender_cboxVar.set('Male')

    def read_display_data(self, event):
        selected_item = self.tree.focus()
        if selected_item:
            row = self.tree.item(selected_item)['values']
            self.clear_form()
            self.idbarangay_entry.insert(0, row[0])
            self.name_entry.insert(0, row[1])
            self.barangay_cboxVar.set(row[2])
            self.age_cboxVar.set(row[3])
            self.gender_cboxVar.set(row[4])
        else:
            pass

    def add_entry(self):
        idbarangay=self.idbarangay_entry.get()
        name=self.name_entry.get()
        barangay=self.barangay_cboxVar.get()
        age=self.age_cboxVar.get()
        gender=self.gender_cboxVar.get()

        if not (idbarangay and name and barangay and age and gender):
            messagebox.showerror('Error.', 'Please enter all fields.')
        elif self.db.id_exists(idbarangay):
            messagebox.showerror('Error.', 'Barangay ID already exists')
        else:
            self.db.insert_candidate(idbarangay, name, barangay, age, gender)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success!', 'Data has been inputted.')

    def delete_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error.', 'Choose a candidate to delete.')
        else:
            idbarangay = self.idbarangay_entry.get()
            self.db.delete_candidate(idbarangay)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success.', 'The data has been deleted.')

    def update_entry(self):
        selected_item = self.tree.focus()
        if not selected_item:
            messagebox.showerror('Error.', 'Choose a candidate to update information.')
        else:
            idbarangay=self.idbarangay_entry.get()
            name=self.name_entry.get()
            barangay=self.barangay_cboxVar.get()
            age=self.age_cboxVar.get()
            gender=self.gender_cboxVar.get()
            self.db.update_candidate(name, barangay, age, gender, idbarangay)
            self.add_to_treeview()
            self.clear_form()
            messagebox.showinfo('Success.', 'The data has been updated!')

    def export_to_csv(self):
        self.db.export_csv()
        messagebox.showinfo('Success.', f'Data exported to {self.db.dbName}.csv')

    def import_from_csv(self):
        file_path = filedialog.askopenfilename(title="Open CSV File", filetypes=[("CSV files", ".csv")])

        if not file_path:
            messagebox.showinfo('Info', 'No file selected.')
            return

        if self.db.import_csv(file_path):
            messagebox.showinfo('Success!', f'Data imported from {file_path}')
            # Optionally, update the displayed data in your GUI after importing
            self.add_to_treeview()
        else:
            messagebox.showerror('Error.', f'Failed to import data from {file_path}')

    def export_entries_to_json(self):
        candidates = self.db.fetch_candidates()
        json_data = []

        for candidate in candidates:
            candidate_dict = {
                'Barangay ID': candidate[0],
                'Name': candidate[1],
                'Barangay': candidate[2],
                'Age': candidate[3],
                'Gender': candidate[4]
            }
            json_data.append(candidate_dict)

        # Export to JSON file
        with open('Candidates.json', 'w') as json_file:
            json.dump(json_data, json_file, indent=4)

        messagebox.showinfo('Success!', 'Data exported to Candidates.json')





