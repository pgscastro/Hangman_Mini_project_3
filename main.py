import random
import inquirer


# score tracker
# add score
# number of wins
# number of defeats
# create if not exists
def read_stats():
    try:
        with open('score_tracker.txt', 'r') as score_tracker:
            stats = score_tracker.read().strip().split(',')
            score = int(stats[0])
            wins = int(stats[1])
            failures = int(stats[2])
    except FileNotFoundError:
        score = 0
        wins = 0
        failures = 0
    return score, wins, failures


score, wins, failures = read_stats()


def write_stats(score, wins, failures):
    with open('score_tracker.txt', 'w') as score_tracker:
        score_tracker.write(f"{score},{wins},{failures}")


# create a word list
# updated to select difficulty
print("Welcome to Hangman!")

questions = [
    inquirer.List(
        "difficulty",
        message="Choose the difficulty",
        choices=["Hard", "Classic", "Easy"],
    ),
]
answers = inquirer.prompt(questions)
# print(answers)
if answers["difficulty"] == "Hard":
    with open('short.txt', 'r') as hard:
        word_list = hard.read().splitlines()
        word_list = [i for i in word_list if len(i) >= 4]
elif answers['difficulty'] == 'Classic':
    with open('medium.txt', 'r') as classic:
        word_list = classic.read().splitlines()
else:
    with open('long.txt', 'r') as easy:
        word_list = easy.read().splitlines()

# create a random word picker
rword = random.choice(word_list)

# find the size of the word
size = len(rword)

# separate it into letters
# print([*list[rword]])
# create '_'
hangman = ['_'] * size
# print(hangman)
print("Current word: " + ' '.join(hangman))


# get user input
# compare with the word list
# handle exceptions
def guess():
    while True:
        user_guess = input("Guess a letter: ").lower()
        if len(user_guess) == 1 and user_guess.isalpha():
            if user_guess in guessed_letters:
                print("You have already guessed that letter. Try again.")
            else:
                guessed_letters.append(user_guess)
                return user_guess
        else:
            print("You need to enter a letter.")


# display and count how many guesses
guesses_remaining = 6
guessed_letters = []

while '_' in hangman and guesses_remaining > 0:
    user_input = guess()
    positions = [i for i, char in enumerate(rword) if char == user_input]
    if positions:
        for i in positions:
            hangman[i] = user_input
        print(f"Good job! {user_input} is in the word!")
    else:
        print(f"Sorry, {user_input} is not in the word.")
        guesses_remaining -= 1
    print("Current word: " + ' '.join(hangman))
    print(f"Guesses: {guesses_remaining}, Guessed letters: {', '.join(guessed_letters)}")

# message ending the game
if '_' not in hangman:
    print(f"Congratulations! You guessed the word: {rword}")
    wins += 1
    score += 10 + 2 * guesses_remaining
else:
    print(f"Game over! The word was: {rword}")
    failures += 1
    score += 1

# write status in file
write_stats(score, wins, failures)
print(f"Your current score is: {score}")
print(f"Victories: {wins}")
print(f"Failed attempts: {failures}")
