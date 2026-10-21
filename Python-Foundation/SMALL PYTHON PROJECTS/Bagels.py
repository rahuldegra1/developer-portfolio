import random

NUM_DIGITS = 3  # (!) try setting this to 1 to 10
MAX_GUESSES = 10  # (!) try setting this to 1 to 100


def main():
    print("""Bagels, a deductive logic game.

    I am thinking of a 3 Digit Number with NO repeated digits.
    Try to guess what it is. Here are some clues:
    
    When i say:         That means:
    PICO                -One digit is correct but in the wrong position.
    FERMI               -One digit is correct and in the right position.
    BAGELS              -No digit is correct.""")

    while True:  # main game loop
        # this stores the secret number the player needs to guess
        secretNum = getSecretNum()
        print("I have thougt up a number")
        print("you have {} guesses to get it.".format(MAX_GUESSES))

        numGuesses = 1
        while numGuesses <= MAX_GUESSES:
            guess = ""
            # Keep logging untill they enter a valid guess:
            while len(guess) != NUM_DIGITS or not guess.isdecimal():
                print("Guess #{}:".format(numGuesses))
                guess = input("> ")

            clues = getClues(guess, secretNum)
            print(clues)
            numGuesses += 1

            if guess == secretNum:
                break  # they're correct, so break out of this loop.
            if numGuesses > MAX_GUESSES:
                print("You ran out of guesses.")
                print("The answer was {}.".format(secretNum))

                # ask player if they want to play again.
                print("Do you want to play again? (yes/no)")
                if not input("> ").lower().startswith("y"):
                    break
        print("Thanks for playing")


def getSecretNum():
    """Returns a string made up of NUM_DIGITS unique random digits."""
    numbers = list("0123456789")  # Create a list of digits 0 to 9.
    random.shuffle(numbers)  # suffle them into random order

    # get the first NUM_DIGITS in the list for the secreat number:

    secretNUM = ""
    for i in range(NUM_DIGITS):
        secretNUM += str(numbers[i])
    return secretNUM


def getClues(guess, secretNum):
    """Returns a string with the pico, fermi, bagels clues for a guess
    and secret number pair."""

    if guess == secretNum:
        return "You got it"

    clues = []

    for i in range(len(guess)):
        if guess[i] == secretNum[i]:
            # A correct digit is in the correct place.
            clues.append("Fermi")
        elif guess[i] in secretNum:
            # a correct digit is in the incorrect place.
            clues.append("Pico")
    if len(clues) == 0:
        return "bagels"  # there are no correct digits at all
    else:
        # Sort the clues into alphabetical order so their original order
        # doesn't give information away.
        clues.sort()
        # Make a single string from the list of string clues.
        return " ".join(clues)

    # if the program is run (instead of imported), run the game:


if __name__ == "__main__":
    main()
