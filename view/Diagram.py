import random
user_choice = int(input("Enter your choice: Type 0 for rock, 1 for paper, 2 for scissor: "))
if user_choice >= 3 or user_choice < 0:
    print("You typed an invalid number, you lose!")
else:
    computer_choice = random.randint(0, 2)
    print(f"Computer chose: {computer_choice}")
    if computer_choice == user_choice:
       print("It's a draw!")
    elif user_choice == 0 and computer_choice == 2:
       print("You win!")
    elif computer_choice == 0 and user_choice == 2:
       print("You lose!")
    elif computer_choice > user_choice:
       print("You lose!")
    elif user_choice > computer_choice:
       print("You win!")