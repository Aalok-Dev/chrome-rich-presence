import ctypes
from typing import Text
from pypresence import Presence
import time, os, sys
from textfilters import title_filter


client_id = '1111111111111111111111111111'  # Fake ID, put your real one here
RPC = Presence(client_id)  # Initialize the client class
RPC.connect() # Start the handshake loop

start_time=time.time()


def full():
    EnumWindows = ctypes.windll.user32.EnumWindows
    EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    GetWindowText = ctypes.windll.user32.GetWindowTextW
    GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
    IsWindowVisible = ctypes.windll.user32.IsWindowVisible

    titles = []
    def foreach_window(hwnd, lParams):
        if IsWindowVisible(hwnd):
            length = GetWindowTextLength(hwnd)
            buff = ctypes.create_unicode_buffer(length + 1)
            GetWindowText(hwnd, buff, length + 1)
            titles.append(buff.value)
    EnumWindows(EnumWindowsProc(foreach_window), 0)

    sub = 'Youtube' #write the name of tab you want to show
    for text in titles:
        if sub in text:
            for title in title_filter:
                textp = text.replace(title,"")


    print(RPC.update(large_image="youtube-logo-png-2088", state=textp, details="Watching to: ", start=start_time, buttons=[{"label": "Watch Youtube", "url": "https://www.youtube.com/"}]))  # Set the presence
    time.sleep(15) # Can only update rich presence every 15 second


    full()
try:
    full()
except KeyboardInterrupt:
    print('Closing program')
except UnboundLocalError:
    print('No Youtube Tab Found!')
    print('Please bring tab to foreground or keep it open in a separate browser!')
finally:
    RPC.close()

