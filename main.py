import time
import pygetwindow as gw
import subprocess

def reopen_spotify():
    # Reopen Spotify
    subprocess.Popen(['spotify'])
    
print("Program started: Have fun listening!")

while True:
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
    
    # Wait for 1 second before checking again
    time.sleep(1)
