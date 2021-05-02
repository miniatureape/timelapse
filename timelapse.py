import sys
import time
import glob
import argparse
import cv2
import tkinter
from tkinter import Tk, RIGHT, LEFT, W, E
import PIL.Image, PIL.ImageTk

WIDTH_PROP = 3
HEIGHT_PROP = 4

def get_filename(count):
    return str(count).zfill(7) + "-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg"

def preview(camera):

    class PreviewApp:
        def __init__(self, window, window_title, device):

            self.window = window
            self.window.title(window_title)
            self.device = device
            self.video = self.init_video(device)

            self.live_canvas = tkinter.Canvas(window, width=self.video.get(WIDTH_PROP), height=self.video.get(HEIGHT_PROP))
            self.live_canvas.grid(row=1, column=0, columnspan=1)

            self.update()
            self.window.mainloop()

        def init_video(self, device):
            camera = cv2.VideoCapture(device)
            camera.set(WIDTH_PROP, 7680)
            camera.set(HEIGHT_PROP, 4320)
            return camera

        def get_frame(self):
             if self.video.isOpened():
                 ret, frame = self.video.read()
                 if ret:
                     return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                 else:
                     return (ret, None)
             else:
                 return (ret, None)

        def update(self):
            ret, frame = self.get_frame()

            if ret:
                self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
                self.live_canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

            self.window.after(16, self.update)

    PreviewApp(tkinter.Tk(), "Timelapse", device)


def capture_photos(device, interval, duration):

    camera = cv2.VideoCapture(device)
    if not camera.isOpened():
        print("Unable to open device", device)
        sys.exit(1)

    camera.set(WIDTH_PROP, 7680)
    camera.set(HEIGHT_PROP, 4320)

    count = 0
    start = time.time()
    last = start

    while True:
        now = time.time()

        if camera.isOpened():
            ret, frame = camera.read()
            cv2.imwrite(get_filename(count), frame)
            count += 1
        else:
            print("Could not access device")
            sys.exit(1)

        if now - start > duration:
            camera.release()
            print("Finished taking photos")
            sys.exit(0)

        time.sleep(interval)

def get_video_devices():
    return glob.glob('/dev/video*')

def init_argparse():

    parser = argparse.ArgumentParser(
        prog="timelapse",
        usage="%(prog)s [OPTION]",
        description="Takes photos at some interval."
    )

    parser.add_argument('-c', '--camera',  nargs='?', choices=get_video_devices(), help="Which camera device to use")
    parser.add_argument('-i', '--interval',  nargs='?', type=int, default=10, help="Seconds between photos (default: 10)")
    parser.add_argument('-d', '--duration',  nargs='?', type=int, default=240, help="Total number of seconds to take photos for (default: 240)")
    parser.add_argument('-p', '--preview', action="store_true", help="Show a window with the selected device. No photos will be taken if this option is present.")

    return parser

parser = init_argparse();
args = parser.parse_args()

device = int(args.camera.replace('/dev/video', ''))

if args.preview:
    preview(device)
else:
    capture_photos(device, args.interval, args.duration)
