Sublime Line Endings Unify
===============================

change files endings (`Mac`,`Unix`,`Windows`) to `Unix` (aka `\n`).  (windows with sublime3 will be `Windows` (aka `\r\n`))

## Installation:

 - you should use [sublime package manager][0]
 - use `cmd+shift+P` then `Package Control: Install Package`
 - look for `Line Endings Unify` and install it.
 - OR, Clone or unpack to "Line Endings Unify" folder inside "Packages" of your Sublime installation.

## How to use:

 - drag folder to sublime
 - use `cmd+shift+P` then `Line Endings Unify`
 - or bind some key in your user key binding:
  ```js
    {
	 "keys": ["ctrl+alt+shift+l"],
	 "command": "line_endings_unify"
	}
  ```
 - input file extentions to process
 - done

**always backup your data**

 [0]: http://wbond.net/sublime_packages/package_control
