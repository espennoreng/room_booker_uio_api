from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


class GetRooms:
    def __init__(self, building, year, month, day, start_time, end_time, password, username):
        self.building = building
        self.year = year
        self.month = month
        self.day = day
        self.start_time = start_time
        self.end_time = end_time
        self.password = password
        self.username = username


    def get_available_rooms(self):
        print("Starting the driver")
        chrome_options = Options()
        chrome_options.add_argument("window-size=1920,1080")
        chrome_options.add_argument("disable-dev-shm-usage")
        self.driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=ChromeDriverManager().install())
        print("Driver started")
        self.driver.implicitly_wait(5000)
        self.link = "https://mail.uio.no/owa/#path=/calendar"
        self.driver.get(self.link)
        self.driver.implicitly_wait(5000)

        print("Logging in")

        if self.driver.find_element(By.ID, "username"):
            self.driver.find_element(By.ID, "username").send_keys(self.username)
            self.driver.find_element(By.ID, "password").send_keys(self.password)
            self.driver.find_element(By.ID, "password").submit()

        time.sleep(1)
        print("Logged in")
        self.driver.get("https://mail.uio.no/owa/#path=/calendar/view/Month")

        while True:
            if self.driver.current_url != "https://mail.uio.no/owa/#path=/calendar/view/Month":
                self.driver.get("https://mail.uio.no/owa/#path=/calendar/view/Month")
                time.sleep(1)
            else:
                break

        print("Calendar loaded")


        print("Getting available rooms")
        self.driver.implicitly_wait(5000)

        # find all buttons inside div with class _wx_s
        buttons = self.driver.find_element(By.CLASS_NAME, "_wx_s").find_elements(By.TAG_NAME, "button")
        self.driver.implicitly_wait(5000)
        buttons[0].click()


        print("Passing in the time")
        self.driver.implicitly_wait(5000)

            
        self.driver.implicitly_wait(5000)
        self.driver.find_element(By.CLASS_NAME, "startDatePicker").find_element(By.TAG_NAME, "button").click()
        self.driver.implicitly_wait(5000)
        buttons = self.driver.find_element(By.CLASS_NAME, "_dx_8").find_elements(By.TAG_NAME, "button")
        m_forward = buttons[2]
        year_month= buttons[1].get_attribute("aria-label").split(" ")
        m = year_month[1]
        y = year_month[0]

        while True:
            if str(y) == str(self.year) and str(m) == str(self.month):
                break
            else:
                m_forward.click()
                self.driver.implicitly_wait(5000)
                buttons = self.driver.find_element(By.CLASS_NAME, "_dx_8").find_elements(By.TAG_NAME, "button")
                month_year = buttons[1].get_attribute("aria-label").split(" ")
                m = month_year[1]
                y = month_year[0]

        # find the correct day
        self.driver.implicitly_wait(5000)

        # select all day tags 
        days = self.driver.find_element(By.CLASS_NAME, "_dx_8").find_elements(By.TAG_NAME, "abbr")
        d = days
        if int(self.day) > 10:
            for day_ in reversed(d):
                t = str(day_.text)
                if t == str(self.day):
                    day_.click()
                    break
        else:
            for day_ in d:
                t = str(day_.text)
           
                if t == str(self.day):
                    day_.click()
                    break

        # change the start time
        self.driver.implicitly_wait(5000)
        start_time = self.driver.find_element(By.CLASS_NAME, "startTimePicker").find_element(By.TAG_NAME, "input")
        for i in range(5):
            start_time.send_keys(Keys.BACKSPACE)
        self.driver.implicitly_wait(5000)
        start_time.send_keys(self.start_time)

        # Change the end time 
        self.driver.implicitly_wait(5000)
        end_time = self.driver.find_elements(By.CLASS_NAME, "_dx_q")[-1].find_element(By.TAG_NAME, "input")
        for i in range(5):
            end_time.send_keys(Keys.BACKSPACE)
        self.driver.implicitly_wait(5000)
        end_time.send_keys(self.end_time)


        print("time checked")
        time.sleep(1)

        print("Finding the building")
        self.driver.implicitly_wait(5000)
        self.driver.find_element(By.CSS_SELECTOR, "form[action='javascript:void(0);']").find_element(By.TAG_NAME, "input").click()
        self.driver.implicitly_wait(5000)
        self.driver.find_element(By.CSS_SELECTOR, "button._lw_a._lw_b.ms-font-weight-regular.ms-font-color-black.o365button").click()
        self.driver.implicitly_wait(5000)

        # Find the buildings
        build_list  = self.driver.find_elements(By.XPATH, "//button/span[contains(text(), 'Choose new room list')]")
        self.driver.implicitly_wait(5000)
        build_list[0].click()

        # find the buildings
        self.driver.implicitly_wait(5000)
        div_with_rooms = self.driver.find_element(By.CSS_SELECTOR, "div[aria-label='List of room lists']").find_element(By.TAG_NAME, "div")
        # Select the building
        buildings = div_with_rooms.find_elements(By.TAG_NAME, "div")
        self.driver.implicitly_wait(10000)
        building_found = False
        b = []
        for building in buildings:
            b.append(building.find_element(By.TAG_NAME, "span").text)
            if building.find_element(By.TAG_NAME, "span").text.__contains__(self.building):
                print("Found the room " + building.find_element(By.TAG_NAME, "span").text)
                self.driver.implicitly_wait(5000)
                building.click()
                building_found = True
                break

        print("Building found")
        
        if not building_found:
            print("Building not found")
            return

        self.driver.implicitly_wait(5000)
        free_rooms =  self.driver.find_element(By.CSS_SELECTOR, "div[aria-label='List of rooms']").find_elements(By.TAG_NAME, "span")

        print("Found " + str(len(free_rooms)) + " free rooms")
        free_room_list = []
        for room in free_rooms:
            free_room_list.append(room.text)

        free_room_list = [x for x in free_room_list if x != "(Free)" and x != "AVAILABLE"]
        self.driver.implicitly_wait(5000)
        self.driver.find_element(By.CSS_SELECTOR, "button[aria-label='Close']").click()
        self.driver.implicitly_wait(5000)
        self.driver.find_element(By.CSS_SELECTOR, "button._db_9.o365button.o365buttonOutlined.ms-font-m.ms-fwt-sb.ms-fcl-np.ms-bgc-nlr.ms-bcl-nlr.ms-fcl-b-f.ms-bcl-tp-f").click()

        # quit driver
        self.driver.quit()

        return free_room_list

