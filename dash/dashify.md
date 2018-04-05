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
```
ffmpeg -i video.mp4 -vn -acodec libvorbis -ab 320k -dash 1 audio.webm
```
```
ffmpeg \
  -f webm_dash_manifest -i audio.webm -c copy -map 0 \
  -f webm_dash_manifest -adaptation_sets "id=0,streams=0" audio_manifest.mpd
```
# Final Manifest
MP4Box create a seperate manifest for each resolution. You should merge these into a single
manifest along with audio.  
You should start with the manifest of the highest resolution as template. But this is not a
requirement. As long as `<AdaptationSet>` arguments `maxWidth` and `maxHeight` is correct
there is no problem.  
Then you should copy the whole `<Representation>` tag. Don't forget to change the ids.  
For audio instead of copying just the `<Representation>` you should copy the entire
`<AdaptationSet>`. You should copy it under `<Period>` not `<AdaptationSet>`
