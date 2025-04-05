import sys
from cx_Freeze import setup, Executable

setup(
    name="AntiSpotifyAds",
    version="0.1",
    description="This is a simple app that SKIPS advertisements on Spotify!",
    options={
        'build_exe': {
            'optimize': 2,  # Level 2 optimization
            'include_files': ['logo.ico']  # Include any necessary files
        }
    },
    executables=[Executable("main.py", icon="logo.ico")]
)
