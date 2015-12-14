# shellcolors.py
Style your commandline output from python scripts

### How it works:
1. Embed XML-like tags into a string, for example
`"This is <green>an example</green>."`
2. The recognized tags will be converted to escaped **ANSI/VT100 control sequences**.

### Usage:

```python
import shellcolors

# basic
raw = "some <greeb>string</green> with <red><bold>styling</bold></red>"
styled = shellcolors.compile(raw)
print(styled)

# style an entire string
styled = shellcolors.style("yellow", "bold", "This string will be yellow and bold.")
print(styled)

# style/compile a string and print it directly
shellcolors.cprint("some <greeb>string</green> with <red><bold>styling</bold></red>")
shellcolors.sprint("yellow", "bold", "This string will be yellow and bold.")

# all colors and styles are available as a function
print(shellcolors.blue("This string will be blue"))
```
On my urxvt terminal the output of the above looks like this:

![screenshot](https://raw.githubusercontent.com/philer/shellcolors/master/screenshot.png)


### Requirements
* Python 3 (does not work with Python 2.7)
* A terminal that supports ANSI/VT100 Control sequences. See [this excellent compatibility table](http://misc.flogisoft.com/bash/tip_colors_and_formatting#terminals_compatibility).

### Available colors and styles
All styles available through ANSI/VT100 Control sequences can be used,
including a few non-standard ones that are commonly supported by terminal emulators.

* Colors:
    + **`default`**
    + **`black`**, **`dark_grey`**, **`light_grey`**, **`white`**
    + **`red`**, **`green`**, **`yellow`**, **`blue`**, **`purple`**, **`cyan`**
    + **`light_red`**, **`light_green`**, **`light_yellow`**, **`light_blue`**, **`light_purple`**, **`light_cyan`**
* Background colors: Same as foreground with a **`bg_`** prefix (e.g. `bg_dark_grey`)
* Styles: (some with aliases)
    + **`bold`** = `bright` = `b` = `strong`
    + **`italic`** = `i` = `em`
    + **`underline`** = `underlined` = `u`
    + **`strikethrough`** = `s`
    + **`invert`** = `reverse`
    + **`dim`**
    + **`hidden`**
    + **`blink`** (please don't use it…)
    
