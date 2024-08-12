import os
import shutil
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip, CompositeVideoClip, ImageClip
import moviepy.video.fx.all as vfx

# Function to split and fit the text within the video frame
def split_text(clip_info, max_width, max_fontsize, duration):
    wrapped_text = TextClip(clip_info['text'], fontsize=max_fontsize, color='white', stroke_color='black', stroke_width=2)
    wrapped_text = wrapped_text.resize(width=max_width)  # Resizes while maintaining aspect ratio
    return wrapped_text.set_duration(duration).set_position(('center', 'bottom'))

# Configuration
clips_info = [
    {
        "file": "bernie.jpg",
        "start": "00:00:00,000",
        "end": "00:00:3,500",
        "text": "Hello, and welcome back to our podcast! I'm your host, Bernie."
    },
    {
        "file": "jessica_zoom_out.mp4",
        "start": "00:00:3,500",
        "end": "00:00:7,114",
        "text": "And I'm Jessica, here to crack the tough codes!"
    },
    {
        "file": "bernie_zoom_out.mp4",
        "start": "00:00:7,114",
        "end": "00:00:10,177",
        "text": "Don't forget about me, Frank, with the latest gadget news."
    },
    {
        "file": "all_slide_right.mp4",
        "start": "00:00:10,177",
        "end": "00:00:15,217",
        "text": "Together, we bring you the latest and greatest in tech!"
    }
]

# Media Path
mediaPath = "<UPDATE>" # Add your media path


# Select video quality
video_quality = {
    "low": {"resolution": (640, 360), "bitrate": "500k"},
    "medium": {"resolution": (1280, 720), "bitrate": "1500k"},
    "high": {"resolution": (1920, 1080), "bitrate": "3000k"},
}
selected_quality = "medium"

# Create a temporary directory for intermediate files
temp_dir = os.path.join(mediaPath, "temp_videos")
os.makedirs(temp_dir, exist_ok=True)

intermediate_videos = []

# Process each clip
for i, clip_info in enumerate(clips_info):
    input_file = os.path.join(mediaPath, clip_info["file"])
    output_file = os.path.join(temp_dir, f"intermediate_{i}.mp4")

    # Determine the duration of the clip
    start_time = sum(int(x) * 60 ** i for i, x in enumerate(reversed(clip_info['start'].split(",")[0].split(":"))))
    end_time = sum(int(x) * 60 ** i for i, x in enumerate(reversed(clip_info['end'].split(",")[0].split(":"))))
    duration = end_time - start_time

    if input_file.endswith('.mp4'):
        video = VideoFileClip(input_file)

        # Check if video duration is less than required duration
        if video.duration < duration:
            # If video is shorter than required, loop and reverse it to fit duration
            looped_video = video.fx(vfx.loop, duration=duration)
            video = looped_video.subclip(0, duration)

            # Write the intermediate video file
            video = video.set_fps(60)
            video = video.without_audio()
             # Add text as a caption
            max_width = 0.9 * video.size[0]
            max_fontsize = 48
            text_clip = split_text(clip_info, max_width, max_fontsize, duration)
            video = CompositeVideoClip([video, text_clip])
            
            video.write_videofile(output_file, bitrate=video_quality[selected_quality]['bitrate'], codec='libx264', audio_codec='aac' if video.audio else None, threads=4)
            intermediate_videos.append(output_file)
            continue
        else:
            video = video.subclip(0, min(duration, video.duration))

    elif input_file.endswith('.jpg') or input_file.endswith('.png'):
        # For images, create a video with the image displayed for the duration
        video = ImageClip(input_file).set_duration(duration)

    # Add text as a caption
    max_width = 0.9 * video.size[0]
    max_fontsize = 48
    text_clip = split_text(clip_info, max_width, max_fontsize, duration)
    video = CompositeVideoClip([video, text_clip])

    # Store the intermediate video path
    intermediate_videos.append(video)

# Concatenate all the intermediate videos
final_clips = []
for clip in intermediate_videos:
    if isinstance(clip, str):
        final_clips.append(VideoFileClip(clip))
    else:
        final_clips.append(clip)

final_video = concatenate_videoclips(final_clips, method="compose")

# Resize and render the final video
final_video = final_video.resize(video_quality[selected_quality]['resolution'])
output_filename = "final_output.mp4"
final_video.write_videofile(output_filename, bitrate=video_quality[selected_quality]['bitrate'], codec='libx264', audio_codec='aac' if final_video.audio else None, threads=8)

# Cleanup intermediate files
shutil.rmtree(temp_dir)

print("Video processing completed and intermediate files cleaned up.")
