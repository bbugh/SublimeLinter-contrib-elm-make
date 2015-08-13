SublimeLinter-contrib-elm-make
================================

[![Build Status](https://travis-ci.org/bbugh/SublimeLinter-contrib-elm-make.svg?branch=master)](https://travis-ci.org/bbugh/SublimeLinter-contrib-elm-make)

This linter plugin for [SublimeLinter][docs] provides linting functionality for the [Elm language](http://elm-lang.org).

It will be used with files that have the elm syntax package, which can be installed from [here](http://github.com/deadfoxygrandpa/Elm.tmLanguage).


## Installation

SublimeLinter 3 must be installed in order to use this plugin. If SublimeLinter 3 is not installed, please follow the instructions [here][installation].

### Required Tools

1. [Elm](http://elm-lang.org) version 0.15.1 must be installed, and the default `elm-make` command must be in your path.

2. You must ensure that the [Elm language Sublime package](http://github.com/deadfoxygrandpa/Elm.tmLanguage) is installed.

That's it! No other installation is required, as this linter uses the built-in error reporting of the elm compiler itself.


### Plugin installation

Please use [Package Control][pc] to install the linter plugin. This will ensure that the plugin will be updated when new versions are available. If you want to install from source so you can modify the source code, you probably know what you are doing so we won’t cover that here.

To install via Package Control, do the following:

1. Within Sublime Text, bring up the [Command Palette][cmd] and type `install`. Among the commands you should see `Package Control: Install Package`. If that command is not highlighted, use the keyboard or mouse to select it. There will be a pause of a few seconds while Package Control fetches the list of available plugins.

1. When the plugin list appears, type `elm-make`. Among the entries you should see `SublimeLinter-contrib-elm-make`. If that entry is not highlighted, use the keyboard or mouse to select it.

## Settings

For information on linter settings, please see [Linter Settings][linter-settings].

`SublimeLinter-contrib-elm-make` does not have any special settings.

## Contributing

If you would like to contribute enhancements or fixes, please do the following:

1. Fork the plugin repository.
1. Hack on a separate topic branch created from the latest `master`.
1. Commit and push the topic branch.
1. Make a pull request.
1. Be patient.  ;-)

Please note that modifications should follow these coding guidelines:

- Indent is 4 spaces.
- Code should pass flake8 and pep257 linters.
- Vertical whitespace helps readability, don’t be afraid to use it.
- Please use descriptive variable names, no abbreviations unless they are very well known.

Thank you for helping out!

[docs]: http://sublimelinter.readthedocs.org
[installation]: http://sublimelinter.readthedocs.org/en/latest/installation.html
[locating-executables]: http://sublimelinter.readthedocs.org/en/latest/usage.html#how-linter-executables-are-located
[pc]: https://sublime.wbond.net/installation
[cmd]: http://docs.sublimetext.info/en/sublime-text-3/extensibility/command_palette.html
[settings]: http://sublimelinter.readthedocs.org/en/latest/settings.html
[linter-settings]: http://sublimelinter.readthedocs.org/en/latest/linter_settings.html
[inline-settings]: http://sublimelinter.readthedocs.org/en/latest/settings.html#inline-settings
