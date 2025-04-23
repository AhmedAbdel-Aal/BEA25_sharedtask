import json
import re

def load_json(file_path: str):
    """Load and return data from a JSON file."""
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


def save_json(file_path: str, data: any):
    """Save data to a JSON file."""
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def load_txt(file_path: str):
    """Load and return contents of a text file."""
    with open(file_path, "r", encoding="utf-8") as f:
        data = f.read()
    return data


def save_txt(file_path: str, data: str):
    """Save data to a text file."""
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(data)

def split_conversation(text):
    """
    Splits the conversation text into parts based on the speaker tags (Tutor: and Student:).
    Returns a list of tuples containing the speaker tag and the corresponding text.
    """
    # Use regex to split while keeping the speaker tag
    parts = re.findall(r'(Tutor:|Student:)(.*?)(?=Tutor:|Student:|$)', text, re.DOTALL)
    return parts

def extract_dialogue(conversation_history):
    """
    Extracts the dialogue from the conversation history string.
    Returns a list of dictionaries with 'speaker' and 'text' keys.
    """
    # Split the conversation history into parts
    parts = split_conversation(conversation_history)
    
    # Create a list of dictionaries for each part
    dialogue = [{'speaker': speaker.strip(':'), 'text': content.strip()} for speaker, content in parts]
    
    return dialogue

def dialogue_to_string(dialogue):
    """
    Converts the dialogue list into a formatted string.
    Each entry is formatted as "Speaker: Text".
    """
    return "\n".join([f"{entry['speaker']}: {entry['text']}" for entry in dialogue])


def format_prompt(template: str, **kwargs) -> str:
    """Format a prompt template with variables."""
    try:
        return template.format(**kwargs)
    except KeyError as e:
        raise ValueError(f"Missing required prompt variable: {e}")

def extract_xml(text: str, tag: str) -> str:
    """
    Extracts the content of the specified XML tag from the given text. Used for parsing structured responses

    Args:
        text (str): The text containing the XML.
        tag (str): The XML tag to extract content from.

    Returns:
        str: The content of the specified XML tag, or an empty string if the tag is not found.
    """
    match = re.search(f"<{tag}>(.*?)</{tag}>", text, re.DOTALL)
    return match.group(1).strip() if match else ""

