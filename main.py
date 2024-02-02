from datetime import datetime
import os

def check_file(file_path="notes.txt"):
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            file.write("NOTES:\n")
            file.write("TO DO:\n")
        print(f"File '{file_path}' created.")
    elif os.path.exists(file_path):
        # Check if the file is empty
        with open(file_path, "r") as file:
            content = file.read()
            if not content.strip():
                with open(file_path, "w") as file:
                    file.write("NOTES:\n")
                    file.write("TO DO:\n")
                print(f"File '{file_path}' found but empty. Resetting file.")
    
    else:
        print(f"File '{file_path}' found.")
def add_entry(entry_type, content, file_path="notes.txt"):
    prefix = "[Note]" if entry_type in ["note", "-n"] else "[ToDo]"
    timestamp = datetime.now().strftime("%Y-%m-%d")
    new_entry = f"{prefix} {timestamp}: {content}\n"
    
    # Initialize containers for existing entries
    notes, to_dos = [], []
    section = None

    # Load and categorize existing entries
    with open(file_path, "r+") as file:
        for line in file:
            if "NOTES:" in line:
                section = 'notes'
            elif "TO DO:" in line:
                section = 'to_dos'
            elif line.strip():  # Ignore empty lines
                if section == 'notes':
                    notes.append(line)
                elif section == 'to_dos':
                    to_dos.append(line)

    # Append the new entry to the appropriate list
    if prefix == "[Note]":
        notes.append(new_entry)
    else:
        to_dos.append(new_entry)

    # Rewrite the file with the updated lists
    with open(file_path, "w") as file:
        if notes:
            file.write("NOTES:\n")
            file.writelines(notes)
        if to_dos:
            file.write("\nTO DO:\n")
            file.writelines(to_dos)

    print(f"Entry added boss man: {new_entry.strip()}")



def display_entries(file_path="notes.txt", filter_type=None):
    if not os.path.exists(file_path):
        print("No entries found.")
        return

    with open(file_path, "r") as file:
        entries = file.readlines()

    display_formatted_entries(entries, filter_type)

def display_formatted_entries(entries, filter_type=None):
    is_printing = False  # Flag to control printing based on the filter_type

    for entry in entries:
        if 'TO DO:' in entry:
            is_printing = filter_type in [None, "todo"]  # Start printing if filtering for todos or not filtering
            if is_printing:
                print("TO DO:")
                print("-" * 10)
            continue

        elif 'NOTES:' in entry:
            is_printing = filter_type in [None, "note"]  # Start printing if filtering for notes or not filtering
            if is_printing:
                print("\nNOTES:")
                print("-" * 10)
            continue

        if is_printing and ':' in entry:  # Check if it's an entry line and the flag is set to print
            # Extract and print the date and content without the prefix
            date_content = entry.split(':', 1)[1].strip()
            print(f'• {date_content}')



def main():
    check_file()
    print("Note and To-Do List Manager")
    print("Type '-e' or '-exit' to quit. Type '-c' or '-clear' to clear the screen.")
    print("Use 'note'/'-n' or 'todo'/'-t' followed by your text. No need for quotes around your text.")
    print("Type '-s' to display all entries. Type '-st' to display only to-dos. Type '-sn' to display only notes.")
    
    while True:
        user_input = input(">> ").strip().split(' ', 1)
        command = user_input[0]

        if command in ['-e', '-exit']:
            print("Exiting...")
            break
        elif command in ['-c', '-clear']:
            os.system('cls' if os.name == 'nt' else 'clear')
        elif command == '-s':
            display_entries()
        elif command == '-st':
            display_entries(filter_type="todo")
        elif command == '-sn':
            display_entries(filter_type="note")
        elif command in ['note', 'todo', "-n", "-t"] and len(user_input) > 1:
            content = user_input[1]
            add_entry(command, content)
        else:
            print("Invalid input. Please use 'note'/'-n' or 'todo'/'-t' followed by your text, or '-e'/'-exit' to exit. Use '-cls' or '-clear' to clear the screen. Type '-s', '-st', or '-sn' to display entries.")

if __name__ == "__main__":
    main()
