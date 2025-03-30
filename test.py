from data import nato_code, morse_code, braille_code
from morsepy import Morsepy

my_word = input("Enter a word: ")

nato = [nato_code[letter] if letter.isalpha() else letter for letter in my_word.upper()]
morse = [morse_code[letter] for letter in my_word.upper()]
braille = [braille_code[letter] for letter in my_word.lower()]
nato_sentence = ' '.join(nato).strip()
morse_sentence = '.'.join(morse).strip()
braille_sentence = ''.join(braille).strip()
print(f"NATO Phonetic:\n{nato_sentence}\n")
print(f"Morse Code:\n{morse_sentence}\n")
print(f"Braille:\n{braille_sentence}")

morsepy = Morsepy()

morsepy.beep(my_word.lower())