from selenium.webdriver.common.by import By

class HomePage:

    # Locators
    CURRENT_CONDITION = (By.XPATH, "//p[contains(@id,'current-weather-condition-description')]")
    HUMIDITY = (By.XPATH, "//p[contains(@id,'humidity')]/span")
    CURRENT_TEMP = (By.XPATH, "//p[contains(@id,'current-temperature')]/span")
    # TODAY-LOW
    # TODAY-HIGH
    DAY_1_TEMP = (By.XPATH, "//p/span[contains(@id,'day-1-temp')]")
    DAY_2_TEMP = (By.XPATH, "//p/span[contains(@id,'day-2-temp')]")
    DAY_3_TEMP = (By.XPATH, "//p/span[contains(@id,'day-3-temp')]")
    DRINKS_ORDERED_COUNTER = (By.XPATH, "//p[contains(@id, 'drinks-ordered')]")

    def __init__(self, driver):
        self.driver = driver