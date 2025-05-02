from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def init_driver():
    """Initialisiert den WebDriver und öffnet die Webseite."""
    driver = webdriver.Chrome()
    driver.get("https://utm.dronespace.at/avm/")

    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.ID, "map"))
        )
        
        # Automatische Bestätigung der Nutzungsbedingungen
        try:
            accept_button = WebDriverWait(driver, 2).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="terms"]/div[2]/div/div[2]'))
            )
            accept_button.click()
            print("Nutzungsbedingungen bestätigt")
        except Exception:
            pass  # Falls die Nutzungsbedingungen nicht erscheinen, einfach weitermachen
    except Exception as e:
        print(f"Fehler beim Initialisieren des WebDrivers: {e}")

    return driver
