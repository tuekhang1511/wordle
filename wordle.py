# import requests
# from bs4 import BeautifulSoup

# def scrape_wordle_words(url):
#     response = requests.get(url)
#     if response.status_code == 200:
#         soup = BeautifulSoup(response.text, "html.parser")
        
#         # Find all divs that contain the word lists
#         word_list_sections = soup.find_all("div", {"class": "light-box text-left"})  # Adjust class if needed
        
#         words = []
#         for section in word_list_sections:
#             # Extract words within the <ul><li><a> structure
#             word_elements = section.select("ul li a")
#             words.extend([element.text.strip() for element in word_elements])
        
#         # Save to file
#         with open("wordle_word_list.txt", "w") as file:
#             file.write("\n".join(words))
        
#         print(f"Scraped {len(words)} words and saved to wordle_word_list.txt.")
#         return words
#     else:
#         print(f"Failed to fetch webpage: {response.status_code}")
#         return []

# # URL of the word list
# wordle_url = "https://www.wordunscrambler.net/word-list/wordle-word-list"
# wordle_words = scrape_wordle_words(wordle_url)

# def fetch_wordle_gist(gist_url):
#     response = requests.get(gist_url)
#     if response.status_code == 200:
#         words = response.text.splitlines()
        
#         # Save to file
#         with open("wordle_all_guesses.txt", "w") as file:
#             file.write("\n".join(words))
        
#         print(f"Fetched {len(words)} words from GitHub gist and saved to wordle_all_guesses.txt.")
#         return words
#     else:
#         print(f"Failed to fetch gist: {response.status_code}")
#         return []

# # URL of the GitHub gist
# gist_url = "https://gist.githubusercontent.com/dracos/dd0668f281e685bad51479e5acaadb93/raw"
# all_possible_guesses = fetch_wordle_gist(gist_url)

import math
import random

# Get word lists from file
def load_word_list(file_path):
    with open(file_path, "r") as file:
        # Adjust split logic based on your file format
        return file.read().splitlines()  # For words on separate lines

wordle_word_list = load_word_list("wordle_word_list.txt")
wordle_all_guesses = load_word_list("wordle_all_guesses.txt")
print(f"Loaded {len(wordle_word_list)} words.")
print(f"Loaded {len(wordle_all_guesses)} words.")

# Get a random word
answer = random.choice(wordle_word_list)


def get_feedback(guess, answer):
    feedback = []
    green_letters = []  
    # First pass: Handle greens
    for index, (g, a) in enumerate(zip(guess, answer)):
        if g == a:
            feedback.append("G")  # Green
            green_letters.append(g)
        else:
            feedback.append("")  # Placeholder for now

    # Second pass: Handle yellows and grays
    for index, g in enumerate(guess):
        if feedback[index] == "G":  # Skip already marked greens
            continue
        if g in answer:
            if answer.count(g) > green_letters.count(g):
                feedback[index] = "Y"  # Yellow
                green_letters.append(g)
            else:
                feedback[index] = "B"  # Gray (duplicate yellow case)
        else:
            feedback[index] = "B"  # Gray

    return "".join(feedback)


def calculate_entropy(guess, answer_list):
    all_feedback = {}
    for word in answer_list:
        feedback = get_feedback(guess, word)
        if feedback in all_feedback:
            all_feedback[feedback] += 1
        else:
            all_feedback[feedback] = 1

    total = len(answer_list)
    # print(all_feedback)
    entropy = 0
    for feedback in all_feedback:
        prob = all_feedback[feedback] / total
        entropy -= prob * math.log2(prob)

    return entropy

def select_best_guess(word_list, answer_list):
    best_guess = None
    best_entropy = -1
    for guess in word_list:
        entropy = calculate_entropy(guess, answer_list)
        if entropy > best_entropy:
            best_entropy = entropy
            best_guess = guess
            # print(best_entropy)
    return best_guess


