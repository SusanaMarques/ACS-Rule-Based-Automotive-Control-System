# Rule Based Automotive Control System (ACS)

This Rule-based Automotive Control System (ACS) controls, manages and regulates the behavior of various devices and subsystems in the vehicle. It assumes different behaviors according to sensory data.

## Air Conditioning Control

According to comfort temperature values, namely 15ºC Winter+Autumn and 25ºC
Spring+Summer, the SBR demonstrates the following behavior:

 - Check the season in order to identify the appropriate comfort temperature;
 - Output to a log file, for later interpretation by the ACS, of the following strings:
     - If the temperature is lower, the following text should be output to the file:
    airconditioning+{temperature ºC}*
     - If the temperature is higher, the following text should be output to the file:
    airconditioning-{temperature ºC}*
    
*ºC until reaching the comfort temperature, whether increasing or decreasing

** To learn more about this project click [here](https://github.com/SusanaMarques/ACS-Rule-Based-Automotive-Control-System/blob/main/project_report.pdf) **
