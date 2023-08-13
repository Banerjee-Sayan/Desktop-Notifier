from tkinter import *
import tkinter as tk
from tkinter import ttk
from tktimepicker import AnalogPicker, AnalogThemes
from plyer import notification 
from datetime import datetime
from win10toast import ToastNotifier
import os

toaster = ToastNotifier()

root = Tk()
root.title('Desktop Notifier')
root.geometry('500x400')
root.configure(bg='lightgray')

notification_get = None
reminders = []

def submit_time():
    global reminders
    global notification_get
    selected_hour = hour_var.get()
    selected_minute = minute_var.get()
    selected_time = f"{int(selected_hour):02d}:{int(selected_minute):02d}"
    notification_get = notification_input.get()
    reminders.append((notification_get, selected_time))
    update_reminders_listbox()
    schedule_notification() 

def delete_reminder():
    global reminders
    selected_index = reminders_listbox.curselection()
    if selected_index:
        index = selected_index[0]
        reminders.pop(index)
        update_reminders_listbox()

def update_reminders_listbox():
    reminders_listbox.delete(0, END)
    for reminder in reminders:
        reminders_listbox.insert(END, f"{reminder[0]} - {reminder[1]}")

def schedule_notification():
    global reminders
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    
    for notification_get, selected_time in reminders:
        if current_time == selected_time:
            toaster.show_toast(notification_get, " ", icon_path=None, duration=60, threaded=True)
    
    root.after(1000, schedule_notification)


header_frame = Frame(root, bg='lightgray')
header_label = Label(header_frame, text='Desktop Notifier', fg='black', font=('Helvetica', 24, 'bold'), bg='lightgray')
header_label.pack(pady=(20, 0))
header_frame.pack(fill='x')

notification_frame = Frame(root, bg='lightgray')
notification_label = Label(notification_frame, text='Enter Notification:', font=('Helvetica', 12), bg='lightgray')
notification_label.pack()
notification_input = Entry(notification_frame, width=40)
notification_input.pack()
notification_frame.pack(fill='x', pady=10)


time_frame = Frame(root)
hour_var = tk.StringVar()
minute_var = tk.StringVar()

hour_label = Label(time_frame, text='Hour:', font=('Helvetica', 12))
hour_spinbox = ttk.Spinbox(time_frame, from_=0, to=23, textvariable=hour_var, width=3)

minute_label = Label(time_frame, text='Minute:', font=('Helvetica', 12))
minute_spinbox = ttk.Spinbox(time_frame, from_=0, to=59, textvariable=minute_var, width=3)

hour_label.pack(side="left")
hour_spinbox.pack(side="left")
minute_label.pack(side="left")
minute_spinbox.pack(side="left")

time_frame.pack()


submit_btn = Button(root, text='Set Reminder', bg='black', fg='white', width=15, command=submit_time)
submit_btn.pack(pady=(20, 5))


delete_btn = Button(root, text='Delete Reminder', bg='red', fg='white', width=15, command=delete_reminder)
delete_btn.pack(pady=(5, 20))


reminders_frame = Frame(root, bg='lightgray')
reminders_label = Label(reminders_frame, text='Upcoming Reminders:', font=('Helvetica', 12), bg='lightgray')
reminders_label.pack()
reminders_listbox = Listbox(reminders_frame, selectmode=SINGLE, width=50, height=5)
reminders_listbox.pack()
reminders_frame.pack(fill='x', pady=10)

root.mainloop()
