import wordle
import random

answer = wordle.answer

# best_guess = wordle.select_best_guess(wordle.wordle_all_guesses, wordle.wordle_word_list)
# print(best_guess)
best_guess = "soare"

# feedback = wordle.get_feedback(best_guess, answer)
# print(feedback)

def filter_words(word_list, guess, feedback):
    def matches_feedback(word):
        return wordle.get_feedback(guess, word) == feedback

    return [word for word in word_list if matches_feedback(word)]

def wordle_solver(answer):
    word_list = wordle.wordle_all_guesses
    attempts = 0

    while attempts < 20:
        if attempts == 0:
            guess = "tarse"
        else:
            guess = wordle.select_best_guess(word_list, wordle.wordle_word_list)
        feedback = wordle.get_feedback(guess, answer)
        # print(f"Attempt {attempts + 1}: Guess = {guess}, Feedback = {feedback}")
        
        if feedback == "GGGGG":
            # print("Solved!")
            return(attempts)
        
        word_list = filter_words(word_list, guess, feedback)
        attempts += 1

    if attempts == 20 and feedback != "GGGGG":
        print("Failed to guess the word.")


def wordle_solver():
    word_list = wordle.wordle_all_guesses
    attempts = 0

    while attempts < 20:
        if attempts == 0:
            guess = "soare"
        else:
            guess = wordle.select_best_guess(word_list, wordle.wordle_word_list)

        feedback = str.upper(str(input("Give the feedback for " + str(guess) + ": ")))
        if feedback == "N":
            word_list.remove(guess)
            continue
        
        if feedback == "GGGGG":
            print("Solved!")
            return(attempts)
        
        word_list = filter_words(word_list, guess, feedback)
        # print(word_list)
        attempts += 1

    if attempts == 20 and feedback != "GGGGG":
        print("Failed to guess the word.")

wordle_solver()

# total_attempts = 0

# for i in range(0, 100):
#     answer = random.choice(wordle.wordle_word_list)
#     attempts = wordle_solver(answer)
#     print(attempts)
#     total_attempts += attempts
# average = total_attempts / 100
# print(average)
