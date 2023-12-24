import os
import sys
import ctypes
import tkinter as tk
import webbrowser
from PIL import ImageTk, Image
import func as func

ctypes.windll.shcore.SetProcessDpiAwareness(1)
main_window = tk.Tk()
main_window.resizable(False, False)
padx = 8
pady = 4
scenes = []
current_scene = 0


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


is_admin = is_admin()
title = "ADMIN: PHP Windows Install Script" if is_admin else "PHP Windows Install Script"
main_window.title(title)

root = func.export_root()


def as_admin(exe, args=None):
    if not args:
        if " " in exe:
            args = exe.split(" ")
            exe = args[0]
            args = args.pop(0)
            args = " ".join(args)
        else:
            args = ""
    if is_admin:
        os.system(exe + " " + args)
    else:
        ctypes.windll.shell32.ShellExecuteW(None, "runas", exe, args, None, 1)


button_container = tk.Frame(main_window)
button_container.grid(row=1, column=0, padx=padx, pady=pady, columnspan=99, sticky=tk.E)
back_button = tk.Button(button_container, text="Back")
back_button.grid(row=0, column=0, pady=pady)
next_button = tk.Button(button_container, text="Next")
next_button.grid(row=0, column=1, padx=padx, pady=pady)
cancel_button = tk.Button(button_container, text="Cancel", command=func.confirm_exit)
cancel_button.grid(row=0, column=2, padx=padx, pady=pady)

php_logo = Image.open(root + "\\php-logo.png")
php_logo = php_logo.resize((128, 69))
php_logo = ImageTk.PhotoImage(php_logo)

php_logo_frame = tk.Frame(main_window)
php_logo_frame.grid(row=0, column=0)
php_logo_label = tk.Label(php_logo_frame, image=php_logo)
php_logo_label.grid(sticky=tk.W)

# step 1: welcome screen
page_welcome = tk.Frame(main_window)
page_welcome.grid(row=0, column=1)
scenes.append(["welcome", page_welcome, ["disabled", None], ["active", "increment"]])
welcome_label = tk.Label(page_welcome, text="Welcome to PHP Windows Install Script.\nThis will install a development PHP server.")
welcome_label.grid(padx=padx, pady=pady)

# step 2: choose a file
page_file_choose = tk.Frame(main_window)
page_file_choose.grid(row=0, column=1)
scenes.append(["file_choose", page_file_choose, ["active", "decrement"], ["disabled", "increment"]])
file_choose_text = tk.Label(page_file_choose, text="Select a PHP package to install.\nIf you don't have any downloaded, you can press the Downloads Link button, and download a package.\nIt has to be the Zip file, and the Thread Safe version is recommended.")
file_choose_text.grid(row=0, column=0, columnspan=99, padx=padx, pady=pady)
file_choose_download = tk.Button(page_file_choose, text="Downloads Link", command=lambda: webbrowser.open_new_tab("https://windows.php.net/download"))
file_choose_download.grid(row=1, column=0, padx=padx, pady=pady)
file_choose_filechooser = tk.Button(page_file_choose, text="Select Package", command=lambda: func.get_package(file_choose_indicator, next_button))
file_choose_filechooser.grid(row=1, column=1, padx=padx, pady=pady)
file_choose_indicator = tk.Label(page_file_choose, text="No package selected!", fg="#FF0000")
file_choose_indicator.grid(row=1, column=2, padx=padx, pady=pady)

# step 3: confirm installation
page_confirm = tk.Frame(main_window)
page_confirm.grid(row=0, column=1)
scenes.append(["confirm", page_confirm, ["active", "decrement"], ["active", "increment"]])
confirm_label = tk.Label(page_confirm, text="Are you sure you want to install the PHP server?\nIt will be installed to your %appdata% directory as php-server.\nPress Next to confirm.")
confirm_label.grid()

# step 4: unzip over php-server
page_install = tk.Frame(main_window)
page_install.grid(row=0, column=1)
scenes.append(["install", page_install, ["disabled", "decrement"], ["disabled", "increment"]])
install_progress_label = tk.Label(page_install, text="Unpacking...")
install_progress_label.grid()

# step 5: post-install
page_post_install = tk.Frame(main_window)
page_post_install.grid(row=0, column=1)
scenes.append(["post-install", page_post_install, ["disabled", "decrement"], ["active", "increment"]])
post_install_label = tk.Label(page_post_install, text="Done!\nYour PHP server is now installed to %appdata%\\php-server,\nand you should be able to use it by executing php in a console.\n You may need to close and re-open any already open consoles\nfor this to work.")
post_install_label.grid()


def set_scene(scene_name=None):
    global current_scene
    scene_already_set = False
    for scene in scenes:
        scene[1].grid_remove()

    if scene_name is None or scene_name == "increment":
        set_scene(current_scene + 1)
        scene_already_set = True
    elif scene_name == "decrement":
        set_scene(current_scene - 1)
        scene_already_set = True
    elif isinstance(scene_name, int):
        current_scene = scene_name
    else:
        # set scene to scene_name
        scene_found = False
        scene = 0
        while not scene_found:
            if scenes[scene][0] == scene_name:
                scene_found = True
            else:
                scene += 1
        current_scene = scene

    if not scene_already_set:
        try:
            scenes[current_scene][1].grid()
        except IndexError:
            sys.exit(0)
        back_button.configure(state=scenes[current_scene][2][0], command=lambda: set_scene(scenes[current_scene][2][1]))
        next_button.configure(state=scenes[current_scene][3][0], command=lambda: set_scene(scenes[current_scene][3][1]))

        # do these specific things when arriving at a scene
        if current_scene == 1:
            if func.is_package_selected():
                next_button.configure(state="active")
        elif current_scene == 3:
            func.install(install_progress_label, lambda: set_scene(4))
        elif current_scene == 4:
            next_button.configure(text="Finish")
            cancel_button.grid_remove()


if __name__ == "__main__":
    set_scene(0)
    main_window.mainloop()