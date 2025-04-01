
from driver_setup import init_driver
from zone_checker import get_zone_info


driver = init_driver()
while True: 
    lon = 48.20817
    lan= 13.37385
    print((get_zone_info(driver, f"{lon}/{lan}")).get("permission"))

