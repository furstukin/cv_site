from data import MORSE_AUDIO_DICT
import subprocess
import time
import logging

logging.basicConfig(level=logging.DEBUG)

def get_ffmpeg_path():
    try:
        ffmpeg_path = subprocess.check_output(["which", "ffmpeg"]).decode().strip()
        print(f"FFmpeg path: {ffmpeg_path}", flush=True)
        return ffmpeg_path
    except subprocess.CalledProcessError:
        raise RuntimeError("FFmpeg is not installed or not found in PATH")


class MorseAudio:
    @classmethod
    def play_audio(cls, text_to_encode: str):
        for char in text_to_encode.lower():
            if char in MORSE_AUDIO_DICT:
                m_char = MORSE_AUDIO_DICT[char]
                audio_file = f'static/audio/morse_code/32-bit/{m_char}.mp3'
                logging.debug(f"Playing audio file: {m_char}.mp3") # Debug testing
                print(f"Playing audio file: {m_char}.mp3", flush=True)
                ffmpeg_path = get_ffmpeg_path()
                result = subprocess.run([ffmpeg_path, "-nodisp", "-autoexit", audio_file], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(result.stdout, flush=True)
                print(result.stderr, flush=True)
                time.sleep(0.05)  # Short delay after playback
            time.sleep(0.1)  # Delay between characters