import random


def get_vocabulary_words():
    """Return the hardcoded Spanish vocabulary list."""
    return [
        {"spanish": "agua", "english": "water"},
        {"spanish": "casa", "english": "house"},
        {"spanish": "gato", "english": "cat"},
        {"spanish": "perro", "english": "dog"},
        {"spanish": "libro", "english": "book"},
        {"spanish": "escuela", "english": "school"},
        {"spanish": "comida", "english": "food"},
        {"spanish": "amigo", "english": "friend"},
        {"spanish": "familia", "english": "family"},
        {"spanish": "ciudad", "english": "city"},
        {"spanish": "coche", "english": "car"},
        {"spanish": "sol", "english": "sun"},
        {"spanish": "luna", "english": "moon"},
        {"spanish": "tiempo", "english": "time"},
        {"spanish": "mano", "english": "hand"},
    ]


def generate_question(words, used_spanish_words):
    """Create one quiz question with 1 correct and 3 incorrect choices."""
    available_words = [word for word in words if word["spanish"] not in used_spanish_words]

    if available_words:
        correct_word = random.choice(available_words)
    else:
        # Fallback if all words were used.
        correct_word = random.choice(words)

    incorrect_pool = [
        word["english"]
        for word in words
        if word["english"] != correct_word["english"]
    ]

    incorrect_choices = random.sample(incorrect_pool, 3)
    all_choices = incorrect_choices + [correct_word["english"]]
    random.shuffle(all_choices)

    correct_index = all_choices.index(correct_word["english"]) + 1

    return {
        "spanish": correct_word["spanish"],
        "choices": all_choices,
        "correct_index": correct_index,
        "correct_english": correct_word["english"],
    }


def get_valid_user_choice():
    """Ask until user enters 1, 2, 3, or 4."""
    while True:
        user_input = input("Your answer (1-4): ").strip()

        if user_input in {"1", "2", "3", "4"}:
            return int(user_input)

        print("Please enter 1, 2, 3, or 4.")


def ask_question(question_data, question_number, total_questions):
    """Display one question, get the answer, and return True/False for correctness."""
    print(f"\nQuestion {question_number}/{total_questions}")
    print(f"What is the English meaning of '{question_data['spanish']}'?")

    for index, choice in enumerate(question_data["choices"], start=1):
        print(f"{index}. {choice}")

    user_choice = get_valid_user_choice()

    if user_choice == question_data["correct_index"]:
        print("Correct!")
        return True

    print(f"Incorrect. The correct answer is: {question_data['correct_english']}")
    return False


def run_quiz():
    """Run a 10-question Spanish vocabulary quiz session."""
    words = get_vocabulary_words()
    total_questions = 10
    score = 0
    used_spanish_words = set()

    print("Spanish Vocabulary Quiz")
    print("Choose the correct English meaning for each Spanish word.")

    for question_number in range(1, total_questions + 1):
        question_data = generate_question(words, used_spanish_words)
        used_spanish_words.add(question_data["spanish"])

        if ask_question(question_data, question_number, total_questions):
            score += 1

    percentage = (score / total_questions) * 100

    print("\nQuiz complete!")
    print(f"Final score: {score}/{total_questions}")
    print(f"Percentage correct: {percentage:.1f}%")


if __name__ == "__main__":
    run_quiz()
