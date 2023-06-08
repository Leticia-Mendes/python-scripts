import random
import hangman_art
import hangman_words

print(hangman_art.logo)

random_word = random.choice(hangman_words.word_list)
len_word = len(random_word)

blank = []
for letter in random_word:
    blank.append("_ ")

blank_join = (print(' '.join(blank)))

live = 7
while live >= 0:
    guess = input("\nGuess a letter: ").lower()
    
    for position in range(len_word):
        letter = random_word[position]
        if letter == guess:
            blank[position] = guess

    blank_join = (' '.join(blank))
    print(blank_join)
    
    guessed = (''.join(blank))
    if guessed == random_word:
        print("Congratulations")
        break
    
    if not guess in random_word:
        live -= 1
        print(f"Letter {guess} is not in the word")
        print(hangman_art.stages[live])
        if live == 0:
            print(f"GAME OVER.")
            print(f"The word was {random_word}")
            break
