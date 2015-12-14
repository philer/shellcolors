#!/usr/bin/python3
"""
Colored/Formatted output on bash (and zsh and some others)

Create html-like style tags in your strings and have them turned into actual
styling.

Usage:
    import shellcolors
    colored_string = shellcolors.compile("<red>some <bold>text</bold></red>")
    red_string     = shellcolors.red("some text")
    shellcolors.sprint("green", "bold", "this will be printed")


Note that closing tags are expected in the correct order(strict XML).
By default all styles are closed at the end of a string.

Example:
    The following are equivalent (by default)
    "<red><blue>foo</blue></red>"
    "<red><blue>foo</red>"
    "<red><blue>foo"
    "<red><blue>foo</blue></red>"

There is a special tag <reset>, which will reset all styles to default.
This tag doesn't need to be closed.

Text colors:
    default,
    white, black, dark_grey, light_grey,
    red, green, yellow, blue, purple, cyan,
    light_red, light_green, light_yellow, light_blue, light_purple, light_cyan,

Background colors:
    All colors as bg_*

Effects:
    bold, dim, italic, underline, blink, invert, hidden, strikethrough

Not all effects are supported by all terminals. If you want to be safe your
formatting looks okay you should use only bold, underline and invert.
A good compatibility table can be found at
http://misc.flogisoft.com/bash/tip_colors_and_formatting#terminals_compatibility
"""

import sys
import re

use_colors = sys.stdout.isatty()

styles = {
    "bold":          1,
    "dim":           2,
    "italic":        3,
    "underline":     4,
    "blink":         5,
    # "blink2":        6,
    "invert":        7,
    "hidden":        8,
    "strikethrough": 9,
    
    # html versions
    "b":      1,
    "strong": 1,
    "i":      3,
    "em":     3,
    "u":      4,
    "s":      9,
}
style_end_add = 20 # e.g. end_bold = 21

colors = {
    "default":      39,

    "black":        30,
    "red":          31,
    "green":        32,
    "yellow":       33,
    "blue":         34,
    "purple":       35,
    "cyan":         36,
    "light_grey":   37,

    "dark_grey":    90,
    "light_red":    91,
    "light_green":  92,
    "light_yellow": 93,
    "light_blue":   94,
    "light_purple": 95,
    "light_cyan":   96,
    "white":        97,
}

bg_colors = dict([ ("bg_" + color, code + 10) for color, code in colors.items() ])

all_styles = styles.copy()
all_styles.update(colors)
all_styles.update(bg_colors)


### core function ###

def compile(string, autoclose = True):
    """
    apply styles defined by xml-esque substrings
    """
    
    stack = []
    
    # regex substitutions need access to local stack
    def substitute(match):
        nonlocal stack
        
        style = match.group(2)
        
        if style == "reset":
            stack = []
            return "\033[0m" if use_colors else ""
            
        elif not style in all_styles:
            return match.group(0)
        
        if not use_colors:
            return ""
        
        # closing tag
        if match.group(1) == '/':
            
            # close first matching style on the stack
            for i, close in reversed(list(enumerate(stack))):
                
                # we check codes rather than names to allow alias mixing
                if all_styles[close] == all_styles[style]:
                    del stack[i]
                    return "\033[" + str(_close_style(close, stack)) + "m"
        
        # opening tag
        else:
            stack.append(style)
            return "\033[" + str(all_styles[style]) + "m"
    
    # run the substitutions
    string = re.sub(r'<(/?)([^>]*)>', substitute, string)
    
    # finish unclosed tags
    if autoclose and stack:
        codes = set()
        while stack:
            close = stack.pop()
            codes.add(_close_style(close, stack))
        
        string += "\033[" + ";".join(map(str, sorted(codes))) + "m"
    
    return string


def _close_style(style, stack):
    
    # colors are closed by re-enabling the previous color
    if style in colors:
        for s in reversed(stack):
            if s in colors:
                return colors[s]
        return colors["default"]

    if style in bg_colors:
        for s in reversed(stack):
            if s in bg_colors:
                return bg_colors[s]
        return bg_colors["bg_default"]

    # styles are closed by using their corresponding end
    return styles[style] + style_end_add
    



### convenience function ###

def style(*args):
    """
    apply all given styles to a string
    """
    styles = list(args)
    string = styles.pop()
    for style in reversed(styles):
        string = "<" + style + ">" + string + "</" + style + ">"
    return compile(string)

def cprint(*strings):
    """
    compile all given strings and print them
    """
    print(*map(compile, strings))

def sprint(*args):
    """
    style a string and print it
    """
    print(style(*args))


# create a function for each style
def _define_shortcut(s):
    def style_shortcut(string):
        return style(s, string)
    return style_shortcut

for s in all_styles.keys():
    locals()[s] = _define_shortcut(s)


log_levels = {
    'info':    ['default'],
    'warning': ['yellow', 'italic'],
    'error':   ['red',    'bold'],
    'success': ['green'],
}

def log(string, level = 'info'):
    args = log_levels[level].copy()
    args.append(string)
    sprint(*args)


