from datetime import datetime
import os

def add_entry(entry_type, content, file_path="notes.txt"):
    prefix = "[Note]" if entry_type in ["note", "-n"] else "[ToDo]"
    timestamp = datetime.now().strftime("%Y-%m-%d")
    entry = f"{prefix} {timestamp}: {content}\n"
    
    # Write the entry to the file
    with open(file_path, "a") as file:
        file.write(entry)
    
    print(f"Entry added boss man: {entry.strip()}")
    
    # Organize entries in the file after adding a new one
    write_entries(file_path)

def write_entries(file_path="notes.txt"):
    if not os.path.exists(file_path):
        print("No entries to organize.")
        return
    
    to_dos, notes = [], []
    with open(file_path, "r") as file:
        for line in file:
            if "[ToDo]" in line:
                to_dos.append(line)
            elif "[Note]" in line:
                notes.append(line)
    
    # Rewrite the file with organized entries
    with open(file_path, "w") as file:
        if to_dos:
            file.write("TO DO:\n-----------------\n")
            file.writelines(to_dos)
        if notes:
            file.write("\nNOTES:\n-----------------\n")
            file.writelines(notes)

def display_entries(file_path="notes.txt", filter_type=None):
    if not os.path.exists(file_path):
        print("No entries found.")
        return
    
    # Simply print the file contents since they're already organized
    with open(file_path, "r") as file:
        if filter_type == "todo":
            print("TO DO:\n-----------------")
            print(file.read())
        else:
            print(file.read())

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
