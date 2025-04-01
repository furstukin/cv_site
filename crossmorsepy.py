from data import MORSE_AUDIO_DICT
import pygame
import time

class MorseAudio:
    @classmethod
    def play_audio(cls, text_to_encode: str):
        pygame.mixer.init(frequency=22050)  # Initialize the Pygame mixer
        for char in text_to_encode.lower():
            if char in MORSE_AUDIO_DICT:
                m_char = MORSE_AUDIO_DICT[char]
                audio_file = f'static/audio/morse_code/32-bit/{m_char}.mp3'
                pygame.mixer.music.load(audio_file)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    time.sleep(0.25)  # Wait for audio to finish playing
            time.sleep(0.1)

