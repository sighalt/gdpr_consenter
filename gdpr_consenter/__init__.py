import time
import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class PopupClicker(object):

    def __init__(self, url, css_selector, max_wait_for_popups_time=30,
                 popup_wait_interval=.5):
        self.url = url
        self.css_selector = css_selector
        if max_wait_for_popups_time % popup_wait_interval != 0:
            warnings.warn("max wait time is not a multiple of the wait interval")

        self.max_wait_for_popups_time = max_wait_for_popups_time
        self.popup_wait_interval = popup_wait_interval
        self.driver = None

    def __enter__(self):
        print("[+] Opening website...")
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.driver.get(self.url)
        time.sleep(5)
        return self

    def __exit__(self, type, value, traceback):
        self.driver.close()

    @property
    def popups(self):
        return self.driver.find_elements_by_css_selector(self.css_selector)

    def wait_for_popups_to_stop(self):
        print("[+] Waiting for popups to stop...")
        already_waited = 0
        last_num_popups = None
        full_cycles = int(self.max_wait_for_popups_time / self.popup_wait_interval)

        for _ in range(full_cycles):
            num_popups = len(self.popups)

            if last_num_popups is None or num_popups > last_num_popups:
                last_num_popups = num_popups
                time.sleep(self.popup_wait_interval)
                continue

            break

    def click_popups(self):
        print("[+] Clicking popups...")
        js_code = """var elems = document.querySelectorAll('%s');
        for(var i= 0;i<elems.length;i++){
            elems[i].click();
        }""" % self.css_selector
        self.driver.execute_script(js_code)
        print("[+] Congratulations, the website is now ready to use")
    

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("url")
    argparser.add_argument("css_selector")
    args = argparser.parse_args()
    
    with PopupClicker(args.url, args.css_selector) as clicker:
        clicker.wait_for_popups_to_stop()
        clicker.click_popups()
        time.sleep(60*60*24)


if __name__ == "__main__":
    main()

