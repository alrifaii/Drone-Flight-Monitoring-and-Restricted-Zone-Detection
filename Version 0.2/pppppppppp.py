from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

def check_flight_permission(zones):
    """Überprüft, ob das Fliegen erlaubt ist."""
    restricted_keywords = ["Authorization required", "Air traffic control clearance required"]
    
    for zone in zones:
        details = zone.text
        if any(keyword in details for keyword in restricted_keywords):
            return "🚫 Flying not allowed"
    return "✅ Flying allowed"

def get_zone_info(driver, cord):
    """Ruft Zoneninformationen für gegebene Koordinaten ab."""
    try:
        new_url = f"window.location.href = 'https://utm.dronespace.at/avm/#p=11.95/{cord}'"
        driver.execute_script(new_url)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "map"))
        )

        map_element = driver.find_element(By.ID, "map")
        actions = ActionChains(driver)
        actions.move_to_element_with_offset(map_element, map_element.size['width'] // 2, map_element.size['height'] // 2).click().perform()

        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, "info-feature"))
        )

        zones = driver.find_elements(By.CLASS_NAME, "info-feature")
        print(zones.get_attribute("outerHTML"))
        zone_info = []
        for zone in zones:
            try:
                name = zone.find_element(By.CLASS_NAME, "name").text
                details = zone.text
                zone_info.append((name, details))
            except Exception:
                pass

        permission = check_flight_permission(zones)

        return {"zones": zone_info, "permission": permission}

    except Exception as e:
        return {"error": str(e)}
