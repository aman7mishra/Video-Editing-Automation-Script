import os
import shutil
import json
from moviepy.editor import VideoFileClip, concatenate_videoclips,\
                           TextClip, CompositeVideoClip, ImageClip,\
                           AudioFileClip, afx, AudioClip, concatenate_audioclips
import moviepy.video.fx.all as vfx
import audio_module


# Load the configuration from the JSON file
with open("/usr/src/app/config.json", 'r') as config_file:
    config = json.load(config_file)

audio_generator = audio_module.AudioGenerator()

# Function to split and fit the text within the video frame
def split_text(clip_info, max_width, max_fontsize, duration):
    wrapped_text = TextClip(clip_info['text'], fontsize=max_fontsize, color='white', font="Arial-Bold", stroke_color='black', stroke_width=2)
    wrapped_text = wrapped_text.resize(width=max_width)  # Resizes while maintaining aspect ratio
    return wrapped_text.set_duration(duration).set_position(('center', 'bottom'))

# Function to parse time in HH:MM:SS.SSS format to seconds
def parse_time(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)

def create_silence(duration):
    return AudioClip(lambda t: [0], duration=duration)


# Extract configuration
mediaPath = config['mediaPath']
output_dir = os.path.join(mediaPath, config['output_dir'])
temp_dir = os.path.join(mediaPath, config['temp_dir'])
selected_quality = config['selected_quality']
orientation = config['orientation']
clips_info = config['clips_info']

if orientation == "Portrait":
    video_quality = {
        "low": {"resolution": (360, 640), "bitrate": "500k"},
        "medium": {"resolution": (720, 1280), "bitrate": "1500k"},
        "high": {"resolution": (1080, 1920), "bitrate": "3000k"},
        "custom": {"resolution": (2160, 3840), "bitrate": "1000k"}
    }
else:
    video_quality = {
        "low": {"resolution": (640, 360), "bitrate": "500k"},
        "medium": {"resolution": (1280, 720), "bitrate": "1500k"},
        "high": {"resolution": (1920, 1080), "bitrate": "3000k"},
        "custom": {"resolution": (3840, 2160), "bitrate": "1000k"}
    }

# Create directories if they don't exist
os.makedirs(temp_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)
output_filename = os.path.join(output_dir, "final_output.mp4")

# List to hold final video clips
final_clips = []

audio_files = []

# Generating Audio
print("Generating Audio files for the clips")
for i, clip_info in enumerate(clips_info):
    audio_generator.save_speech(
        clip_info['text'],
        os.path.join(temp_dir, f"audio_{i}.wav"),
        clip_info['voice']
    )
    audio_files.append(os.path.join(temp_dir, f"audio_{i}.wav"))
audio_generator.commit()

for file in audio_files:
    audio_module.wait_for_file(file)
print("Completed generation of Audio files for the clips")

# Process each clip
for i, clip_info in enumerate(clips_info):
    print("Processing - ", clip_info["file"])
    input_file = os.path.join(mediaPath, clip_info["file"])

    start_time = parse_time(clip_info['start'])
    end_time = parse_time(clip_info['end'])
    duration = end_time - start_time

    audio_clip = AudioFileClip(audio_files[i])

    if audio_clip.duration < duration:
        print("Audio shorter than the video clip. Adding silence to the clip")
        silence_duration = 5
        silence = create_silence(silence_duration)
        audio_clip = concatenate_audioclips([audio_clip, silence])
    elif audio_clip.duration > duration:
        print("Audio longer than the video clip. Please decrease the video length or lengthen the audio")
    
    audio_clip = audio_clip.set_duration(duration)

    if input_file.endswith(('.mp4', '.mov', '.avi', '.mkv')):
        video = VideoFileClip(input_file)
        video = video.without_audio()

        if video.duration < duration:
            print("The video file provided is shorter than the script duration.")
            #  --------  Uncomment the following lines to enable following. ------------
            # If video is shorter than required, loop and reverse it to fit duration
            # looped_clip = vfx.loop(video, duration=duration)
            # looped_clip = video.fx(vfx.loop, duration=duration)
            # reversed_clip = looped_clip.fx(vfx.time_mirror).subclip(0, duration)
            # video = concatenate_videoclips([looped_clip, reversed_clip])
            # print(f"Video {clip_info['file']} was too short. Extended and reversed to match duration {duration} seconds.")
        else:
            video = video.subclip(0, min(duration, video.duration))
            print(f"Video {clip_info['file']} trimmed to {duration} seconds.")

    elif input_file.endswith(('.png', '.jpg', '.jpeg')):
        video = ImageClip(input_file).set_duration(duration)
        print(f"Image {clip_info['file']} has been converted to a video clip with duration {duration} seconds.")

    else:
        print(f"File {clip_info['file']} is not supported.")
        continue

    video = video.resize(height=video_quality[selected_quality]['resolution'][1],
                         width=video_quality[selected_quality]['resolution'][0])
    video = video.on_color(size=video_quality[selected_quality]['resolution'], color=(0, 0, 0), pos='center')

    # Add text as a caption
    max_width = 0.9 * video.size[0]
    max_fontsize = 70
    text_clip = split_text(clip_info, max_width, max_fontsize, duration)
    video_with_text_and_audio = CompositeVideoClip([video, text_clip]).set_audio(audio_clip)

    # Add the processed clip to the list
    final_clips.append(video_with_text_and_audio)

# Concatenate all the clips videos
final_video = concatenate_videoclips(final_clips, method="compose")

# Resize and render the final video
final_video = final_video.resize(video_quality[selected_quality]['resolution'])
final_video.write_videofile(output_filename, bitrate=video_quality[selected_quality]['bitrate'], codec='libx264', audio_codec='aac', threads=8)

# Cleanup intermediate files
shutil.rmtree(temp_dir)

print("Video processing completed and intermediate files cleaned up.")
