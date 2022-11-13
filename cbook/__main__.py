from options import OPTIONS
from startup import setup, show_help, greet_user
from input_handlers import ask_int


def main():
    # Setting up the configuration file
    setup()
    # Greeting the user
    greet_user()
    # Starting the main program
    keys = tuple(OPTIONS.keys())
    while True:
        print()
        show_help()
        i = ask_int("Choose an option: ", low=1, high=len(OPTIONS))
        selected_option = keys[i-1]
        func = OPTIONS[selected_option]
        try:
            func()
        except KeyboardInterrupt:
            pass
        print()
    

if __name__ == "__main__":
    main()