import random, sys

ALL_CLOSED = """
+------+ +------+ +------+
|      | |      | |      |
|   1  | |   2  | |  3   |
|      | |      | |      |
|      | |      | |      |
|      | |      | |      |
+------+ +------+ +------+"""

FIRST_GOAT = """
+------+ +------+ +------+
|  ((  | |      | |      |
|  oo  | |   2  | |  3   |
| /_/|_| |      | |      |
|    | | |      | |      |
|GOAT||| |      | |      |
+------+ +------+ +------+"""

SECOND_GOAT = """
+------+ +------+ +------+
|      | |  ((  | |      |
|   1  | |  OO  | |  3   |
|      | | /_/|_| |      |
|      | |    | | |      |
|      | |GOAT||| |      |
+------+ +------+ +------+"""

THIRD_GOAT = """
+------+ +------+ +------+
|      | |      | |  ((  |
|   1  | |   2  | |  OO  |
|      | |      | | /_/|_|
|      | |      | |    | |
|      | |      | |GOAT|||
+------+ +------+ +------+"""

FIRST_CAR_OTHERS_GOAT = """
+------+ +------+ +------+
| CAR! | |  ((  | |  ((  |
|   __ | |  oo  | |  oo  |
|  /_  | | /_/| | | /_/| |
| /    | | /  | | | /  | |
|   0  | |GOAT| | |GOAT| |
+------+ +------+ +------+"""

SECOND_CAR_OTHERS_GOAT = """
+------+ +------+ +------+
|  ((  | | CAR! | |  ((  |
|  oo  | |   __ | |  oo  |
| /_/| | |  /_  | | /_/| |
| /  | | | /    | | /  | |
|GOAT| | |   0  | |GOAT| |
+------+ +------+ +------+"""

THIRD_CAR_OTHERS_GOAT = """
+------+ +------+ +------+
|  ((  | |  ((  | | CAR! |
|  oo  | |  oo  | |    __|
| /_/| | | /_/| | |  _/  |
| /  | | | /  | | | /_ __|
|GOAT| | |GOAT| | |   0  |
+------+ +------+ +------+"""

print(
    """ In the Monty Hall game show, you can pick one of three doors. One door
has a new car for a prize. The other two doors have worthless goats:
{}
Say you pick Door #1.
Before the door you choose is opened, another door with a goat is opened:
{}
You can choose to either open the door you originally picked or swap
to the other unopened door.

It may seem like it doesn't matter if you swap or not, but your odds
do improve if you swap doors! This program demonstrates the Monty Hall
problem by letting you do repeated experiments.""".format(ALL_CLOSED, THIRD_GOAT)
)

input("Press Enter to start...")

swapWins = 0
swapLosses = 0
stayWins = 0
stayLosses = 0

while True:  # main program loop.
    # the computer picks which door has the car:
    doorthatHasCar = random.randint(1, 3)
    # Ask the player to pick a door
    print(ALL_CLOSED)

    while True:  # Keep asking the player until they enter a valid door.
        print('pick a door 1,2, or 3 (or "quit" to stop):')
        response = input("> ").upper()
        if response == "QUIT":
            # End the game
            print("Thanks for Playing!")
            sys.exit()

        if response == "1" or response == "2" or response == "3":
            break
    doorPick = int(response)

    # Figure out which goat door to show the player
    while True:
        # Select a door that is a goat and not picked by the player:
        showGoatDoor = random.randint(1, 3)
        if showGoatDoor != doorPick and showGoatDoor != doorthatHasCar:
            break

        # show this goat door to the player
        if showGoatDoor == 1:
            print(FIRST_GOAT)
        elif showGoatDoor == 2:
            print(SECOND_GOAT)
        elif showGoatDoor == 3:
            print(THIRD_GOAT)

        print("Door {} contains a goat!".format(showGoatDoor))

        # ask the player if they want to swap:

        while True:  # keep asking until the player enter Y or N.
            print("Do you want to swap doors? Y/N")
            swap = input("> ").upper()
            if swap == "Y" or swap == "N":
                break

        # Swap the player"s door if they wanted to swap

        if swap == "Y":
            if doorPick == "1" and showGoatDoor == "2":
                doorPick = 3
            elif doorPick == "1" and showGoatDoor == "3":
                doorPick = 2
            elif doorPick == 2 and showGoatDoor == 1:
                doorPick = 3
            elif doorPick == 2 and showGoatDoor == 3:
                doorPick = 1
            elif doorPick == 3 and showGoatDoor == 1:
                doorPick = 2
            elif doorPick == 3 and showGoatDoor == 2:
                doorPick = 1

        # open all the doors:

        if doorthatHasCar == 1:
            print(FIRST_CAR_OTHERS_GOAT)
        elif doorthatHasCar == 2:
            print(SECOND_CAR_OTHERS_GOAT)
        elif doorthatHasCar == 3:
            print(THIRD_CAR_OTHERS_GOAT)

        print("Door {} has the car!".format(doorthatHasCar))

        # Record wins and losses for swapping and not swapping

        if doorPick == doorthatHasCar:
            print("You won!")
            if swap == "Y":
                swapWins += 1
            elif swap == "N":
                stayWins += 1
        else:
            print("Sorry, you lost.")
            if swap == "Y":
                swapLosses += 1
            elif swap == "N":
                stayLosses += 1

        # calculate success rate of swapping and not swapping:
        totalSwaps = swapWins + swapLosses
        if totalSwaps != 0:  # Prevent zero divide error.
            swapSuccess = round(stayWins / totalSwaps * 100, 1)
        else:
            swapSuccess = 0.0

        totalStays = stayWins + stayLosses
        if totalStays != 0:  # prevent zer divide.
            staysuccess = round(swapWins / totalStays * 100, 1)
        else:
            staysuccess = 0.0

        print()
        print("Swapping:    ", end="")
        print("{} wins, {} losses, ".format(swapWins, swapLosses), end="")
        print("success rate {}%".format(staysuccess))
        print()
        input("Press Enter to repeat the experiment...")
