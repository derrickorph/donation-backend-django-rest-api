import random

"""
def cycle_numbers(pop_up_bar):
    numbers = list(pop_up_bar)  # Step 1: Initialize an array with numbers

    # Prompt the user to input the maximum number
    while True:
        max_number = int(input("Enter the maximum number: "))
        if max_number > 0:  # Ensure max_number is positive
            break
        else:
            print("Invalid input. Please enter a positive number.")

    # Use the maximum number to generate a new list of numbers
    numbers = list(range(1, max_number + 1))

    # Check if the user input number is 60 or above
    if max_number >= 60:
        combination_size = 10
    else:
        combination_size = 3

    while len(numbers) > 0:
        # Step 3: Perform desired operation on each number
        print(f"These are the best {combination_size} digits: {', '.join(map(str, numbers[:combination_size]))}")

        # Step 4: Ask the user to input 'Y' to see the next combinations or 'N' to stop
        user_input = input("Do you want to see the next combinations? (Y/N): ").upper()

        if user_input == 'Y':
            # Display the next combinations
            numbers = numbers[combination_size:]
        elif user_input == 'N':
            # Stop the cycle if the user inputs 'N'
            break
        else:
            # Handle invalid input
            print("Invalid input. Please enter 'Y' or 'N'.")


cycle_numbers(range(1, 11))

"""


def cycle_numbers(users_list):
    # Check if the user input number is 60 or above
    if len(users_list) >= 60:
        combination_size = 10
    else:
        combination_size = 3

    while len(users_list) > 0:
        # Step 3: Perform desired operation on each user
        current_combination = users_list[:combination_size]
        print("Current combination:")
        for user in current_combination:
            print(user)

        # Step 4: Ask the user to input 'Y' to see the next combinations or 'N' to stop
        # user_input = input("Do you want to see the next combinations? (Y/N): ").upper()
        user_input = input("Do you want to see the next combinations? (Y/N): ").upper()

        if user_input == 'Y':
            # Display the next combinations
            users_list = users_list[combination_size:]
        elif user_input == 'N':
            # Stop the cycle if the user inputs 'N'
            break
        else:
            # Handle invalid input
            print("Invalid input. Please enter 'Y' or 'N'.")


# Exemple d'utilisation
users = [
    {
        "id": 1,
        "username": "super-admin",
        "surname": "",
        "is_superuser": True,
        "is_active": True,
        "id_number": "",
        "nationality": None,
        "email": "superadmin@gmail.com",
        "bank": "",
        "acc": "",
        "phoneNumber": None
    },
    {
        "id": 2,
        "username": "fexiw",
        "surname": "Russo",
        "is_superuser": False,
        "is_active": True,
        "id_number": "123456789",
        "nationality": None,
        "email": "rajev@mailinator.com",
        "bank": "Ferdinand Boyle",
        "acc": "753",
        "phoneNumber": "+1 (932) 838-3036"
    },
    {
        "id": 3,
        "username": "tacelilob",
        "surname": "Walter",
        "is_superuser": False,
        "is_active": True,
        "id_number": "89999",
        "nationality": None,
        "email": "soko@mailinator.com",
        "bank": "Cameron Owens",
        "acc": "511",
        "phoneNumber": "+1 (148) 864-1981"
    },
    {
        "id": 4,
        "username": "tedavihum",
        "surname": "Mooney",
        "is_superuser": False,
        "is_active": True,
        "id_number": "3718999",
        "nationality": None,
        "email": "qivutyb@mailinator.com",
        "bank": "Tatum Kinney",
        "acc": "989",
        "phoneNumber": "+1 (504) 309-3108"
    }
]

cycle_numbers(users)
