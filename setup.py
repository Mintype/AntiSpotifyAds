from cx_Freeze import setup, Executable

setup(
    name="AntiSpotifyAds",
    version="0.1",
    description="This is a simple app that SKIPS advertisements on Spotify!",
    executables=[Executable("main.py", icon="logo.ico")]
)
