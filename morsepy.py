"""
MIT License

Copyright (c) 2025 Dustin Bloomquist
 Credit to Silas Hayes-Williams as original source

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import winsound
import time

MORSE_DICT = {
    'a': '.-',
    'b': '-...',
    'c': '-.-.',
    'd': '-..',
    'e': '.',
    'f': '..-.',
    'g': '--.',
    'h': '....',
    'i': '..',
    'j': '.---',
    'k': '-.-',
    'l': '.-..',
    'm': '--',
    'n': '-.',
    'o': '---',
    'p': '.--.',
    'q': '--.-',
    'r': '.-.',
    's': '...',
    't': '-',
    'u': '..-',
    'v': '...-',
    'w': '.--',
    'x': '-..-',
    'y': '-.--',
    'z': '--..',
    '1': '.----',
    '2': '..---',
    '3': '...--',
    '4': '....-',
    '5': '.....',
    '6': '-....',
    '7': '--...',
    '8': '---..',
    '9': '----.',
    '0': '-----',
    '.': '.-.-.-',
    ',': '--..--',
    '?': '..--..',
    ':': '---...',
    ';': '_._._.',
    "'": '.----.',
    '"': '.-..-.',
    '(': '-.--.',
    ')': '-.--.-',
    '/': '-..-.',
    '-': '-....-',
    '=': '-...-',
    '+': '.-.-.',
    '!': '-.-.--',
    '×': '-..-',
    '@': '.--.-.',
    ' ': '/'
}


class Morsepy:

    @staticmethod
    def encrypt(morse:str):
        # Encrypts any string into morse
        # Only one string can be passed as an argument

        cipher = ''
        for char in morse:
            try:
                cipher += MORSE_DICT[char]
                cipher += ' '
            except KeyError:
                raise ValueError(f' Character "{char}" is not currently supported by morsepy')

        return cipher.strip()

    @classmethod
    def beep(cls, morse: str):
           # Outputs a series of varied length beeps for the morse of any english given,
           # this will only work on windows operating systems due to the winsound module being used

        for char in cls.encrypt(morse):

            if char == '.':
                winsound.Beep(850, 100)
                time.sleep(0.01)
            elif char == '-':
                winsound.Beep(850, 200)
                time.sleep(0.01)
            elif char == ' ' or char == '/':
                time.sleep(.4)