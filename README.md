# Windows Context Switcher

Quickly open a Context (a group of apps) with just a single click.

---
## Usage

### Setting Up
1. Clone this repository into any directory (preferably one you can easily access)
2. Edit meta/config.txt, replacing the APPDATA_PATH and START_MENU_PATH placeholders with your specific version. If needed, you can also replace MS_APPS_PATH, and set the OBSIDIAN flag to True or False depending on your needs.
3. If any of your app's .lnk files aren't in START_MENU_PATH, and their .exe files aren't in APPDATA_PATH, then add their .exe path to meta/exceptions.txt. Take care to only capitalise the first letter of the filename, and make all others lowercase (this may be fixed in a later release). I've included Zotero as an example.
4. If you want to be able to open websites with this, you need to save a shortcut to them. Here are instructions on how to do so in [Chrome](https://support.google.com/chrome_webstore/answer/3060053?hl=en-GB) - a PR for support in other browsers is welcome. It doesn't matter whether you want the website to open in its own window (almost like an app) or just as part of the browser; whatever you choose when saving the shortcut is what happens.

### Creating Contexts
Run _generate_bat.bat (or generate_bat.py directly if you like) and follow the provided instructions.

---
## FAQ:

### Help! I can't find the name of my app!
If you can't automatically find the .exe file corresponding to the App Name, there may be a few issues.
Firstly, the 'name' you provide to the program may be wrong. Usually, it's just the regular name of the app, but not always - more specifically, it's the app's .exe file, but with the '.exe' removed.
An example of this is VSCode - it's launched with 'Code.exe', so the name you need to enter to the program is Code. If you don't want to remember this, just add it to meta/exceptions.txt, the same way Ms word,WINWORD.EXE is stored (i.e VSCode,Code.exe).

If this still doesn't work, then it's likely that your app isn't stored in the APPDATA_PATH folder. To find out where it _is_ stored, you can:
- Search for it in the Start Menu, right click and select 'Open File Location'. 
- Use a File Searching app (I recommend Everything) to locate the .exe file
Then, copy the path given into meta/exceptions.txt. Don't forget to add the actual .exe onto the end!

---

## Contributing

Feel free to make any issues or pull requests you like! I'm open to any help.
