# Video Editing Automation Script - Docker Guide

This script automates the process of creating a video by processing a series of clips, adding text captions, generating audio from text, and combining them into a final output video. The Docker setup encapsulates all dependencies, ensuring consistent and reproducible results across different environments.

## Overview

The Docker container handles the following key operations:

1. **Configuration Setup**: Reads the `config.json` file that defines the input clips, file paths, start and end times, text captions, and other settings.
2. **Media Processing**: Processes each clip based on the configurations provided:
   - Reads the input video or image files.
   - Adjusts video duration if needed.
   - Adds text captions and audio.
   - Saves intermediate files.
3. **Video Concatenation**: Merges all processed clips into a final video.
4. **Final Rendering**: Adjusts the video quality and orientation before saving the final output.
5. **Cleanup**: Removes temporary files after processing.

## Configuration

### 1. `config.json`

The `config.json` file contains all the necessary configurations for the script to run. Here’s an example structure:

```json
{
    "mediaPath": "/usr/src/app/media_files",
    "output_dir": "rendered",
    "temp_dir": "temp_videos",
    "selected_quality": "medium",
    "orientation": "Portrait",
    "clips_info": [
      {
        "file": "bernie.jpg",
        "start": "00:00:00.000",
        "end": "00:00:5.500",
        "text": "Hello, and welcome back to our podcast! I'm your host, Bernie.",
        "voice": "english-north"
      },
      {
        "file": "jessica_zoom_out.mp4",
        "start": "00:00:5.500",
        "end": "00:00:9.500",
        "text": "And I'm Jessica, here to crack the tough codes!",
        "voice": "english_rp"
      },
      {
        "file": "bernie_zoom_out.mp4",
        "start": "00:00:9.500",
        "end": "00:00:14.377",
        "text": "Don't forget about me, Frank, with the latest gadget news.",
        "voice": "english_wmids"
      },
      {
        "file": "all_slide_right.mp4",
        "start": "00:00:14.377",
        "end": "00:00:19.517",
        "text": "Together, we bring you the latest and greatest in tech!",
        "voice":"english-us"
      }
    ]
}
```

### Attributes:
- **`mediaPath`**: Directory containing your media files.
- **`output_dir`**: Directory where the final video will be saved.
- **`temp_dir`**: Directory for storing intermediate files during processing.
- **`selected_quality`**: Desired output video quality (`low`, `medium`, `high`).
- **`orientation`**: Video orientation (`Portrait`, `Landscape`).
- **`clips_info`**: List of dictionaries, each containing:
  - `file`: Path to the media file.
  - `start` & `end`: Clip start and end times.
  - `text`: Caption text.
  - `voice`: Voice selection for text-to-speech. 

## Docker Instructions

### 1. Install Docker

Ensure Docker is installed on your machine. For Windows, follow the [official Docker installation guide](https://docs.docker.com/desktop/install/windows-install/).

### 2. Build the Docker Image

Navigate to the directory containing the `Dockerfile` and run the following command to build the Docker image:

```bash
docker build -t video-editing-automation .
```

### 3. Prepare Your Media Files and Configuration

Ensure your media files are in a folder, e.g., `media_files`, and the `config.json` file is in the same directory.

### 4. Run the Docker Container

Use the following command to run the Docker container, ensuring that you map the `media_files` directory correctly:

```bash
docker run -v $(pwd)/media_files:/usr/src/app/media_files -v $(pwd)/config.json:/usr/src/app/config.json video-editing-automation
```

### 5. Output

The final rendered video will be saved in the `rendered` folder within the `media_files` directory.

## Notes

- Ensure the `config.json` file path is correctly specified in the `docker run` command.
- If you encounter intermittent errors, rerunning the container usually resolves the issue.
- The script assumes your media files are in the `.mp4`, `.jpg`, or `.png` format. Adjust the script if other formats are required.