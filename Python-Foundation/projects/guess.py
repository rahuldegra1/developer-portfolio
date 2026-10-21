import random

while True:
    ranNum = random.randint(1, 100)
    attempts = 0
    while True:
        try:
            user = int(input("guess the number:"))
        except:
            print("please enter a valid number")
            continue
        attempts += 1
        if user == ranNum:
            print("You are absolutely Correct in", attempts, "tries")
            break

        if attempts == 7:
            print("You lost! The number was", ranNum)
            break

        elif user > ranNum:
            print("Number is too big")

        elif user < ranNum:
            print("number is too small")

    player = input("play again? (y/n)")
    if player == "n":
        break
