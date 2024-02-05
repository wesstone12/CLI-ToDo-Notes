import os
api_key = os.environ.get('OPENAI_API_KEY')
from langchain_openai import OpenAI
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.prompts import PromptTemplate

def read_entries(file_path="notes.txt", filter_type=None):
    if not os.path.exists(file_path):
        print("No entries found.")
        return

    notes, to_dos, finished = [], [], []
    section = None
    with open(file_path, "r") as file:
        for line in file:
            if "NOTES:" in line:
                section = 'notes'
            elif "TO DO:" in line:
                section = 'to_dos'
            elif "FINISHED TO DOs:" in line:
                section = 'finished'
            else:
                # Append based on the current section
                if line.strip():  # Check if line is not just whitespace
                    if section == 'notes':
                        notes.append(line.strip())
                    elif section == 'to_dos':
                        to_dos.append(line.strip())
                    elif section == 'finished':
                        finished.append(line.strip())

    # Debug print to check lists' content after reading
    print(f"Notes: {notes}\nTo-Dos: {to_dos}\nFinished To-Dos: {finished}")
    return to_dos, notes, finished


def langchain(to_dos, notes, finished):
    chat = ChatOpenAI(temperature=.7, max_tokens=1000, model = 'gpt-4')
    messages = [
    SystemMessage(
        content=f'''
        ***TASK***: You are a helpful assistant for summarizing my work notes. 
        I want you to read my notes and to-dos and summarize them for me in a paragraph. Be concise and accurate.
        
        You need to have a section for my notes and a section for my to-dos and finished to-dos (the things i accomplished).
        
        **Example:**
        NOTES: Example paragraph of notes.

        TO-DOS: Example paragraph of to-dos.

        FINISHED TO-DOS: Example paragraph of finished to-dos.

        <End in smiley face or other emoji>
        '''
    ),
    HumanMessage(
        content=f'''Notes: {notes}
        To-Dos: {to_dos}
        Finished To-Dos: {finished}


     ''')
    
    ]
    

    return chat.invoke(messages).content

