from data import MORSE_AUDIO_DICT
import subprocess
import time
import logging
import os
import platform

logging.basicConfig(level=logging.DEBUG)

import subprocess
import platform
import os

def get_ffmpeg_path():
    try:
        # Dynamically locate ffmpeg path
        if platform.system() == "Windows":
            # Use `where` on Windows
            ffmpeg_path = subprocess.check_output(["where", "ffmpeg"]).decode().strip()
        else:
            # Use `which` on Unix-based systems
            ffmpeg_path = subprocess.check_output(["which", "ffmpeg"]).decode().strip()

        print(f"FFmpeg path: {ffmpeg_path}", flush=True)
        return ffmpeg_path
    except subprocess.CalledProcessError:
        # Fallback or error message
        raise RuntimeError("FFmpeg is required but not found in PATH.")

class MorseAudio:
    @classmethod
    def play_audio(cls, text_to_encode: str):
        for char in text_to_encode.lower():
            if char in MORSE_AUDIO_DICT:
                m_char = MORSE_AUDIO_DICT[char]
                audio_file = f'static/audio/morse_code/32-bit/{m_char}.mp3'

                # Validate file existence
                if not os.path.exists(audio_file):
                    logging.error(f"Audio file not found: {audio_file}")
                    raise FileNotFoundError(f"File does not exist: {audio_file}")

                logging.debug(f"Playing audio file: {m_char}.mp3")  # Debug testing
                ffmpeg_path = get_ffmpeg_path()
                result = subprocess.run([ffmpeg_path, "-nodisp", "-autoexit", audio_file], capture_output=True,
                                        text=True)

                print(f"Running FFplay for file: {audio_file}", flush=True)
                print(f"FFplay stdout: {result.stdout if result.stdout else 'No output'}", flush=True)
                print(f"FFplay stderr: {result.stderr if result.stderr else 'No errors'}", flush=True)

                time.sleep(0.5)  # Adjust delay after playback
            time.sleep(0.1)  # Delay between characters