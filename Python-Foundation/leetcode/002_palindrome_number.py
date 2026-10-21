def isPalindrome(x):
    if x < 0:
        return False
    if x > 0 and x % 10 == 0:
        return False
    temp = x
    reversed_num = 0

    while temp > 0:
        digit = temp % 10
        reversed_num = (reversed_num * 10) + digit
        temp = temp // 10
    return reversed_num == x


print(isPalindrome(121))
print(isPalindrome(-121))
print(isPalindrome(10))
