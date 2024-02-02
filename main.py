from datetime import datetime
import os

def add_entry(entry_type, content, file_path="notes.txt"):
    prefix = "[Note]" if entry_type in ["note", "-n"] else "[ToDo]"
    timestamp = datetime.now().strftime("%Y-%m-%d")
    entry = f"{prefix} {timestamp}: {content}\n"
    
    with open(file_path, "a") as file:
        file.write(entry)
    
    print(f"Entry added boss man: {entry.strip()}")

def display_entries(file_path="notes.txt", filter_type=None):
    # Check if the file exists to avoid FileNotFoundError
    if not os.path.exists(file_path):
        print("No entries found.")
        return

    to_dos, notes = [], []
    with open(file_path, "r") as file:
        for line in file:
            if "[ToDo]" in line:
                to_dos.append(line)
            elif "[Note]" in line:
                notes.append(line)

    if filter_type == "todo":
        print("TO DO:\n-----------------")
        print("".join(to_dos))
    else:
        print("TO DO:\n-----------------")
        print("".join(to_dos))
        print("NOTES:\n-----------------")
        print("".join(notes))

def main():
    print("Note and To-Do List Manager")
    print("Type '-e' or '-exit' to quit. Type '-cls' or '-clear' to clear the screen.")
    print("Use 'note'/'-n' or 'todo'/'-t' followed by your text. No need for quotes around your text.")
    print("Type '-s' to display all entries. Type '-st' to display only to-dos.")
    
    while True:
        user_input = input(">> ").strip().split(' ', 1)
        command = user_input[0]

        if command in ['-e', '-exit']:
            print("Exiting...")
            break
        elif command in ['-cls', '-clear']:
            os.system('cls' if os.name == 'nt' else 'clear')
        elif command in ['-s', '-st']:
            display_type = "todo" if command == "-st" else None
            display_entries(filter_type=display_type)
        elif command in ['note', 'todo', "-n", "-t"] and len(user_input) > 1:
            content = user_input[1]
            add_entry(command, content)
        else:
            print("Invalid input. Please use 'note'/'-n' or 'todo'/'-t' followed by your text, or '-e'/'-exit' to exit. Use '-cls' or '-clear' to clear the screen. Type '-s' or '-st' to display entries.")

if __name__ == "__main__":
    main()
