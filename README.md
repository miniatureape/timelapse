# Timelapse

Takes JPG photos on at a specified interval for a specified duration. Tested only on Ubuntu 20.

## Install

Add `opencv-python` and `Pillow` or use the requirements file:

```
pip install -r requirements.txt
```

## Usage

To use you need to specify which device you want to capture from. To see a list, try:

```
python timelapse.py --help
```

and review the choices for the `--camera` option.

To view the device to check that you have the right one and get your framing right, try the preview option:

```
python timelapse.py --camera "/dev/video0" --preview
```

This won't take any photos, but will open a window and allow you to make sure you're taking pictures of the right thing.

To actually take photos, remove the preview option and specify an interval and overall duraction in seconds.

```
python timelapse.py --camera "/dev/video0" --interval 10 --duraction 240
```

This will take a photo every ten seconds for one minute and save it in the current working directory.

## Making Videos

Use `ffmpeg` or similar in order to turn your photos into a video.

```
ffmpeg -framerate 24 -pattern_type glob -i '*.jpg'   -c:v libx264 -pix_fmt yuv420p out.mp4
```

With this command it takes 24 photos to make one second of video.
