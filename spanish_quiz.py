import csv
import random

# Location of Spanish_Vocab.csv
filepath = r"C:\Users\danny\OneDrive\Documents\Spanish_Vocab.csv"

def get_vocabulary_words(filename):
    """
    Imports a CSV file with two columns and returns it as a list of dictionaries.
    Assumes the first row contains headers that will be used as dictionary keys.

    Each dictionary represents one vocabulary word with two keys:
        "spanish" : the Spanish word
        "english" : the English meaning
    """
    data = []
    with open(filename, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        # Clean the keys by stripping the BOM character if present
        fieldnames = [field.strip('\ufeff') for field in reader.fieldnames]
        reader.fieldnames = fieldnames
        for row in reader:
            # Create a new dictionary with cleaned keys
            cleaned_row = {key.strip('\ufeff'): value for key, value in row.items()}
            data.append(cleaned_row)
    return data


def generate_question(words, used_spanish_words):
    """
    Create one quiz question.

    Inputs:
        words               → the full vocabulary list
        used_spanish_words  → a set containing Spanish words already used in this session

    Output:
        a dictionary containing:
            spanish          → the Spanish word to display
            choices          → list of 4 English answer choices
            correct_index    → the number (1–4) of the correct answer
            correct_english  → the correct English meaning
    """

    # ---------------------------------------------------------
    # Build a list of words that have NOT been used yet.
    # The result is a list of dictionary objects.
    # ---------------------------------------------------------
    available_words = [
        word
        for word in words
        if word["spanish"] not in used_spanish_words
    ]

    # ---------------------------------------------------------
    # Choose the correct word for this question.
    # From available_words if not blank otherwise from full list
    # ---------------------------------------------------------
    if available_words:
        correct_word = random.choice(available_words)
    else:
        # Fallback in case all words have already been used.
        correct_word = random.choice(words)

    # ---------------------------------------------------------
    # Loop through every word in the vocabulary list and collect 
    # ONLY the English meanings that are not the correct answer.
    # ---------------------------------------------------------
    incorrect_pool = [
        word["english"]
        for word in words
        if word["english"] != correct_word["english"]
    ]

    # ---------------------------------------------------------
    # Select three incorrect answers from the pool.
    # ---------------------------------------------------------
    incorrect_choices = random.sample(incorrect_pool, 3)

    # ---------------------------------------------------------
    # Combine the incorrect answers with the correct answer.
    # ---------------------------------------------------------
    all_choices = incorrect_choices + [correct_word["english"]]

    # ---------------------------------------------------------
    # Shuffle the order of the choices so the correct answer
    # appears in a random position.
    # ---------------------------------------------------------
    random.shuffle(all_choices)

    # ---------------------------------------------------------
    # Determine which numbered option is correct.
    # ---------------------------------------------------------
    correct_index = all_choices.index(correct_word["english"]) + 1

    # ---------------------------------------------------------
    # Return all information needed as a dictionary so the 
    # calling code can access each piece of data by name.
    # ---------------------------------------------------------
    return {
        "spanish": correct_word["spanish"],
        "choices": all_choices,
        "correct_index": correct_index,
        "correct_english": correct_word["english"],
    }


def get_valid_user_choice():
    """
    Ask the user for input until a valid answer is entered.

    Valid inputs are the numbers 1, 2, 3, or 4.

    Returns:
        an integer (1–4)
    """

    # Infinite loop until a valid answer is returned.
    while True:

        # input() waits for the user to type something.
        # strip() removes leading/trailing whitespace.
        user_input = input("Your answer (1-4): ").strip()

        # Check whether the user entered a valid choice.
        if user_input in {"1", "2", "3", "4"}:
            # Convert the string to an integer before returning.
            return int(user_input)

        # If input is invalid, show a message and repeat the loop.
        print("Please enter 1, 2, 3, or 4.")


def ask_question(question_data, question_number, total_questions):
    """
    Display one quiz question, collect the answer,
    and return whether the user was correct.

    Returns:
        True  → correct answer
        False → incorrect answer
    """

    # Print the question number and total questions.
    print(f"\nQuestion {question_number}/{total_questions}")

    # Show the Spanish word the user must translate.
    print(f"What is the English meaning of '{question_data['spanish']}'?")

    # ---------------------------------------------------------
    # Display the four answer choices.
    # start=1 makes numbering begin at 1 instead of 0.
    # ---------------------------------------------------------
    for index, choice in enumerate(question_data["choices"], start=1):
        print(f"{index}. {choice}")

    # Ask the user to enter their answer.
    user_choice = get_valid_user_choice()

    # ---------------------------------------------------------
    # Check whether the user's choice matches the correct index.
    # ---------------------------------------------------------
    if user_choice == question_data["correct_index"]:
        print("Correct!")
        return True

    # If incorrect, display the correct answer.
    print(f"Incorrect. The correct answer is: {question_data['correct_english']}")
    return False

def number_questions():
    """
    Ask the user for input until a valid answer is entered.
    """
    # Total number of quiz questions.
    while True:
        total_questions = input("How many questions do you want: ").strip()
        if total_questions.isdigit():
            return int(total_questions)
        print("Please enter a number.")

def run_quiz():
    """
    Run a complete quiz session consisting of 10 questions.
    """

    # Load the vocabulary words.
    words = get_vocabulary_words(filepath)

    # Track how many answers the user gets correct.
    score = 0

    # A SET used to track Spanish words already used in this session.
    used_spanish_words = set()

    print("")
    print("Spanish Flashcard Game")
    print("Choose the correct English meaning for each Spanish word.")
    print("")
    # Get the number of questions
    total_questions = number_questions()

    # ---------------------------------------------------------
    # Main quiz loop.
    # ---------------------------------------------------------
    for question_number in range(1, total_questions + 1):

        # Generate a question using the vocabulary list.
        question_data = generate_question(words, used_spanish_words)

        # Record that this Spanish word has now been used.
        used_spanish_words.add(question_data["spanish"])

        # Ask the question and update score if correct.
        if ask_question(question_data, question_number, total_questions):
            score += 1

    # ---------------------------------------------------------
    # Calculate the final percentage score.
    # ---------------------------------------------------------
    percentage = (score / total_questions) * 100

    # Display the final results.
    print("\nQuiz complete!")
    print(f"Final score: {score}/{total_questions}")
    print(f"Percentage correct: {percentage:.1f}%")


# ---------------------------------------------------------
# This block ensures the quiz runs only when this file
# is executed directly, not when imported as a module.
# ---------------------------------------------------------
if __name__ == "__main__":
    run_quiz()
