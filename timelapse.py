import sys
import tkinter
from tkinter import Tk, RIGHT, LEFT
import cv2
import PIL.Image, PIL.ImageTk
import time

class App:

    def __init__(self, window, window_title, video_source=4):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        """
        self.window.columnconfigure(0, pad=3)
        self.window.columnconfigure(1, pad=3)
        self.window.rowconfigure(0, pad=3)
        self.window.rowconfigure(1, pad=3)
        self.window.rowconfigure(2, pad=3)
        """

        self.running = False

         # open video source (by default this will try to open the computer webcam)
        self.video_label = tkinter.Label(window, text="Live feed")
        # self.video_label.grid(row=0, column=0)
        self.video_label.pack()
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width = self.vid.width * 2, height = self.vid.height)
        # self.canvas.grid(row=1)
        self.canvas.pack()

        self.btn_toggle=tkinter.Button(window, text="Start", width=50, command=self.toggle)
        # self.btn_toggle.grid(row=2)
        self.btn_toggle.pack()

        self.delay_label = tkinter.Label(window, text="Seconds between photos:")
        # self.delay_label.grid(row=2)
        self.delay_label.pack()
        self.delay_entry = tkinter.Entry(window, text="60")
        # self.delay_entry.grid(row=2)
        self.delay_entry.pack()

        self.duration_label = tkinter.Label(window, text="Maximum minutes to run")
        self.duration_label.pack()
        self.duration_entry = tkinter.Entry(window, text="60")
        self.duration_entry.pack()

        self.start_time = time.time()
        self.last_time = time.time()
        self.count = 0
        self.delay = 15
        self.update()

        self.window.mainloop()

    def toggle(self):
        self.running = not self.running
        self.interval = int(self.delay_entry.get())
        self.btn_toggle['text'] = "Stop" if self.running else "Start"


    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

        if self.running:
            now = time.time()
            if time.time() - self.last_time > self.interval:
                self.last_time = now
                ret, frame = self.vid.get_frame()
                if ret:
                    self.count += 1
                    cv2.imwrite(str(self.count).zfill(7) + "-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

        self.window.after(self.delay, self.update)

class MyVideoCapture:
    def __init__(self, video_source=0):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
             raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
         if self.vid.isOpened():
             ret, frame = self.vid.read()
             if ret:
                 # Return a boolean success flag and the current frame converted to BGR
                 return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
             else:
                 return (ret, None)
         else:
             return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Create a window and pass it to the Application object
if len(sys.argv) == 2:
    video_source = int(sys.argv[1])
else:
    video_source = 0

App(tkinter.Tk(), "Tkinter and OpenCV", video_source=video_source)
