from cs50 import get_float

while True:
    cents = get_float("Shange owed: ")
    if cents > 0:
        break

cents = round(cents * 100)

count = 0

# Number of quarters
while cents >= 25:
    cents = cents - 25
    count += 1

# Number of dimes
while cents >= 10:
    cents = cents - 10
    count += 1

# Number of nickles
while cents >= 5:
    cents = cents - 5
    count += 1

# Number of pennies
while cents >= 1:
    cents = cents - 1
    count += 1

print("Coins:", count)
