#!/usr/bin/env python
from subprocess import Popen, PIPE
from pathlib import Path
import json, requests, sys

# Query Oxford Dictionaries
def do_query(word):
	dictionary_url = f"https://od-api.oxforddictionaries.com/api/v2/entries/{lang}/{word}"
	headers = {"app_id": creds["app_id"], "app_key": creds["app_key"]}
	return requests.get(dictionary_url, headers=headers).json()

# Extract definitions from result
def get_all_definitions(results):
	definitions = []

	if "lexicalEntries" in results[0]:
		for lexical_entry in results[0]["lexicalEntries"]:
			if "entries" in lexical_entry:
				for entry in lexical_entry["entries"]:
					if "senses" in entry:
						for sense in entry["senses"]:
							if "definitions" in sense:
								for definition in sense["definitions"]:
									definitions.append(definition)
							elif "shortDefinitions" in sense:
								for definition in sense["shortDefinitions"]:
									definitions.append(definition)
							elif "crossReferenceMarkers" in sense:
								for definition in sense["crossReferenceMarkers"]:
									definitions.append(definition)

	return list(set(definitions))

# Display definitions in Rofi
def display_definitions(menu, title):
	proc = Popen(f'rofi -dmenu -i -p "{title}"', stdout=PIPE, stdin=PIPE, shell=True, text=True)
	ans = proc.communicate("\n".join(menu))[0].strip()

	if ans == "":
		ask_word()
	else:
		clipboard_copy(ans)

# Send a string to the clipboard
def clipboard_copy(text):
	proc = Popen('xclip -sel clip -f', stdout=PIPE, stdin=PIPE, shell=True, text=True)
	proc.communicate(text)
	
# Ask for the word to query
def ask_word():
	proc = Popen(f'rofi -dmenu -i -p "Define ({lang})"', stdout=PIPE, stdin=PIPE, shell=True, text=True)
	ans = proc.communicate("")[0].strip().lower()
	
	if ans == "":
		exit(0)
	
	if len(ans.split(" ")) > 1:
		ask_word()
		return

	response = do_query(ans)

	if "results" not in response:
		ask_word()
		return

	definitions = get_all_definitions(response["results"])
	display_definitions(definitions, f"{ans} ({lang})")		

# Read the api credentials file
def get_creds():
	global creds
	thispath = Path(__file__).parent.resolve()
	filepath = Path(thispath) / Path("creds.json")
	with open(filepath, "r") as f:
		creds = json.load(f)

# Main function
def main():
	global lang

	if len(sys.argv) != 2:
		print("Provide a language code like en (english) or es (spanish)")
		exit(0)

	lang = sys.argv[1]

	get_creds()
	ask_word()

if __name__ == "__main__":
	main()