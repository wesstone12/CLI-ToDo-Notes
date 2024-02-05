from datetime import datetime
import os
import summarizer

def check_file(file_path="notes.txt"):
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            file.write("NOTES:\n")
            file.write("TO DO:\n")
            file.write("FINISHED TO DOs:\n")
        print(f"File '{file_path}' created.")
    elif os.path.exists(file_path):
        # Check if the file is empty
        with open(file_path, "r") as file:
            content = file.read()
            if not content.strip():
                with open(file_path, "w") as file:
                    file.write("NOTES:\n")
                    file.write("TO DO:\n")
                    file.write("FINISHED TO DOs:\n")
                    
                print(f"File '{file_path}' found but empty. Resetting file.")
    
    else:
        print(f"File '{file_path}' found.")
def add_entry(entry_type, content, file_path="notes.txt"):
    prefix = "[Note]" if entry_type in ["note", "-n"] else "[ToDo]"
    timestamp = datetime.now().strftime("%Y-%m-%d")
    new_entry = f"{prefix} {timestamp}: {content}\n"
    
    # Read the current file content and append the new entry in the correct section
    notes, to_dos, finished_todos = [], [], []
    current_section = None

    with open(file_path, "r") as file:
        for line in file:
            if "NOTES:" in line:
                current_section = notes
            elif "TO DO:" in line:
                current_section = to_dos
            elif "FINISHED TO DOs:" in line:
                current_section = finished_todos
            else:
                current_section.append(line)

    # Append the new entry to the appropriate list
    if prefix == "[Note]":
        notes.append(new_entry)
    elif prefix == "[ToDo]":
        to_dos.append(new_entry)  # Ensure this is appending to to_dos, not finished_todos

    # Rewrite the file with the updated content
    with open(file_path, "w") as file:
        file.write("NOTES:\n")
        file.writelines(notes)
        file.write("TO DO:\n")
        file.writelines(to_dos)
        file.write("FINISHED TO DOs:\n")
        file.writelines(finished_todos)

    print(f"Entry added boss man: {new_entry.strip()}")



def display_entries(file_path="notes.txt", filter_type=None):
    if not os.path.exists(file_path):
        print("No entries found.")
        return

    with open(file_path, "r") as file:
        entries = file.readlines()

    display_formatted_entries(entries, filter_type)
def check_off_todo(file_path="notes.txt"):
    # Load existing entries
    entries = {"notes": [], "to_dos": [], "finished_todos": []}
    section = None
    with open(file_path, "r") as file:
        for line in file:
            if "NOTES:" in line:
                section = "notes"
            elif "TO DO:" in line:
                section = "to_dos"
            elif "FINISHED TO DOs:" in line:
                section = "finished_todos"
            elif line.strip():
                entries[section].append(line)
    
    # Display current to-dos with indexes
    if entries["to_dos"]:
        print("TO DOs:")
        for index, todo in enumerate(entries["to_dos"], start=1):
            print(f"{index}. {todo.strip()}")
    else:
        print("No TO DOs to display.")
        return

    try:
        choice = int(input("Enter the number of the to-do to check off: ")) - 1
        if 0 <= choice < len(entries["to_dos"]):
            finished_todo = entries["to_dos"].pop(choice)
            entries["finished_todos"].append(finished_todo)
            # Ensure this part correctly rewrites the sections without mixing them.
            with open(file_path, "w") as file:
                if entries["notes"]:
                    file.write("NOTES:\n" + "".join(entries["notes"]))
                file.write("\nTO DO:\n" + "".join(entries["to_dos"]))
                file.write("\nFINISHED TO DOs:\n" + "".join(entries["finished_todos"]))
    except ValueError:
        print("Please enter a number.")

def update_todo_file(file_path, to_dos=None, finished_todo=None):
    notes, current_todos, finished_todos = [], [], []
    section = None

    # Read the file and categorize entries
    with open(file_path, "r") as file:
        for line in file:
            if "NOTES:" in line:
                section = 'notes'
            elif "TO DO:" in line:
                section = 'to_dos'
            elif "FINISHED TO DOs:" in line:
                section = 'finished_todos'
            elif line.strip():  # Check if line is not just whitespace
                if section == 'notes':
                    notes.append(line)
                elif section == 'to_dos' and to_dos is not None:
                    current_todos.append(line)
                elif section == 'finished_todos':
                    finished_todos.append(line)

    # Update the lists based on operations
    if finished_todo:
        # Add the finished to-do item to the finished_todos list
        finished_todos.append(finished_todo)

    # Rewrite the file with updated sections, ensuring there are newlines between sections
    with open(file_path, "w") as file:
        if notes:
            file.write("NOTES:\n" + "".join(notes) + "\n")
        if to_dos is not None:
            file.write("TO DO:\n" + "".join(to_dos) + "\n")
        file.write("FINISHED TO DOs:\n" + "".join(finished_todos))

    print("File updated successfully.")


def display_formatted_entries(entries, filter_type=None):
    sections = {'notes': [], 'to_dos': [], 'finished_todos': []}
    current_section = None

    for entry in entries:
        if 'NOTES:' in entry:
            current_section = 'notes'
        elif 'TO DO:' in entry:
            current_section = 'to_dos'
        elif 'FINISHED TO DOs:' in entry:
            current_section = 'finished_todos'
        elif entry.strip():  # Add non-empty lines to the current section
            sections[current_section].append(entry.strip())

    # Display sections based on filter_type or if they have content
    if not filter_type or filter_type == "note":
        if sections['notes']:
            print("NOTES:\n----------")
            for note in sections['notes']:
                print(f"• {note}")
            print()  # Add a newline for spacing if the section was displayed

    if not filter_type or filter_type == "todo":
        if sections['to_dos']:
            print("TO DO:\n----------")
            for todo in sections['to_dos']:
                print(f"• {todo}")
            print()  # Add a newline for spacing if the section was displayed

    if not filter_type:  # Finished to-dos are always shown without a specific filter
        if sections['finished_todos']:
            print("FINISHED TO DOs:\n----------")
            for finished_todo in sections['finished_todos']:
                print(f"• {finished_todo}")




def main():
    check_file()
    print("Note and To-Do List Manager")
    print("Type '-e' or '-exit' to quit. Type '-c' or '-clear' to clear the screen.")
    print("Use 'note'/'-n' or 'todo'/'-t' followed by your text. No need for quotes around your text.")
    print("Type '-s' to display all entries. Type '-st' to display only to-dos. Type '-sn' to display only notes.")
    print("To remove an entry, type '-x'. ")
    
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
        elif command == '-x':
            check_off_todo(file_path="notes.txt")
        else:
            print("Type '-e' or '-exit' to quit. Type '-c' or '-clear' to clear the screen.")
            print("Use 'note'/'-n' or 'todo'/'-t' followed by your text. No need for quotes around your text.")
            print("Type '-s' to display all entries. Type '-st' to display only to-dos. Type '-sn' to display only notes.")
            print("To remove an entry, type '-x'. ")
if __name__ == "__main__":
    main()

    to_dos, notes, finished = summarizer.read_entries()
    print(summarizer.langchain(to_dos, notes, finished))
