import pyttsx3
import time
import os

class AudioGenerator():
    def __init__(self) -> None:
        # Initialize the text-to-speech engine
        self.engine = pyttsx3.init()
        # Dictionary to store available voices
        self.voices_list = {}
        # Populate the dictionary with available voices
        self.get_voices()

    def get_voices(self):
        # Retrieve the available voices from the TTS engine
        voices = self.engine.getProperty('voices')
        for voice in voices:
            # Store the voice name and its corresponding ID in the dictionary
            self.voices_list[voice.name] = voice.id

    def save_speech(self, text, filename, voice_name):
        # Set the voice to be used for TTS based on the provided voice name
        self.engine.setProperty('voice', self.voices_list[voice_name])
        # Generate speech from text and save it to a file
        self.engine.save_to_file(text, filename)

    def commit(self):
        # Execute the queued commands (like saving speech to a file)
        self.engine.runAndWait()


# After generating the audio file, wait until it exists and is accessible
def wait_for_file(file_path, max_wait=10):
    """Wait for a file to exist with a timeout."""
    wait_time = 0
    while not os.path.exists(file_path) and wait_time < max_wait:
        time.sleep(0.5)  # Wait for 0.5 seconds before checking again
        wait_time += 0.5
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} could not be found after {max_wait} seconds")
