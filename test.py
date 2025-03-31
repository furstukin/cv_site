from data import NATO_CODE, MORSE_CODE, BRAILLE
from crossmorsepy import MorseAudio

my_word = input("Enter a word: ")

nato = [NATO_CODE[letter] if letter.isalpha() else letter for letter in my_word.upper()]
morse = [MORSE_CODE[letter] for letter in my_word.upper()]
braille = [BRAILLE[letter] for letter in my_word.lower()]
nato_sentence = ' '.join(nato).strip()
morse_sentence = '.'.join(morse).strip()
braille_sentence = ''.join(braille).strip()
print(f"NATO Phonetic:\n{nato_sentence}\n")
print(f"Morse Code:\n{morse_sentence}\n")
print(f"Braille:\n{braille_sentence}")

morse_audio = MorseAudio()

morse_audio.play_audio(my_word)
