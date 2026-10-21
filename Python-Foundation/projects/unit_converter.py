print("1. km to miles")
print("2. miles to km")
print("3. kg to lbs")
print("4. lbs to kg")
print("5. meters to feet")

km_to_miles = 0.621371
miles_to_km = 1.60934
kg_to_lbs = 2.20462
lbs_to_kg = 0.453592
meters_to_feet = 3.28084

while True:
    try:
        choice = input("Enter your choice (1/2/3/4/5): ")
        user = float(input("Enter the value to convert: "))
    except:
        print("Invalid input. Please enter a valid number.")
        continue

    if choice == "1":
        print(f"{user} km is equal to {round(user * km_to_miles, 2)} miles")
    elif choice == "2":
        print(f"{user} miles is equal to {round(user * miles_to_km, 2)} km")
    elif choice == "3":
        print(f"{user} kg is equal to {round(user * kg_to_lbs, 2)} lbs")
    elif choice == "4":
        print(f"{user} lbs is equal to {round(user * lbs_to_kg, 2)} kg")
    elif choice == "5":
        print(f"{user} meters is equal to {round(user * meters_to_feet, 2)} feet")
    else:
        print("Invalid operation")

    player = input("convert again? (y/n)")
    if player == "n":
        break
