# AeroGuard AT
A drone monitoring system for Austria that tracks flight locations using GPS and barometer data, with geofencing to detect restricted zones. It stores data in a MongoDB database and provides information on the drone's position, altitude, and zone status.



## Introduction  
This project focuses on real-time **drone flight monitoring** and **restricted airspace detection** in **Austria**. A sensor system collects **GPS and altitude data** to determine if the drone is airborne and whether it is entering a restricted zone. The data is processed locally and transmitted to the cloud for **storage, analysis, and visualization**. If a restricted zone is entered, the event is **logged and displayed on a real-time dashboard**.

## Proposed Technologies  
- **Protocols:** MQTT for real-time data transmission  
- **Devices:** Raspberry Pi, GPS module (UART), Barometer (I²C)  
- **Programming Languages:** Python for data processing and cloud communication  
- **Data Storage & Processing:** Cloud database for flight history and analysis  

## Proposed Tools  
- **IDEs & Development Tools:** VS Code, GitHub  
- **Cloud Platforms:** Microsoft Azure IoT Hub for data storage (& visualization)  
- **Visualization:** Interactive dashboard for real-time and historical flight tracking (Azure Map or Flask)
