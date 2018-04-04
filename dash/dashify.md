# Note
Another way to prepare dash videos is in video_creation.txt but it is too slow compared to this way

# Requirements
```
sudo apt install x264 gpac
```

# Video Preparation
```
x264 --output tmp_N.264 --fps 24 --preset slow --bitrate N --vbv-maxrate 2N --vbv-bufsize 4N --min-keyint M --keyint M --scenecut 0 --no-scenecut --pass 1 --video-filter "resize:width=W,height=H" video.mkv
```

```
MP4Box -add tmp_N.264 -fps 24 output_N.mp4
```
The command below also creates the dash manifest as `output_N_dash.mpd`
```
MP4Box -dash T -frag T -rap -segment-name segmentN_ output_N.mp4
```

Notes
* N would be framerate which resolutions with which framerate will be below
* M should be set according to `segment_length * fps` example: 4 seconds and 24 fps = 96
* W and H should be resolution values
* T is segment length by miliseconds. You should use the same length you used in M

## Resolution Framerate table

| Height  | Weight   | Framerate  |
| ------- |:--------:| ----------:|
| 1920    | 1080     | 5000, 3000 |
| 1280    | 720      | 2400, 1500 |
| 854     | 480      | 750        |
| 640     | 480      | 350        |

# Audio Preparation
You should use the other method for now

# Final Manifest
You would have merge these 
