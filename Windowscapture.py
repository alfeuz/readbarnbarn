import win32gui, win32ui, win32con
import numpy as np
from ctypes import windll
class WindowCapture:
    def __init__(self, window_name):
        # find the handle for the window we want to capture
        if window_name.lower() == "all":
            self.hwnd = None  # None means capture full screen
            self.capture_mode = "fullscreen"
        else:
            self.hwnd = win32gui.FindWindow(None, window_name)
            if not self.hwnd:
                raise Exception('Window not found: {}'.format(window_name))
            self.capture_mode = "window"
    
    def screenshot(self):
        if self.capture_mode == "fullscreen":
            return self.capture_fullscreen()
        else:
            return self.capture_window()
    
    def capture_fullscreen(self):
        # Get full screen dimensions
        screen_width = windll.user32.GetSystemMetrics(0)
        screen_height = windll.user32.GetSystemMetrics(1)
        
        # Create device context
        hdesktop = win32gui.GetDesktopWindow()
        hwnd_dc = win32gui.GetWindowDC(hdesktop)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()
        
        # Create bitmap
        bitmap = win32ui.CreateBitmap()
        bitmap.CreateCompatibleBitmap(mfc_dc, screen_width, screen_height)
        save_dc.SelectObject(bitmap)
        
        # Copy screen to bitmap
        save_dc.BitBlt((0, 0), (screen_width, screen_height), mfc_dc, (0, 0), win32con.SRCCOPY)
        
        # Convert to numpy array
        bmpinfo = bitmap.GetInfo()
        bmpstr = bitmap.GetBitmapBits(True)
        img = np.frombuffer(bmpstr, dtype=np.uint8).reshape((bmpinfo["bmHeight"], bmpinfo["bmWidth"], 4))
        img = img[..., :3]  # Remove alpha channel
        img = np.ascontiguousarray(img)
        
        # Clean up
        win32gui.DeleteObject(bitmap.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(hdesktop, hwnd_dc)
        
        return img
    
    def capture_window(self):
        left, top, right, bottom = win32gui.GetClientRect(self.hwnd)

        w = right - left
        h = bottom - top
        hwnd_dc = win32gui.GetWindowDC(self.hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()
        bitmap = win32ui.CreateBitmap()
        bitmap.CreateCompatibleBitmap(mfc_dc, w, h)
        save_dc.SelectObject(bitmap)
        # If Special K is running, this number is 3. If not, 1
        result = windll.user32.PrintWindow(self.hwnd, save_dc.GetSafeHdc(), 3)
        bmpinfo = bitmap.GetInfo()
        bmpstr = bitmap.GetBitmapBits(True)
        img = np.frombuffer(bmpstr, dtype=np.uint8).reshape((bmpinfo["bmHeight"], bmpinfo["bmWidth"], 4))
        img = img[...,: 3]
        img = np.ascontiguousarray(img)# make image C_CONTIGUOUS and drop alpha channel
        win32gui.DeleteObject(bitmap.GetHandle())
        save_dc.DeleteDC()
        mfc_dc.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, hwnd_dc)
        return img


