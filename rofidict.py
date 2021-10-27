#!/usr/bin/env python
from subprocess import Popen, PIPE
import json, os, requests, sys

def do_query(query):
	dictionary_url = f"https://od-api.oxforddictionaries.com/api/v2/entries/{lang}/{query}"
	response = requests.get(dictionary_url, headers={"app_id": creds["app_id"], "app_key": creds["app_key"]}).json()
	if "results" in response:
		return response["results"]
	else:
		exit(0)
    
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

	return list(set(definitions))

def display_definitions(menu, title):
	proc = Popen(f'rofi -dmenu -i -p "{title}"', stdout=PIPE, stdin=PIPE, shell=True, text=True)
	result = proc.communicate("\n".join(menu))[0].strip()

	if result == "":
		ask_query()
	else:
		proc = Popen('xclip -sel clip -f', stdout=PIPE, stdin=PIPE, shell=True, text=True)
		proc.communicate(result)

def ask_query():
	proc = Popen(f'rofi -dmenu -i -p "Define ({lang})"', stdout=PIPE, stdin=PIPE, shell=True, text=True)
	query = proc.communicate("")[0].strip().lower()
	
	if query == "":
		exit(0)

	results = do_query(query)
	definitions = get_all_definitions(results)
	display_definitions(definitions, f"{query} ({lang})")		

def get_creds():
	global creds
	filepath = os.path.dirname(os.path.realpath(__file__))
	with open(f"{filepath}/creds.json", "r") as f:
		creds = json.load(f)

def main():
	global lang

	if len(sys.argv) != 2:
		print("Provide a language code like en (english) or es (spanish)")
		exit(0)

	lang = sys.argv[1]

	get_creds()
	ask_query()

if __name__ == "__main__":
	main()