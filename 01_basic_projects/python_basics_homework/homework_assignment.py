# Python Basics Homework Assignment for Theo
# Instructions: Add comments above any code that demonstrates the 7 Python concepts

# Use this format: # This is an example of: [CONCEPT NAME]. 
# The first example is filled in for you. 
# Make sure you add the concept above the line of code, not below it.
# Each code block may have multiple concepts.
# Indicate which part of the code is demonstrating the concept.

# This is an example of a: import
import random
# This is an example of a: import
import time


# This is an example of a: VARIABLE (student_name)
# This is an example of: STRING (Theo)
student_name = "Theo"

# This is an example of a: VARIABLE 
# This is an example of: STRING
student_name = "Your Name Here"

# Now continue defining each concept above the code block that uses it.

# Welcome message
# This is an example of a: VARIABLE 
# This is an example of: STRING
welcome_message = "Welcome to Python Basics Practice!"

# 2.
# This is an example of a: function
def display_welcome():
    print("=" * 40)
    print(welcome_message)
    print(f"Student: {student_name}")
    print("=" * 40)
# This is an example of a: function
def guess_the_number():
    # This is an example of a: VARIABLE 
    secret_number = random.randint(1, 10)
    # This is an example of a: VARIABLE 
    attempts = 0
    # This is an example of a: VARIABLE 
    max_attempts = 3
    
    print("\nLet's play a guessing game!")
    print("I'm thinking of a number between 1 and 10")
    print(f"You have {max_attempts} attempts to guess it!")
    
    while attempts < max_attempts:
        try:
            # This is an example of a: string and variable
            guess = int(input(f"\nAttempt {attempts + 1}: Enter your guess: "))
            attempts += 1
            # This is an example of a: if statement
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
# This is an example of a: function
# This is an example of a: VARIABLE 
# This is an example of: list
def analyze_scores():
    test_scores = [85, 92, 78, 96, 88, 73, 91]
    subject_names = ["Math", "Science", "English", "History", "Art", "PE", "Music"]
    
    print("\n--- Grade Analysis ---")
    print("Subject Scores:")
    # This is an example of a: loop
    # This is an example of a: VARIABLE 

    for i in range(len(test_scores)):
        score = test_scores[i]
        subject = subject_names[i]
        # This is an example of a: if statement
        if score >= 90:
             # This is an example of a: VARIABLE 
             # This is an example of: STRING
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
 # This is an example of a: VARIABLE 
 # This is an example of: STRING      
        print(f"{subject}: {score}% (Grade: {grade_letter}) - {performance}")
    
    average_score = sum(test_scores) / len(test_scores)
    print(f"\nOverall average: {average_score:.1f}%")
# This is an example of a: function
def countdown_timer():
    countdown_message = "Get ready for the next activity!"
    print(f"\n{countdown_message}")
    # This is an example of a: loop
    for seconds in range(5, 0, -1):
        print(f"Starting in {seconds}...")
        time.sleep(1)
    
    print("Let's go! 🚀")
# This is an example of a: function
# This is an example of a: VARIABLE 
 # This is an example of: list     
def main():
    display_welcome()
    
    activities = ["Number Guessing Game", "Grade Analysis", "Countdown Timer"]
    
    print("\nToday's activities:")
    # This is an example of a: loop
    for activity in activities:
        print(f"- {activity}")
    
    countdown_timer()
     # This is an example of a: if statement   
    if guess_the_number():
        success_message = "Great job on the guessing game!"
        print(success_message)
    
    analyze_scores()
    # This is an example of a: string
    completion_message = "Homework assignment completed!"
    print(f"\n{completion_message}")
    print("Don't forget to add your comments identifying the Python concepts!")
# This is an example of a: if statement   
if __name__ == "__main__":
    main()
