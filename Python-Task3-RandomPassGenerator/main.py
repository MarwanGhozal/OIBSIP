import random
import string
# upper, lower, number, symbol = False
while True:
    try:
        length = int(input("Please enter the desired length of the password: "))
        if length < 8:
            print("Minimum password length is 8.")
            continue
        break

    except ValueError:
        print('Invalid input. Please enter numeric value for length.') 
while True:        
        use_upper = input("Do you want to use uppercase letters? (y/n)")
        use_upper = use_upper.lower() == "y"

        use_lower = input("Do you want to use lowercase letters? (y/n)")
        use_lower = use_lower.lower() == "y"

        use_number = input("Do you want to use digits? (y/n)")
        use_number = use_number.lower() == "y"

        use_symbols = input("Do you want to use symbols? (y/n)")
        use_symbols = use_symbols.lower() == "y"


        selected_types = sum([use_upper, use_lower, use_number, use_symbols])
        if selected_types < 2:
            print("A minimum of two selections are needed.")
            continue
        break



def generate_random_password(length, use_upper, use_lower, use_number, use_symbols):

    selected_pools = []
    if use_upper:
        selected_pools.append(string.ascii_uppercase)
    if use_lower:
        selected_pools.append(string.ascii_lowercase)
    if use_number: 
        selected_pools.append(string.digits)
    if use_symbols:
         selected_pools.append(string.punctuation)

    #We need to make the selected pool into a list to ensure we use every type picked, not just a random string where we pick random characters from, this might cause a password of 8 A even though the user selected to use symbols.

    password = [random.choice(pool) for pool in selected_pools]
    pool = ''.join(selected_pools)
    password += random.choices(pool, k=length - len(password))
    random.shuffle(password)
    return ''.join(password)

while True:
    print("Your generated password is " + generate_random_password(length, use_upper, use_lower, use_number, use_symbols))

    again = input("Do you want to generate another password? (y/n)")
    if again.lower() != 'y':
        break
