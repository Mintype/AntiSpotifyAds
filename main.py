import time
import pygetwindow as gw
import subprocess
import pyautogui
import sys
import tkinter as tk
import threading
from PIL import Image, ImageTk
from tkinter import *
from tkinter.ttk import *

def reopen_spotify():
    # Reopen Spotify
    subprocess.Popen(['spotify'])

def press_play():
    # Press the play button to unpause music
    pyautogui.press('playpause')

def monitor_spotify():
    while running:
        windows = gw.getWindowsWithTitle('Advertisement')

        if windows:
            # Close Spotify
            for window in windows:
                window.close()
                print("Closing Spotify")

            # Wait a second
            time.sleep(1)

            # Reopen Spotify
            reopen_spotify()
            print("Reopening Spotify")

            # Wait for Spotify to fully reopen
            time.sleep(5)

            # Press play to unpause music
            press_play()
            print("Pressing play to unpause music")

        # Wait for 1 second before checking again
        time.sleep(1)

def on_close():
    global running
    running = False
    root.destroy()

spotify_logo = '''
                  ██████████                  
             ████████████████████             
          ██████████████████████████          
        ██████████████████████████████        
      ██████████████████████████████████      
     ████████████████████████████████████     
   ████████████████████████████████████████   
  ██████████            ████████████████████  
  ██████                         ███████████  
 ███████      ████████               ████████ 
 ██████████████████████████████        ██████ 
 ██████████████       ██████████████   ██████ 
 ████████                     ███████████████ 
 █████████  █████████████         ███████████ 
 ██████████████████████████████     █████████ 
 ███████████            █████████████████████ 
  █████████                   ██████████████  
  ██████████████████████████     ███████████  
   ████████████████████████████████████████   
     ████████████████████████████████████     
      ██████████████████████████████████      
        ██████████████████████████████        
          ██████████████████████████          
             ████████████████████             
                  ██████████                  
'''
sys.stdout.buffer.write(spotify_logo.encode('utf-8'))
print("\nAnti-Spotify-Ads program started: Have fun listening!")

# Create a tkinter window
root = tk.Tk()
root.title("Anti-Spotify-Ads Control Panel")

# Set window size
root.geometry("300x100")

# Load the logo
icon = tk.PhotoImage(file="logo.png")
root.iconphoto(False, icon, icon)

# Add a label
label = tk.Label(root, text="This program is running...\nClose this window to stop.")
label.pack(pady=20)

# Set the close event
root.protocol("WM_DELETE_WINDOW", on_close)

# Set running to True
running = True

# Start the monitoring in a new thread
monitor_thread = threading.Thread(target=monitor_spotify)
monitor_thread.start()

# Start the tkinter main loop
root.mainloop()

# Wait for the thread to finish
monitor_thread.join()
