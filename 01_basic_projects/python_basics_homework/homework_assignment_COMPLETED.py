# Python Basics Homework Assignment for Theo - COMPLETED EXAMPLE
# Instructions: Add comments above any code that demonstrates the 7 Python concepts

# Use this format: # This is an example of: [CONCEPT NAME]. The first example is filled in for you. 
# Make sure you add the concept above the line of code, not below it.
# Each code block may have multiple concepts.


import random
import time


# 1. This is an example of: VARIABLE
# 5. This is an example of: STRING
student_name = "Your Name Here"

# Now continue defining each concept above the code block that uses it.

# 1. This is an example of: VARIABLE
# 5. This is an example of: STRING
welcome_message = "Welcome to Python Basics Practice!"

# 2. This is an example of: FUNCTION
def display_welcome():
    print("=" * 40)
    print(welcome_message)
    print(f"Student: {student_name}")
    print("=" * 40)

# 2. This is an example of: FUNCTION
def guess_the_number():
    # 1. This is an example of: VARIABLE
    secret_number = random.randint(1, 10)
    # 1. This is an example of: VARIABLE
    attempts = 0
    # 1. This is an example of: VARIABLE
    max_attempts = 3
    
    # 5. This is an example of: STRING
    print("\nLet's play a guessing game!")
    # 5. This is an example of: STRING
    print("I'm thinking of a number between 1 and 10")
    # 5. This is an example of: STRING
    print(f"You have {max_attempts} attempts to guess it!")
    
    # 3. This is an example of: LOOP
    while attempts < max_attempts:
        try:
            # 1. This is an example of: VARIABLE
            # 5. This is an example of: STRING
            guess = int(input(f"\nAttempt {attempts + 1}: Enter your guess: "))
            attempts += 1
            
            # 4. This is an example of: IF STATEMENT
            if guess == secret_number:
                # 5. This is an example of: STRING
                print("🎉 Congratulations! You guessed it!")
                return True
            # 4. This is an example of: IF STATEMENT
            elif guess < secret_number:
                # 5. This is an example of: STRING
                print("Too low! Try again.")
            # 4. This is an example of: IF STATEMENT
            else:
                # 5. This is an example of: STRING
                print("Too high! Try again.")
                
        except ValueError:
            # 5. This is an example of: STRING
            print("Please enter a valid number!")
            
    # 5. This is an example of: STRING
    print(f"\nGame over! The number was {secret_number}")
    return False

# 2. This is an example of: FUNCTION
def analyze_scores():
    # 1. This is an example of: VARIABLE
    # 6. This is an example of: LIST
    test_scores = [85, 92, 78, 96, 88, 73, 91]
    # 1. This is an example of: VARIABLE
    # 6. This is an example of: LIST
    # 5. This is an example of: STRING
    subject_names = ["Math", "Science", "English", "History", "Art", "PE", "Music"]
    
    # 5. This is an example of: STRING
    print("\n--- Grade Analysis ---")
    # 5. This is an example of: STRING
    print("Subject Scores:")
    
    # 3. This is an example of: LOOP
    for i in range(len(test_scores)):
        # 1. This is an example of: VARIABLE
        score = test_scores[i]
        # 1. This is an example of: VARIABLE
        subject = subject_names[i]
        
        # 4. This is an example of: IF STATEMENT
        if score >= 90:
            # 1. This is an example of: VARIABLE
            # 5. This is an example of: STRING
            grade_letter = "A"
            # 1. This is an example of: VARIABLE
            # 5. This is an example of: STRING
            performance = "Excellent!"
        # 4. This is an example of: IF STATEMENT
        elif score >= 80:
            # 1. This is an example of: VARIABLE
            # 5. This is an example of: STRING
            grade_letter = "B"
            # 1. This is an example of: VARIABLE
            # 5. This is an example of: STRING
            performance = "Good job!"
        # 4. This is an example of: IF STATEMENT
        elif score >= 70:
            # 1. This is an example of: VARIABLE
            # 5. This is an example of: STRING
            grade_letter = "C"
            # 1. This is an example of: VARIABLE
            # 5. This is an example of: STRING
            performance = "Keep trying!"
        # 4. This is an example of: IF STATEMENT
        else:
            # 1. This is an example of: VARIABLE
            # 5. This is an example of: STRING
            grade_letter = "D"
            # 1. This is an example of: VARIABLE
            # 5. This is an example of: STRING
            performance = "Need improvement"
            
        # 5. This is an example of: STRING
        print(f"{subject}: {score}% (Grade: {grade_letter}) - {performance}")
    
    # 1. This is an example of: VARIABLE
    average_score = sum(test_scores) / len(test_scores)
    # 5. This is an example of: STRING
    print(f"\nOverall average: {average_score:.1f}%")

# 2. This is an example of: FUNCTION
def countdown_timer():
    # 1. This is an example of: VARIABLE
    # 5. This is an example of: STRING
    countdown_message = "Get ready for the next activity!"
    # 5. This is an example of: STRING
    print(f"\n{countdown_message}")
    
    # 3. This is an example of: LOOP
    for seconds in range(5, 0, -1):
        # 5. This is an example of: STRING
        print(f"Starting in {seconds}...")
        time.sleep(1)
    
    # 5. This is an example of: STRING
    print("Let's go! 🚀")

# 2. This is an example of: FUNCTION
def main():
    display_welcome()
    
    # 1. This is an example of: VARIABLE
    # 6. This is an example of: LIST
    # 5. This is an example of: STRING
    activities = ["Number Guessing Game", "Grade Analysis", "Countdown Timer"]
    
    # 5. This is an example of: STRING
    print("\nToday's activities:")
    # 3. This is an example of: LOOP
    for activity in activities:
        # 5. This is an example of: STRING
        print(f"- {activity}")
    
    countdown_timer()
    
    # 4. This is an example of: IF STATEMENT
    if guess_the_number():
        # 1. This is an example of: VARIABLE
        # 5. This is an example of: STRING
        success_message = "Great job on the guessing game!"
        print(success_message)
    
    analyze_scores()
    
    # 1. This is an example of: VARIABLE
    # 5. This is an example of: STRING
    completion_message = "Homework assignment completed!"
    # 5. This is an example of: STRING
    print(f"\n{completion_message}")
    # 5. This is an example of: STRING
    print("Don't forget to add your comments identifying the Python concepts!")

# 4. This is an example of: IF STATEMENT
if __name__ == "__main__":
    main()
