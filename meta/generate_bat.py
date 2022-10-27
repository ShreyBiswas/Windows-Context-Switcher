import os

### FILE HANDLING
def read_exceptions():
    # read meta/exceptions.txt as dictionary
    # in format app_name,path
    # outputs dictionary in format {app_name: path}
    exceptions = open("exceptions.txt", "r").read().strip().split("\n")
    return dict(path.split(",") for path in exceptions)


def read_config():
    # read meta/config.txt as dictionary
    # in format key=value
    # outputs dictionary in format {key: value}
    config = open("config.txt", "r").read().strip().split("\n")
    return dict(line.split("=") for line in config)


# load exceptions.txt and config.txt for use
exceptions = read_exceptions()
config = read_config()


def write_to_file(context, bat_contents):
    # creates a batch file with the given context name
    with open(f"..\\{context}.bat", "w") as file:
        file.write(bat_contents)


### FILE LOCATION


def find_ms_file(file_name):
    # searches for a file in Microsoft's specific folder, usually C:\\Program Files\\Microsoft Office\\root\\Office16\\
    # for some reason, MS apps are differently named, so file_name is taken from exceptions.txt
    # e.g MS Word -> WINWORD.EXE

    for root, dirs, files in os.walk(
        config["MS_APPS_PATH"]
    ):  # searches all subfolders of the paths
        for file in files:
            if file == file_name.upper():  # MS apps are all uppercase
                return os.path.join(root, file)
    return False


def find_app_shortcut(file_name):
    # searches for a file in the user's Start Menu folder, usually C:\\Users\\user\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs

    for root, dirs, files in os.walk(config["START_MENU_PATH"]):
        for file in files:
            if file == f"{file_name}.lnk":
                return os.path.join(root, file)
    return False


def find_files(file_names):
    # finds the paths for a series of files in the AppData folder, usually C:\\Users\\user\\AppData\\Local\\
    # returns a list of paths

    paths = []
    print(f'Finding {", ".join(file_names)}')

    for root, dirs, files in os.walk(config["APPDATA_PATH"]):
        # TODO: Replace below lines with set intersection?
        for file_name in file_names:  # checks all files at once
            if f"{file_name}.exe" in files:
                paths.append(os.path.join(root, file_name))
                print(f"Found {file_name}.")
                if len(paths) == len(
                    file_names
                ):  #! Warning - if there are two .exe files with the same name,
                    return (
                        paths,
                        True,
                    )  #! this finds both and ignores the final element in the list
                    # * Workaround is to add the .exe you want to exceptions.txt
    return paths, False


### UTILS


def get_obsidian_uri(
    vault_name,
):  # Obsidian lets you use URIs to open specific vaults much more easily
    vault_name = vault_name.replace(
        " ", "%20"
    )  # TODO: Replace with actual URI translation
    return f"obsidian://open?vault={vault_name}"


def check_exception(app_name):  # quickly confirms whether an app is in exceptions.txt
    try:
        return exceptions[app_name]
    except KeyError:
        return False


##### MAIN #####


def interface():  # just for convenience when generating .bat files
    print("\n\n\n-------------------------------------------------------------------")
    print("Welcome to the batch file generator for creating Windows Contexts!\n\n")
    print("Please enter the name of the context you want to create.")

    CONTEXT_NAME = input("Context name: ").strip()

    if config["OBSIDIAN"] == "True":
        # Get the name of the Obsidian vault
        print(
            "\nEnter the name of the Obsidian vault you want to open in this context."
        )
        print("Hit Enter without any text if you do not want to open a vault.")
        OBSIDIAN_VAULT = input().strip()
    else:
        OBSIDIAN_VAULT = False

    # Loop until the user enters an empty string (hits enter twice)
    print(
        "\nEnter the apps you want to open in this context. Press enter after each one."
    )
    print("Hit Enter twice when you are done.")
    APP_NAMES = []
    while True:
        app = input()
        if not app:
            break
        # capitalise only first letter of app, lowercase the rest
        # most app .exe files are capitalised like this
        app = app[0].upper() + app[1:].lower()
        APP_NAMES.append(app)

    print(
        "\n Enter the websites (PWAs) you want to open in this context. Press enter after each one."
    )
    print("Hit Enter twice when you are done.")
    PWA_NAMES = []
    while True:
        PWA = input()
        if not PWA:
            break
        PWA = PWA[0].upper() + PWA[1:].lower()
        PWA_NAMES.append(PWA)

    print("\nThank you! Generating batch file now...\n")

    return CONTEXT_NAME, APP_NAMES, PWA_NAMES, OBSIDIAN_VAULT


if __name__ == "__main__":
    CONTEXT_NAME, APP_NAMES, PWA_NAMES, OBSIDIAN_VAULT = interface()

    bat_contents = "@echo off"  # stops the batch file from printing each command

    unique = [
        app for app in APP_NAMES if app.startswith("Ms ") or check_exception(app)
    ]  # will be handled separately rather than in find_files
    paths = []

    FAILED = []  # tracks failed searches

    for app_name in unique:
        print(f"Finding {app_name}...")

        if app_name.startswith("Ms "):
            path = find_ms_file(exceptions[app_name])
        else:
            path = check_exception(app_name)

        paths.append(path)
        print(f"Found {app_name}.")

    for app in set(APP_NAMES) - set(unique):
        print(f"\nFinding {app}...")
        if path := find_app_shortcut(f"{app}.exe"):
            print(f"Found {app}.")
            paths.append(path)
        else:
            print("Couldn't locate {app} shortcut. Adding to failed list.")
            FAILED.append(app)

    for PWA in PWA_NAMES:
        print(f"\nFinding {PWA}...")
        if path := find_app_shortcut(f"{PWA}lnk"):
            print(f"Found {PWA}.")
            paths.append(path)
        else:
            print("Couldn't locate {PWA} shortcut. Adding to failed list.")
            FAILED

    print(f"\nCouldn't locate {', '.join(FAILED)}.")
    print("Searching for .exe files...")

    others = find_files(FAILED)
    if others[1]:  # if all apps were found
        print(f"\nSuccessfully found all apps. Add these to meta/exceptions.txt for faster lookup in the future.\n{'\n '.join(others[0])}.")
        paths.extend(others[0])
    else:
        print("\nFAILED TO FIND ALL ADDITIONAL APPS")
        print(f"Apps found: {others[0]}")
        print(f"Apps not found: {set(FAILED) - set(others[0])}")
        print("Please locate .exe files for the above apps, and add to meta/exceptions.txt")
        # end program or continue based on y/n input
        continue_ = input("Add just the successful apps or exit? (y|yes|continue/n|no|exit): ").lower()
        if continue_ in ["y", "yes", "continue"]:
            print(f"Continuing with {others[0]}")
            paths.extend(others[0])
        else:
            print(f"Exiting. Please add the following to meta/exceptions.txt:\n{', '.join(set(FAILED) - set(others[0]))}")
            exit()

    for path in paths:  # add command to start each app
        bat_contents += f'\nstart "" "{path}"'

    if OBSIDIAN_VAULT:  # add command to open Obsidian at specific vault
        # * NOTE: Vaults must have been previously registered in Obsidian
        # * In other words, when you open the Obsidian app, the Vault should be accessible from the sidebar

        bat_contents += f"\nstart {get_obsidian_uri(OBSIDIAN_VAULT)}"

    bat_contents += "\nexit"  # close cmd window after opening all apps

    print("\nWriting to batch file...")
    write_to_file(CONTEXT_NAME, bat_contents)
    print("Done!")
