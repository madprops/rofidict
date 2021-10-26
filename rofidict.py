#!/usr/bin/env python

from subprocess import run, Popen, PIPE
import json, os, requests

LANG = "en-gb"

def do_query(query):
	dictionary_url = f"https://od-api.oxforddictionaries.com/api/v2/entries/{LANG}/{query}"
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

	return definitions

def display_definitions(menu, title):
	echo = Popen(["echo", "\n".join(menu)], stdout=PIPE)
	result = run(rofi_command + ["-no-custom", "-p", title], stdin=echo.stdout, capture_output=True, text=True).stdout.strip()
	echo.stdout.close()

	if result == "":
		exit(0)

	proc = Popen("xclip -sel clip -f", stdout=PIPE, stdin=PIPE, shell=True, text=True)
	proc.communicate(result)

def choose_word():
	result = run(rofi_command + ["-p", "define:"], capture_output=True, text=True)
	query = result.stdout.strip().lower()
	
	if query == "":
		exit(0)

	results = do_query(query)
	definitions = get_all_definitions(results)
	display_definitions(definitions, query)		

def get_creds():
	global creds
	filepath = os.path.dirname(os.path.realpath(__file__))
	with open(f"{filepath}/creds.json", "r") as f:
		creds = json.load(f)

def main():
	global rofi_command
	rofi_command = ["rofi", "-dmenu", "-lines", "10", "-no-fixed-num-lines", "-i"]
	get_creds()
	choose_word()

if __name__ == "__main__":
	main()