# Python Basics Homework Assignment for Theo
# Instructions: Add comments above any code that demonstrates the 7 Python concepts

# Use this format: # This is an example of: [CONCEPT NAME]. 
# The first example is filled in for you. 
# Make sure you add the concept above the line of code, not below it.
# Each code block may have multiple concepts.
# Indicate which part of the code is demonstrating the concept.

import random
import time


# This is an example of a: VARIABLE (student_name)
# This is an example of: STRING (Theo)
student_name = "Theo"

# Student's name (you can change this)
student_name = "Your Name Here"

# Now continue defining each concept above the code block that uses it.

# Welcome message
welcome_message = "Welcome to Python Basics Practice!"

# 2.
def display_welcome():
    print("=" * 40)
    print(welcome_message)
    print(f"Student: {student_name}")
    print("=" * 40)

def guess_the_number():
    secret_number = random.randint(1, 10)
    attempts = 0
    max_attempts = 3
    
    print("\nLet's play a guessing game!")
    print("I'm thinking of a number between 1 and 10")
    print(f"You have {max_attempts} attempts to guess it!")
    
    while attempts < max_attempts:
        try:
            guess = int(input(f"\nAttempt {attempts + 1}: Enter your guess: "))
            attempts += 1
            
            if guess == secret_number:
                print("🎉 Congratulations! You guessed it!")
                return True
            elif guess < secret_number:
                print("Too low! Try again.")
            else:
                print("Too high! Try again.")
                
        except ValueError:
            print("Please enter a valid number!")
            
    print(f"\nGame over! The number was {secret_number}")
    return False

def analyze_scores():
    test_scores = [85, 92, 78, 96, 88, 73, 91]
    subject_names = ["Math", "Science", "English", "History", "Art", "PE", "Music"]
    
    print("\n--- Grade Analysis ---")
    print("Subject Scores:")
    
    for i in range(len(test_scores)):
        score = test_scores[i]
        subject = subject_names[i]
        
        if score >= 90:
            grade_letter = "A"
            performance = "Excellent!"
        elif score >= 80:
            grade_letter = "B"
            performance = "Good job!"
        elif score >= 70:
            grade_letter = "C"
            performance = "Keep trying!"
        else:
            grade_letter = "D"
            performance = "Need improvement"
            
        print(f"{subject}: {score}% (Grade: {grade_letter}) - {performance}")
    
    average_score = sum(test_scores) / len(test_scores)
    print(f"\nOverall average: {average_score:.1f}%")

def countdown_timer():
    countdown_message = "Get ready for the next activity!"
    print(f"\n{countdown_message}")
    
    for seconds in range(5, 0, -1):
        print(f"Starting in {seconds}...")
        time.sleep(1)
    
    print("Let's go! 🚀")

def main():
    display_welcome()
    
    activities = ["Number Guessing Game", "Grade Analysis", "Countdown Timer"]
    
    print("\nToday's activities:")
    for activity in activities:
        print(f"- {activity}")
    
    countdown_timer()
    
    if guess_the_number():
        success_message = "Great job on the guessing game!"
        print(success_message)
    
    analyze_scores()
    
    completion_message = "Homework assignment completed!"
    print(f"\n{completion_message}")
    print("Don't forget to add your comments identifying the Python concepts!")

if __name__ == "__main__":
    main()
