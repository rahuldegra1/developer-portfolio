while True:
    try:
        user1 = float(input("Enter your First Number: "))
        user2 = float(input("Enter your second Number: "))
    except:
        print("type a valid number")
        continue
    operation = input()
    if operation == "+":
        print(user1 + user2)
    elif operation == "-":
        print(user1 - user2)
    elif operation == "*":
        print(user1 * user2)
    elif operation == "/":
        if user2 == 0:
            print("not defined")
        else:
            print(user1 / user2)
    else:
        print("invalid operation")
    player = input("calculate again? (y/n)")
    if player == "n":
        break
