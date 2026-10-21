import datetime, random


def getBirthdays(NumberOfBirthdays):
    """Returns a list of number random date objects for birthdays."""
    birthdays = []

    for i in range(NumberOfBirthdays):
        # The year is unimportant for our simulation, as long as all
        # birthdays have the same year.
        startOfYear = datetime.date(2001, 1, 1)

        # get a random day into the year:
        randomNumberOfDays = datetime.timedelta(random.randint(0, 364))
        birthday = startOfYear + randomNumberOfDays
        birthdays.append(birthday)
    return birthdays


def getMatch(birthdays):
    """Returns the date object of a birthday that occurs more than once
    in the birthdays list."""

    if len(birthdays) == len(set(birthdays)):
        return None  # all birthdays are unique, so return None

    # compare each birthdays to every birthday:

    for a, birthdayA in enumerate(birthdays):
        for b, birthdayB in enumerate(birthdays[a + 1 :]):
            if birthdayA == birthdayB:
                return birthdayA


# Display the intro:
print(""" The Birthday Paradox shows us that in a group of N people, the odds
 that two of them have matching birthdays is surprisingly large.
 This program does a Monte Carlo simulation (that is, repeated random
 simulations) to explore this concept.
 (It's not actually a paradox, it's just a surprising result.)""")

# set up a tuple of month names in order:

MONTHS = (
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
)

while True:  # Keep asking until the user enter a valid amount.
    print("How many birthdays shall i generate? (Max 100)")
    response = input("> ")
    if response.isdecimal() and (0 < int(response) <= 100):
        numBDays = int(response)
        break  # user has entered a valid amount
print()

# generate and display the birthdays:
print(" Here are", numBDays, "birthdays")
birthdays = getBirthdays(numBDays)
for i, birthday in enumerate(birthdays):
    if i != 0:
        # display a comma for each birthday after ther first birthday
        print(",", end="")

    monthName = MONTHS[birthday.month - 1]
    dateText = "{} {}".format(monthName, birthday.day)
    print(dateText, end="")
print()
print()

# Determine if there are teo birthdays that match.
match = getMatch(birthdays)

# display results:
print("In this simulation,", end="")
if match != None:
    monthName = MONTHS[match.month - 1]
    dateText = "{} {}".format(monthName, match.day)
    print("multiple people have a birthday on", dateText)

else:
    print("there are no matching birthdays")
print()

# Run Throungh 100,000 simulations;
print("Generating", numBDays, "random birthdays 100,000 times...")
input("press Enter to begin...")

print("Let's run another 100,000 simulations")
simMatch = 0  # How many simulations had matching birthdays in them.
for i in range(100_000):
    # Report on the progress every 10,000 simulations:
    if i % 10_000 == 0:
        print(i, "simulation run...")
    birthdays = getBirthdays(numBDays)
    if getMatch(birthdays) != None:
        simMatch = simMatch + 1
print("100,000 simulations run.")

# display simulation results:
probability = round(simMatch / 100_000 * 100, 2)
print("Out of 100,000 simulations of", numBDays, "people, there was a")
print("matching birthday in that group", simMatch, "times. this means")
print("that", numBDays, "people have a", probability, " % chance of")
print("having a matching birthday in their group ")
print("thats's prbably more than you would think!")
