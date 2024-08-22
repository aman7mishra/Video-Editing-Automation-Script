# Video Editing Automation Script - Docker

This Docker-based script automates the creation of a video by processing clips, adding text captions and audio, and concatenating them into a final output video. It utilizes the `moviepy` library and is designed to run within a Docker container for consistency and ease of use.

## Overview

The script performs the following key tasks:

1. **Configuration Setup:** Reads settings from the `config.json` file, which includes paths, video quality, and clip details.
2. **Create Temporary Directory:** Sets up a directory for storing intermediate video files.
3. **Process Clips:** Handles each clip by reading the input file, adjusting duration, adding text captions and audio, and saving intermediate files.
4. **Concatenate Videos:** Merges intermediate videos into a final output video.
5. **Resize and Render:** Adjusts video resolution based on selected quality and orientation.
6. **Cleanup:** Removes temporary files created during the process.

## Usage

For detailed instructions on how to configure and run the Docker container, please refer to the [HowToUse.md](HowToUse.md) file.
