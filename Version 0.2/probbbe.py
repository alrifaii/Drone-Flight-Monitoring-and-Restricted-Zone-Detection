from driver_setup import init_driver
from zone_checker import get_info_div, get_zone_info


driver = init_driver()
while True: 
    ab = input(": ")
    print(get_info_div(driver,ab).info_html)
    print(get_zone_info(driver,ab))