# Video Editing Automation Script

This script automates the process of creating a video by processing a series of clips, adding text captions, and combining them into a final output video. It leverages the `moviepy` library to handle various video editing tasks.

## Overview

The script performs the following key operations:

1. **Setup Configuration**: Defines the input clips, including file paths, start and end times, and text captions.
2. **Create Temporary Directory**: Sets up a directory to store intermediate video files.
3. **Process Clips**: Handles each clip by:
   - Reading the input file (video or image).
   - Adjusting video duration if needed.
   - Adding text captions.
   - Saving intermediate video files.
4. **Concatenate Videos**: Merges all intermediate videos into a single final video.
5. **Resize and Render**: Adjusts the resolution of the final video based on the selected quality.
6. **Cleanup**: Deletes temporary files created during the process.

## Requirements

Ensure you have the following Python packages installed:

- `moviepy`
- `pillow - 8.4.0`
- `ffmpeg`
- `imagemagick`

You can install it using pip:

```bash
pip3 install moviepy,ffmpeg
pip3 install pillow==8.4.0
```

You might also need ffmpeg, imagemagick to be installed. Please follow steps available online based on your machine.

## Configuration

### 1. Clips Information

The `clips_info` list contains details about each clip to be processed:

- `file`: The path to the video or image file.
- `start`: The start time of the clip in `HH:MM:SS,MS` format.
- `end`: The end time of the clip in `HH:MM:SS,MS` format.
- `text`: The text caption to be added to the clip.

Example:

```python
clips_info = [
    {
        "file": "bernie.jpg",
        "start": "00:00:00,000",
        "end": "00:00:03,500",
        "text": "Hello, and welcome back to our podcast! I'm your host, Bernie."
    },
    ...
]
```

### 2. Media Path

Set the `mediaPath` variable to the directory where your media files are located:

```python
mediaPath = "/path/to/your/media"
```

Ensure this path is accurate and points to the directory containing your video and image files.

### 3. Video Quality

The `video_quality` dictionary allows you to select the desired resolution and bitrate for the output video. Options are:

- `low`: 640x360 resolution, 500k bitrate
- `medium`: 1280x720 resolution, 1500k bitrate
- `high`: 1920x1080 resolution, 3000k bitrate

Select the quality by setting `selected_quality`:

```python
selected_quality = "medium"
```

## Script Workflow

### Step 1: Create Temporary Directory

A temporary directory is created to store intermediate video files. This helps in organizing the files during processing.

```python
temp_dir = os.path.join(mediaPath, "temp_videos")
os.makedirs(temp_dir, exist_ok=True)
```

### Step 2: Process Each Clip

For each clip:

- Determine the duration based on the `start` and `end` times.
- If the input file is a video, adjust its duration if it’s shorter than required. For shorter videos, loop or reverse them as needed.
- Add the text caption to the video.
- Save the intermediate video file in the temporary directory.

### Step 3: Concatenate Videos

All intermediate videos are combined into a final video using the `concatenate_videoclips` function:

```python
final_video = concatenate_videoclips(final_clips, method="compose")
```

### Step 4: Resize and Render

The final video is resized to match the selected quality and rendered as an MP4 file:

```python
final_video = final_video.resize(video_quality[selected_quality]['resolution'])
output_filename = "final_output.mp4"
final_video.write_videofile(output_filename, bitrate=video_quality[selected_quality]['bitrate'], codec='libx264', audio_codec='aac' if final_video.audio else None, threads=8)
```

### Step 5: Cleanup

The temporary directory and its contents are deleted to free up space:

```python
shutil.rmtree(temp_dir)
```

## Usage

1. Place your media files (videos and images) in the directory specified by `mediaPath`.
2. Update the `clips_info` list with your media file names, start and end times, and captions.
3. Run the script:

```bash
python3 script.py
```

4. The final video will be saved as `final_output.mp4` in the current working directory.

## Notes

- Ensure that the `moviepy` library is installed and accessible in your Python environment.
- The script assumes that media files are either `.mp4`, `.jpg`, or `.png`. Adjust the script for other formats if necessary.
- Intermediate files are stored temporarily and removed after processing.
