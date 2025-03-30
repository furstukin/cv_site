import pygame
import time
import numpy

MORSE_CODE_DICT = {
    'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.',
    'g': '--.', 'h': '....', 'i': '..', 'j': '.---', 'k': '-.-', 'l': '.-..',
    'm': '--', 'n': '-.', 'o': '---', 'p': '.--.', 'q': '--.-', 'r': '.-.',
    's': '...', 't': '-', 'u': '..-', 'v': '...-', 'w': '.--', 'x': '-..-',
    'y': '-.--', 'z': '--..', '1': '.----', '2': '..---', '3': '...--',
    '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..',
    '9': '----.', '0': '-----', ' ': '/'
}

pygame.init()
pygame.mixer.init(frequency=44100, size=-16, channels=1)  # Mono output
SND_FREQ = 1000  # Tone frequency in Hz
SND_TIME_UNIT = 0.1  # Base unit duration in seconds

def generate_wave(frequency, duration, sample_rate=44100):
    t = numpy.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = 0.5 * numpy.sin(2 * numpy.pi * frequency * t)  # Generate sine wave
    return (wave * 32767).astype(numpy.int16)  # Convert to 16-bit PCM format

import simpleaudio as sa

def play_tone(frequency, duration):
    sample_rate = 44100
    t = numpy.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    wave = 0.5 * numpy.sin(2 * numpy.pi * frequency * t)  # Sine wave
    audio = (wave * 32767).astype(numpy.int16).tobytes()  # Convert to bytes
    play_obj = sa.play_buffer(audio, 1, 2, sample_rate)  # Mono: channels=1, bytes=2
    play_obj.wait_done()


def play_morse(text):
    for char in text.lower():
        if char != ' ':
            for symbol in MORSE_CODE_DICT.get(char, ''):
                if symbol == '.':
                    play_tone(SND_TIME_UNIT)
                elif symbol == '-':
                    play_tone(SND_TIME_UNIT * 3)
                time.sleep(SND_TIME_UNIT)  # Gap between symbols
            time.sleep(SND_TIME_UNIT * 2)  # Gap between letters
        else:
            time.sleep(SND_TIME_UNIT * 6)  # Gap between words
    pygame.mixer.quit()

if __name__ == '__main__':
    text_to_encode = input("Enter text to convert to Morse code: ")
    play_morse(text_to_encode)
