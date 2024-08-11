import time
import pygetwindow as gw
import subprocess
import pyautogui
import sys

def reopen_spotify():
    # Reopen Spotify
    subprocess.Popen(['spotify'])

def press_play():
    # Press the play button to unpause music
    pyautogui.press('playpause')
    
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
        
        # Wait for Spotify to fully reopen
        time.sleep(5)
        
        # Press play to unpause music
        press_play()
        print("Pressing play to unpause music")
    
    # Wait for 1 second before checking again
    time.sleep(1)
