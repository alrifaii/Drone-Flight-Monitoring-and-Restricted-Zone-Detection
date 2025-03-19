# Drone-Flight-Monitoring-and-Restricted-Zone-Detection
A drone flight monitoring system for Austria that detects restricted zone violations using GPS and barometer data, processes alerts on a Raspberry Pi, and stores flight history in Azure IoT Hub for real-time visualization.



## Introduction  
This project focuses on real-time **drone flight monitoring** and **restricted airspace detection** in **Austria**. A sensor system collects **GPS and altitude data** to determine if the drone is airborne and whether it is entering a restricted zone. The data is processed locally and transmitted to the cloud for **storage, analysis, and visualization**. If a restricted zone is entered, the event is **logged and displayed on a real-time dashboard**.

## Proposed Technologies  
- **Protocols:** MQTT for real-time data transmission  
- **Devices:** Raspberry Pi, GPS module, Barometer  
- **Programming Languages:** Python for data processing and cloud communication  
- **Data Storage & Processing:** Cloud database for flight history and analysis  

## Proposed Tools  
- **IDEs & Development Tools:** VS Code, GitHub  
- **Cloud Platforms:** Microsoft Azure IoT Hub for data storage (& visualization)  
- **Visualization:** Interactive dashboard for real-time and historical flight tracking (Azure Map or Flask)
