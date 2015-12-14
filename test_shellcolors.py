#!/usr/bin/python3

import shellcolors as sc
import unittest

class TestShellcolors(unittest.TestCase):
    
    def test_compile_clean(self):
        self.assertEqual(
            sc.compile("<red> foo </red>"),
            "\033[31m foo \033[39m"
        )
        self.assertEqual(
            sc.compile("<red><blue> foo </blue></red>"),
            "\033[31m\033[34m foo \033[31m\033[39m"
        )
    
    def test_compile_open(self):
        self.assertEqual(
            sc.compile("<red><blue> foo "),
            "\033[31m\033[34m foo \033[31;39m"
        )
        self.assertEqual(
            sc.compile("<red><bold><blue> foo </bold>"),
            "\033[31m\033[1m\033[34m foo \033[21m\033[31;39m"
        )
        self.assertEqual(
            sc.compile("<red><u><blue><bg_green><b> foo </underline>"),
            "\033[31m\033[4m\033[34m\033[42m\033[1m foo \033[24m\033[21;31;39;49m"
        )
    
        
    def test_compile_colors_swaped(self):
        self.assertEqual(
            sc.compile("<red> a <blue> b </red> c </blue>"),
            "\033[31m a \033[34m b \033[34m c \033[39m"
        )
    
    def test_compile_styles_swaped(self):
        self.assertEqual(
            sc.compile("<u> a <b> b </u> c </b>"),
            "\033[4m a \033[1m b \033[24m c \033[21m"
        )
    
    def test_reset(self):
        self.assertEqual(
            sc.compile("<red><bold><blue> foo <reset>"),
            "\033[31m\033[1m\033[34m foo \033[0m"
        )
        self.assertEqual(
            sc.compile("<red><bold><blue> foo </reset>"),
            "\033[31m\033[1m\033[34m foo \033[0m"
        )
    
    def test_compile_mixed_aliases(self):
        self.assertEqual(
            sc.compile("<bold> foo </bold>"),
            sc.compile("<b> foo </bold>")
        )
        self.assertEqual(
            sc.compile("<bold> foo </bold>"),
            sc.compile("<bold> foo </b>")
        )
        self.assertEqual(
            sc.compile("<bold> foo </bold>"),
            sc.compile("<strong> foo </b>")
        )
        self.assertEqual(
            sc.compile("<bold><italic> foo </italic></bold>"),
            sc.compile("<b><i> foo </italic></bold>")
        )
        self.assertEqual(
            sc.compile("<bold><italic> foo </italic></bold>"),
            sc.compile("<bold><italic> foo </i></b>")
        )
        self.assertEqual(
            sc.compile("<bold><italic> foo </italic></bold>"),
            sc.compile("<b><em> foo </i></strong>")
        )
    
    def test_style(self):
        self.assertEqual(
            sc.style("red", "foo"),
            sc.compile("<red>foo</red>")
        )
        self.assertEqual(
            sc.style("red", "bold", "foo"),
            sc.compile("<red><bold>foo</bold></red>")
        )
        self.assertEqual(
            sc.style("b", "foo"),
            sc.compile("<bold>foo</bold>")
        )
    
    def test_sprint(self):
        sc.sprint("red", "bold", "red + bold")
        
    def test_cprint(self):
        sc.cprint("<red><bold>red + bold</bold></red>")
    
    def test_style_functions(self):
        self.assertEqual(
            sc.compile("<red> foo </red>"),
            sc.red(" foo ")
        )
        self.assertEqual(
            sc.compile("<bg_red> foo </bg_red>"),
            sc.bg_red(" foo ")
        )
        self.assertEqual(
            sc.compile("<bold> foo </bold>"),
            sc.bold(" foo ")
        )
    
    def test_function_mixing(self):
        self.assertEqual(
            sc.compile("<red>" + sc.bold(sc.style("underline", " foo ")) + "</red>"),
            sc.compile("<red><b><u> foo </u></b></red>")
        )
    
# run
if __name__ == '__main__':
    unittest.main()
