This is a fork of https://github.com/defCoding/rofi-dictionary with some of my own modifications.

You will need to create a JSON file named `creds.json` in the cloned repo. This will contain the `app_key` and `app_id` needed for the Oxford Dictionary API. To retrieve your values, create an account and application at the [OxfordDictionary website](https://developer.oxforddictionaries.com/). Once you've created your application, get your `app_key` and `app_id` from the API Credentials page.

```json
{
  "app_key": "APP KEY GOES HERE",
  "app_id": "APP ID GOES HERE"
}
```

It's necessary to provide the language code as an argument:

`/path/to/rofidict.py en` 

(For english definitions)

`/path/to/rofidict.py es` 

(For spanish definitions)

[Check available languages here](https://developer.oxforddictionaries.com/documentation/languages)

Selecting a definition copies it to the clipboard if `xclip` is installed.