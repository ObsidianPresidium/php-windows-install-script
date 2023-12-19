import os
import sys
import tkinter as tk
import tkinter.messagebox as tkmsg
from tkinter import filedialog
import zipfile
import threading

package_filename = None


def export_root():
    if getattr(sys, "frozen", False):  # fix for pyinstaller paths
        return sys._MEIPASS
    else:
        return os.path.dirname(os.path.abspath(__file__))


def get_package(indicator_widget : tk.Label, next_button : tk.Button):
    filetypes = [
        ("PHP Zip Package", ".zip")
    ]
    filename = filedialog.askopenfilename(title="Select Package", initialdir=f"{os.getenv("USERPROFILE")}\\Downloads",
                                          filetypes=filetypes)
    if os.path.exists(filename):
        global package_filename
        package_filename = filename
        indicator_widget.configure(text="Package selected, press Next to continue", fg="#00FF00")
        next_button.configure(state="active")
    else:
        indicator_widget.configure(text="No package selected!", fg="#FF0000")
        next_button.configure(state="disabled")


def unzip_and_path(install_location, progress_label, callback_function):
    with zipfile.ZipFile(package_filename, "r") as zip_ref:
        zip_ref.extractall(install_location)

    progress_label.configure(text="Creating a user-specific PATH variable...")
    if "php-server" not in os.environ["PATH"]:
        os.environ["PATH"] += os.pathsep + install_location
        os.system(f"powershell setx PATH ((Get-ItemProperty HKCU:\\Environment).PATH + ';{install_location}')")

    progress_label.configure(text="Done!")
    callback_function()


def install(progress_label : tk.Label, callback_function):
    progress_label.configure(text="Getting ready...")
    install_location = os.getenv("APPDATA") + "\\php-server"
    if os.path.exists(install_location):
        os.rmdir(install_location)
    os.mkdir(install_location)

    unzip_thread = threading.Thread(target=unzip_and_path, args=(install_location, progress_label, callback_function,))
    unzip_thread.start()
    progress_label.configure(text="Unpacking the PHP package...")


def confirm_exit():
    confirm = tkmsg.askyesno("PHP Windows Install Script", "Are you sure you want to cancel the installation?")
    if confirm:
        sys.exit(0)