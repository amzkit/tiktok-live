#!/usr/bin/env python
"""A simple cmd2 application."""
import cmd2
import time
import argparse
import subprocess
import threading
from queue import Queue 


def callback():
    process = subprocess.run(['python', 'flashsale_click_15.py'])

class FirstApp(cmd2.Cmd):

    """A simple cmd2 application."""

    speak_parser = cmd2.Cmd2ArgumentParser()
    speak_parser.add_argument('-p', '--piglatin', action='store_true', help='atinLay')
    speak_parser.add_argument('-s', '--shout', action='store_true', help='N00B EMULATION MODE')
    speak_parser.add_argument('-r', '--repeat', type=int, help='output [n] times')
    speak_parser.add_argument('words', nargs='+', help='words to say')

    @cmd2.with_argparser(speak_parser)
    def do_speak(self, args):
        """Repeats what you tell me to."""
        words = []
        for word in args.words:
            if args.piglatin:
                word = '%s%say' % (word[1:], word[0])
            if args.shout:
                word = word.upper()
            words.append(word)
        repetitions = args.repeat or 1
        for _ in range(min(repetitions, self.maxrepeats)):
            # .poutput handles newlines, and accommodates output redirection too
            self.poutput(' '.join(words))

    def do_start(self, args):
        threads = threading.Thread(target=callback)
        threads.start()

    def do_stop(self, args):
        
        

if __name__ == '__main__':
    import sys
    c = FirstApp()
    sys.exit(c.cmdloop())


browser.switch_to.window(browser.window_handles[1])
product_tab = WebDriverWait(browser, 3).until(ExpectedConditions.presence_of_element_located((By.XPATH, "//span[@class='text-headingL hover:text-text1 transition-colors text-text3'][contains(text(),'สินค้า')]")))
product_tab.click()
product_tab.find_elements(By.XPATH, "//span[@class='text-headingL hover:text-text1 transition-colors text-text3'][contains(text(),'สินค้า')]")
live_board_buttons = browser.find_elements(By.XPATH, live_board_button_xpath)



live_board_buttons[i].click()
browser.switch_to.window(browser.window_handles[0])
live_board_button_xpath = "//div[@class='flex flex-col w-full']//div[@class='flex justify-between']//div[1]//button[1]"
live_board_buttons = browser.find_elements(By.XPATH, live_board_button_xpath)
print('['+time.strftime('%H:%M')+'][Product] live board opened')

