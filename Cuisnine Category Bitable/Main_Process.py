import subprocess

Uber_Eats = './Uber_Eats_Code/Ubereats_Process.py'
Door_Dash = './Door_Dash_Code/Doordash_Process.py'
while True:
    # Take input from the user
    choice = input("Which script do you want to execute? \nPress [ 1 ] for Ubereats_Process and [ 2 ] for Doordash_Process (press any other key to exit): ")

    if choice == '1':
        # Execute test1.py
        subprocess.run(['python', Uber_Eats], check=True)
    elif choice == '2':
        # Execute test2.py
        subprocess.run(['python', Door_Dash], check=True)
    else:
        invalid_choice = input("Invalid choice. Press 1 for Ubereats_Process and 2 Doordash_Process (press any key to exit): ")
        if invalid_choice == '1':
            # Execute test1.py
            subprocess.run(['python', Uber_Eats], check=True)
        elif invalid_choice == '2':
            # Execute test2.py
            subprocess.run(['python', Door_Dash], check=True)
        else:
            print("Exiting the program.")
            break

    # Ask the user if they want to execute another script
    another_choice = input("Do you want to run another script? Press y to continue (press any other key to exit): ")
    if another_choice.lower() != 'y':
        break  # Exit the loop if the user doesn't want to run another script

print("Program exited.")
