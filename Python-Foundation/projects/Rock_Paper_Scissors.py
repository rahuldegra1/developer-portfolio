import random

choices = ["rock", "paper", "scissors"]

wins = 0
losses = 0
ties = 0

while True:
    bot_choice = random.choice(choices)
    try:
        user_choice = str(input("Enter your choice (rock, paper, scissors): ")).lower()
    except:
        print("please enter a valid choice")
        continue

    if user_choice == bot_choice:
        print("It's a tie!")
        ties += 1
    elif user_choice == "rock":
        if bot_choice == "scissors":
            print("you won!")
            wins += 1
        elif bot_choice == "paper":
            print("you lost!")
            losses += 1
    elif user_choice == "paper":
        if bot_choice == "rock":
            print("you won!")
            wins += 1
        elif bot_choice == "scissors":
            print("you lost!")
            losses += 1
    elif user_choice == "scissors":
        if bot_choice == "paper":
            print("you won!")
            wins += 1
        elif bot_choice == "rock":
            print("you lost!")
            losses += 1
    else:
        print("invalid choice")
    print(f"Score - Wins : {wins}, Losses : {losses}, Ties : {ties}")
    player = input("play again? (y/n)")
    if player == "n":
        break
