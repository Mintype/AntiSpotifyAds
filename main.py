import time
import subprocess
import sys
import tkinter as tk
import threading
import os

IS_MAC = sys.platform == "darwin"
IS_WINDOWS = sys.platform.startswith("win")

if IS_WINDOWS:
    import pygetwindow as gw
    import pyautogui


# --------------------------------------------------------------------------- #
# macOS helpers (Spotify exposes an AppleScript interface on macOS)
# --------------------------------------------------------------------------- #
def _osascript(script):
    """Run an AppleScript snippet and return its stdout, or None on failure."""
    try:
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True, text=True, timeout=5,
        )
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return None
    if result.returncode != 0:
        return None
    return result.stdout.strip()


def mac_spotify_running():
    out = _osascript('tell application "System Events" to (name of processes) contains "Spotify"')
    return out == "true"


def mac_ad_playing():
    """Return True if Spotify is currently playing an advertisement."""
    if not mac_spotify_running():
        return False
    # Ads have a URL like "spotify:ad:..." instead of "spotify:track:...".
    url = _osascript('tell application "Spotify" to get spotify url of current track')
    if url and url.startswith("spotify:ad:"):
        return True
    name = _osascript('tell application "Spotify" to get name of current track')
    return name == "Advertisement"


# --------------------------------------------------------------------------- #
# Cross-platform actions
# --------------------------------------------------------------------------- #
def ad_detected():
    if IS_MAC:
        return mac_ad_playing()
    if IS_WINDOWS:
        return bool(gw.getWindowsWithTitle("Advertisement"))
    return False


def close_spotify():
    if IS_MAC:
        _osascript('tell application "Spotify" to quit')
    elif IS_WINDOWS:
        for window in gw.getWindowsWithTitle("Advertisement"):
            window.close()


def reopen_spotify():
    try:
        if IS_MAC:
            subprocess.run(["open", "-a", "Spotify"], check=True)
        elif IS_WINDOWS:
            user_profile = os.environ.get("USERPROFILE", "")
            spotify_path = os.path.join(user_profile, r"AppData\Roaming\Spotify\Spotify.exe")
            # Popen so we don't block until Spotify exits.
            subprocess.Popen([spotify_path])
    except FileNotFoundError:
        print("Spotify is not installed or not found in the system path.")
    except subprocess.CalledProcessError:
        print("Error opening Spotify.")


def press_play():
    if IS_MAC:
        _osascript('tell application "Spotify" to play')
    elif IS_WINDOWS:
        pyautogui.press("playpause")


def monitor_spotify():
    while running:
        try:
            if ad_detected():
                print("Advertisement detected - closing Spotify")
                close_spotify()
                time.sleep(1)

                print("Reopening Spotify")
                reopen_spotify()
                time.sleep(5)

                print("Pressing play to resume music")
                press_play()
        except Exception as exc:  # keep the monitor alive on unexpected errors
            print(f"Monitor error: {exc}")

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
sys.stdout.buffer.write(spotify_logo.encode("utf-8"))
print("\nAnti-Spotify-Ads program started: Have fun listening!")

if not (IS_MAC or IS_WINDOWS):
    print("Warning: unsupported platform - ad detection is only implemented for macOS and Windows.")

# Create a tkinter window
root = tk.Tk()
root.title("Anti-Spotify-Ads Control Panel")

# Set window size
root.geometry("300x100")

# Load the logo (.ico files are only supported by Tk on Windows)
if IS_WINDOWS:
    try:
        root.iconbitmap(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.ico"))
    except tk.TclError:
        pass

# Add a label
label = tk.Label(root, text="This program is running...\nClose this window to stop.")
label.pack(pady=20)

# Set the close event
root.protocol("WM_DELETE_WINDOW", on_close)

# Set running to True
running = True

# Start the monitoring in a new thread
monitor_thread = threading.Thread(target=monitor_spotify, daemon=True)
monitor_thread.start()

# Start the tkinter main loop
root.mainloop()

# Wait for the thread to finish
monitor_thread.join()
