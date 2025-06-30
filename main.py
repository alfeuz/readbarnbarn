from Windowscapture import *
from Mapping import *
import cv2 as cv
import time

""" windows = WindowCapture('BAAC')
while True:
    screen = windows.screenshot()
    cv.imshow('screen',screen)
    time.sleep(0.1)
    if cv.waitKey(10) == 27: 
        break
cv.destroyAllWindows() """

## initialize title ##
windows = WindowCapture('all')
#looptime = time()

# Create window with resize capability
cv.namedWindow('Screen Capture', cv.WINDOW_NORMAL)
cv.resizeWindow('Screen Capture', 800, 600)  # Set initial window size

print("Program started!")
print("Controls:")
print("- ESC: Exit program")
print("- X button: Close window to exit program")
print("- You can resize the window by dragging corners")
print("- Press any key in the window to continue...")

while True:
    ## take screenshot ##
    screen = windows.screenshot() #ค่าที่อ่านได้เป็น numpy array
    ##start bot ##
    #search = Mapping(screen,'img/test11.jpg') #ค่าที่จะส่งไป class bot จึงไม่ต้องทำการแปลงค่าให้เป็นตัวเลข
    #point = search.search(threshold=0.6,debug=True)
    #print(f"Found points: {point}")
    
    # Display the screen capture in resizable window
    cv.imshow('Screen Capture', screen)
    
    # Check for key press first
    key = cv.waitKey(1) & 0xFF
    if key == 27:  # ESC key
        print("ESC pressed - Exiting program...")
        break
    elif key != 255:  # Any other key pressed (255 means no key pressed)
        print(f"Key pressed: {key}")
    
    # Check if window was closed (X button pressed) - using try-except for reliability
    try:
        # Alternative method to check if window exists
        window_property = cv.getWindowProperty('Screen Capture', cv.WND_PROP_VISIBLE)
        if window_property <= 0:
            print("Window closed - Exiting program...")
            break
    except cv.error:
        # If getWindowProperty fails, the window was likely closed
        print("Window closed (detected via exception) - Exiting program...")
        break

print("Program ended!")
cv.destroyAllWindows()