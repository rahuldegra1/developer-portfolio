list = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
user = int(input("Enter a number from list: "))
low = 0
high = len(list) - 1
while low <= high:
    mid = (low + high) // 2
    if list[mid] == user:
        print(f"Found {user} at position {mid}")
        break
    elif list[mid] < user:
        low = mid + 1
    else:
        high = mid - 1
else:
    print(f"{user} not found in the list.")
