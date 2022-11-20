import os
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from dotenv import load_dotenv

import time
from app.decrypt import Decrypt

from app.firebase_util import update_available_rooms


class RoomBooker:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("window-size=1920,1080")
        chrome_options.add_argument("disable-dev-shm-usage")
        chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36")

        self.driver = webdriver.Chrome(
            chrome_options=chrome_options, executable_path=ChromeDriverManager().install())
                



    def is_logged_in(self):
        print("Checking if logged in")
        # if class with _wx_s exists
        try:
            self.driver.find_element(By.CLASS_NAME, "_wx_s")
            return True
        except:
            return False

    def login(self, p, u):

        self.driver.implicitly_wait(5000)
        link = "https://mail.uio.no/owa/#path=/calendar"
        self.driver.get(link)
        self.driver.implicitly_wait(5000)

        self.driver.find_element(
            By.ID, "username").send_keys(u)
        self.driver.find_element(
            By.ID, "password").send_keys(p)
        self.driver.find_element(By.ID, "password").submit()

        time.sleep(1)
        print("Logged in")
        self.driver.get(
            "https://mail.uio.no/owa/#path=/calendar/view/Month")

        while True:
            if self.driver.current_url != "https://mail.uio.no/owa/#path=/calendar/view/Month":
                self.driver.get(
                    "https://mail.uio.no/owa/#path=/calendar/view/Month")
                time.sleep(1)
            else:
                break

        print("Calendar loaded")

    def get_available_rooms(self, building_, year, month, day, start_time, end_time):
        print("Getting available rooms")
        self.driver.implicitly_wait(5000)

        # find all buttons inside div with class _wx_s
        buttons = self.driver.find_element(
            By.CLASS_NAME, "_wx_s").find_elements(By.TAG_NAME, "button")
        if len(buttons) > 0:
            buttons[0].click()

        print("Passing in the time")
        self.driver.implicitly_wait(5000)

        self.book_time(year, month, day, start_time, end_time)
        print("time checked")
        time.sleep(1)

        print("Finding the building")
        self.driver.implicitly_wait(5000)
        self.driver.find_element(By.CSS_SELECTOR, "form[action='javascript:void(0);']").find_element(
            By.TAG_NAME, "input").click()
        self.driver.implicitly_wait(5000)
        self.driver.find_element(
            By.CSS_SELECTOR, "button._lw_a._lw_b.ms-font-weight-regular.ms-font-color-black.o365button").click()
        self.driver.implicitly_wait(5000)

        # Find the buildings
        build_list = self.driver.find_elements(
            By.XPATH, "//button/span[contains(text(), 'Choose new room list')]")
        self.driver.implicitly_wait(5000)
        build_list[0].click()

        # find the buildings
        self.driver.implicitly_wait(5000)
        div_with_rooms = self.driver.find_element(
            By.CSS_SELECTOR, "div[aria-label='List of room lists']").find_element(By.TAG_NAME, "div")
        # Select the building
        buildings = div_with_rooms.find_elements(By.TAG_NAME, "div")
        self.driver.implicitly_wait(10000)
        building_found = False
        b = []
        for building in buildings:
            b.append(building.find_element(By.TAG_NAME, "span").text)
            if building.find_element(By.TAG_NAME, "span").text.__contains__(building_):
                print("Found the room " +
                      building.find_element(By.TAG_NAME, "span").text)
                self.driver.implicitly_wait(5000)
                building.click()
                building_found = True
                break

        print("Building found")

        if not building_found:
            print("Building not found")
            return

        self.driver.implicitly_wait(5000)
        free_rooms = self.driver.find_element(
            By.CSS_SELECTOR, "div[aria-label='List of rooms']").find_elements(By.TAG_NAME, "span")

        print("Found " + str(len(free_rooms)) + " free rooms")
        free_room_list = []
        for room in free_rooms:
            free_room_list.append(room.text)

        free_room_list = [x for x in free_room_list if x !=
                          "(Free)" and x != "AVAILABLE"]
        self.driver.implicitly_wait(5000)
        self.driver.find_element(
            By.CSS_SELECTOR, "button[aria-label='Close']").click()
        self.driver.implicitly_wait(5000)
        self.driver.find_element(
            By.CSS_SELECTOR, "button._db_9.o365button.o365buttonOutlined.ms-font-m.ms-fwt-sb.ms-fcl-np.ms-bgc-nlr.ms-bcl-nlr.ms-fcl-b-f.ms-bcl-tp-f").click()

        self.driver.implicitly_wait(5000)
        self.driver.find_element(
            By.CSS_SELECTOR, "button[aria-label='Close']").click()
        self.driver.implicitly_wait(5000)

        return free_room_list

    def book_room(self, title, building_, room_):
        if self.driver.find_element(By.CLASS_NAME, "_wx_s"):
            self.driver.find_element(By.CLASS_NAME, "_wx_s").find_element(
                By.TAG_NAME, "button").click()

        self.driver.implicitly_wait(5000)
        self.driver.find_element(
            By.CSS_SELECTOR, "input[placeholder='Add a title for the event']").send_keys(title)
        self.driver.implicitly_wait(5000)
        self.driver.find_element(By.CSS_SELECTOR, "form[action='javascript:void(0);']").find_element(
            By.TAG_NAME, "input").click()
        self.driver.implicitly_wait(5000)
        self.driver.find_element(
            By.CSS_SELECTOR, "button._lw_a._lw_b.ms-font-weight-regular.ms-font-color-black.o365button").click()

        # Find the buildings
        build_list = self.driver.find_elements(
            By.XPATH, "//button/span[contains(text(), 'Choose new room list')]")
        self.driver.implicitly_wait(5000)
        build_list[0].click()

        # find the buildings
        self.driver.implicitly_wait(5000)
        div_with_rooms = self.driver.find_element(
            By.CSS_SELECTOR, "div[aria-label='List of room lists']").find_element(By.TAG_NAME, "div")

        # Select the building
        buildings = div_with_rooms.find_elements(By.TAG_NAME, "div")
        self.driver.implicitly_wait(10000)
        for building in buildings:
            if building.find_element(By.TAG_NAME, "span").text.__contains__(building_):
                print("Found the room " + building.find_element(By.TAG_NAME,
                      "span").text + " and clicked it")
                self.driver.implicitly_wait(5000)
                building.click()
                break

        # Select the room
        self.driver.implicitly_wait(5000)
        free_rooms = self.driver.find_element(
            By.CSS_SELECTOR, "div[aria-label='List of rooms']").find_elements(By.TAG_NAME, "span")
        found = False
        for room in free_rooms:
            if room.text.__contains__(room_):
                self.driver.implicitly_wait(5000)
                room.find_element(By.XPATH, "..").click()
                found = True
                break

        if not found:
            free_rooms[0].find_element(By.XPATH, "..").click()

    def book_time(self, year, month, day, start_time_, end_time_):
        self.driver.implicitly_wait(5000)
        print("Selecting the time")
        self.driver.find_element(By.CLASS_NAME, "startDatePicker").find_element(
            By.TAG_NAME, "button").click()
        self.driver.implicitly_wait(5000)
        buttons = self.driver.find_element(
            By.CLASS_NAME, "_dx_8").find_elements(By.TAG_NAME, "button")
        m_forward = buttons[2]
        year_month = buttons[1].get_attribute("aria-label").split(" ")
        m = year_month[1]
        y = year_month[0]
        print("Current month is " + m + " and current year is " + y)
        while True:
            if str(y) == str(year) and str(m) == str(month):
                break
            else:
                m_forward.click()
                self.driver.implicitly_wait(5000)
                buttons = self.driver.find_element(
                    By.CLASS_NAME, "_dx_8").find_elements(By.TAG_NAME, "button")
                month_year = buttons[1].get_attribute("aria-label").split(" ")
                m = month_year[1]
                y = month_year[0]
        print("Found the month and year")
        # find the correct day
        self.driver.implicitly_wait(5000)
        # select all day tags
        days = self.driver.find_element(
            By.CLASS_NAME, "_dx_8").find_elements(By.TAG_NAME, "abbr")
        d = days
        if int(day) > 10:
            for day_ in reversed(d):
                t = str(day_.text)
                if t == str(day):
                    day_.click()
                    break
        else:
            for day_ in d:
                t = str(day_.text)

                if t == str(day):
                    day_.click()
                    break
        print("Found the day")
        # change the start time
        self.driver.implicitly_wait(5000)
        start_time = self.driver.find_element(
            By.CLASS_NAME, "startTimePicker").find_element(By.TAG_NAME, "input")
        # click the start time
        start_time.click()
        print("Found the start time")
        for i in range(5):
            start_time.send_keys(Keys.BACKSPACE)
        self.driver.implicitly_wait(5000)
        start_time.send_keys(start_time_)
        print("Changed the start time")
        # Change the end time
        self.driver.implicitly_wait(5000)
        end_time = self.driver.find_elements(
            By.CLASS_NAME, "_dx_q")[-1].find_element(By.TAG_NAME, "input")
        # click the end time
        end_time.click()
        for i in range(5):
            end_time.send_keys(Keys.BACKSPACE)
        self.driver.implicitly_wait(5000)
        end_time.send_keys(end_time_)

        print("Changed the time")

    def set_message(self, text):
        self.driver.implicitly_wait(5000)
        self.driver.find_element(By.CLASS_NAME, "_cx_42").click()
        self.driver.implicitly_wait(5000)
        self.driver.find_element(
            By.CSS_SELECTOR, "div[aria-label='Event body']").send_keys(text)

    def add_people(self, attendees):
        for i in range(len(attendees)):
            self.driver.implicitly_wait(5000)
            self.driver.find_element(
                By.CSS_SELECTOR, "input[aria-label='Add people']").send_keys(attendees[i])
            self.driver.implicitly_wait(5000)
            time.sleep(0.5)
            self.driver.implicitly_wait(5000)
            self.driver.find_element(
                By.CSS_SELECTOR, "input[autoid='_fp_0']").send_keys(Keys.ENTER)
            time.sleep(0.5)

    def send(self):
        self.driver.implicitly_wait(5000)
        self.driver.find_element(
            By.CSS_SELECTOR, "button[aria-label='Send']").click()
        print("Sent the meeting request")

    def book(self, building, room, year, month, day, start_time, end_time, title, text, attendees):
        try:
            self.book_room(title, building, room)
            self.book_time(year, month, day, start_time, end_time)

            if text != "":
                self.set_message(text)

            if len(attendees) != 0:
                self.add_people(attendees)

            self.send()

            return True

        except Exception as e:
            return False

        finally:
            time.sleep(2)
            self.driver.get(
                "https://mail.uio.no/owa/#path=/calendar")
            # self.driver.quit()

    def update_availability(self):
        if self.is_logged_in() == False:
            d = Decrypt()
            load_dotenv()
            p = os.environ['PASS_KEY']
            u = os.environ['USER_KEY']
            if not p:
                p = os.getenv('PASS_KEY')
                u = os.getenv('USER_KEY')
            p = d.decrypt(p + "==")
            u = d.decrypt(u + "==")

            self.login(p, u)

        durations = [4, 3, 2, 1, 0.5]
        last_room_and_duration = {}
        first_time = True
        for duration in durations:
            building = "Kollokvierom i Ole-Johan Dahls hus"
            year = datetime.now().year
            # in the format of "January"
            month = datetime.now().strftime("%B")
            day = datetime.now().day
            start_time = datetime.now().strftime("%H:%M")

            # if time is over 24:00
            if int(start_time.split(":")[0]) + duration > 24:
                diff = int(start_time.split(":")[0]) + duration - 24
                day += 1
                start_time = "0" + str(diff) + ":00"

            end_time = (datetime.now() + timedelta(hours=duration)
                        ).strftime("%H:%M")

            rooms = self.get_available_rooms(
                building, year, month, day, start_time, end_time)

            if len(rooms) != 0:
                for room in rooms:
                    if room not in last_room_and_duration.keys():
                        last_room_and_duration[room] = duration
                    else:
                        if duration > last_room_and_duration[room]:
                            last_room_and_duration[room] = duration

            update_available_rooms(
                rooms, duration, last_room_and_duration, first_time)
            first_time = False

