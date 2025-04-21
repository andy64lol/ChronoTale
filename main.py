# The game launcher

import os

def launch_legacies():
    print("\nLaunching Legacies...")
    os.system('python3 Legacies.py')

def launch_z_survival():
    print("\nLaunching Z_Survival...")
    os.system('python3 Z_survival.py')

def main():
    while True:
        print("\n=== Game Launcher ===")
        print("1. Launch Legacies")
        print("2. Launch Z_Survival")
        print("3. Exit")
        
        choice = input("Select a game to launch (1/2) or exit (3): ").strip()
        
        if choice == '1':
            launch_legacies()
        elif choice == '2':
            launch_z_survival()
        elif choice == '3':
            print("Exiting the launcher. Goodbye!")
            break
        else:
            print("Invalid selection. Please choose 1, 2, or 3.")

if __name__ == "__main__":
    main()
