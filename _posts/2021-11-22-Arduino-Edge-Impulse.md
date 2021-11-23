---
layout: post
title: "Set Arduino Tiny ML Kit up in Edge Impulse"
categories: tinyml
---
I've bought Arduino Tiny Machine Learning Kit for my tiny machine learning projects. As a start, I'm taking the lecture: Introduction to Embedded Machine Learning from Coursera. To set the device up to Edge impulse you need to install Edge Impulse CLI and Arduino CLI. 
Here you can find some tips so that you don't deal with errors during the installation: 
Remember that those tips are valid for Windows OS. 

### 1. Sign up to edge impulse and create a project. 


### 2. Install Edge Impulse CLI: 

- [https://docs.edgeimpulse.com/docs/cli-installation](https://docs.edgeimpulse.com/docs/cli-installation)
- Make sure that you **download  Visual Studio Community (using the "Desktop development with C++" workload).** 
- Download the latest version of python. 
- Install node.js from: https://nodejs.org/en/
- **Install the additional tools when installing NodeJS.** 

<div class="fig figcenter fighighlight">
  <img src="/assets/tinyml_images/nodejs.PNG" width="60%">
  <div class="figcaption">Figure 1: Node.js download</div>
</div>

- Check this website for additional configurations: [https://github.com/nodejs/node-gyp#on-windows](https://github.com/nodejs/node-gyp#on-windows)
  
- Set msvs version
  
    `$npm config set msvs_version 2017`

- If you have multiple Python versions installed, **you need to identify which Python version node-gyp should use**: 
  [https://github.com/nodejs/node-gyp#on-windows]

    `$npm config set python /path/to/executable/python`

- Additional info can be found here: [https://github.com/Microsoft/nodejs-guidelines](https://github.com/Microsoft/nodejs-guidelines/blob/master/windows-environment.md#compiling-native-addon-modules)
- Install CLI tools via: 
  
    `$npm install -g edge-impulse-cli --force`

(Note that before python config and downloading visual studio community, I got plenty of errors during installation of CLI tools. )

### 3. Install Arduino CLI 

- Install Arduino CLI to your C:/ directory from [https://arduino.github.io/arduino-cli/0.20/installation/](https://arduino.github.io/arduino-cli/0.20/installation/). Then add the Arduino 
  CLI installation path to your PATH environment variable. 
- Run the following commands:
  
    `$ arduino-cli core list`
  
    `$ arduino-cli board list`

For me, those commands were both empty :( I will explain the solution in a minute. 

### 4. Update the firmware
- You need to download the latest Edge Impulse firmware and unzip the file: 
  [https://docs.edgeimpulse.com/](https://docs.edgeimpulse.com/docs/arduino-nano-33-ble-sense#2-update-the-firmware)
- Open flash_windows.bat to flash the firmware. 
- Wait until it is completed. 
  
  `Here, I got this error: Unknown FQBN: platform arduino:mbed is not installed`

If you don't care about this error and jump to the last step (like me!) with the command 

    $edge-impulse-daemon

you will get timeout errors.  :)

  `Failed to get info off device Timeout when waiting for >  (timeout: 5000) onConnected`

Let's turn back to Step 3. All these errors are coming from the arduino:mbed installation.
I searched for the solution from the following websites:

- [forum_egde_impulse_1](https://forum.edgeimpulse.com/t/incorrect-fqbn-error-installing-ei-firmware-for-arduino-nano-33ble-sense/1372/12)
- [forum_egde_impulse_2](https://forum.edgeimpulse.com/t/arduino-cli-version/1332/6)
- [forum_egde_impulse_3](https://forum.edgeimpulse.com/t/issue-uploading-edge-impulse-firmware-for-nano/1683/2)
- [forum_egde_impulse_4](https://forum.arduino.cc/t/problem-uploading-to-new-board-arduino-nano-33-ble/685958) 
- [get_start_with_arduino_1](https://create.arduino.cc/projecthub/B45i/getting-started-with-arduino-cli-7652a5)
- [get_start_with_arduino_1](https://docs.arduino.cc/software/ide-v1/tutorials/getting-started/cores/arduino-mbed_nano)


Here you can find what I did to solve this problem:
- Download Arduino IDE. 
- Download: Tools/Board Manager/ Arduino Mbed OS Nano Boards

I think it is not helpful since $arduino-cli core list is still empty!

- Run the following command:
  
    `$ arduino-cli core install arduino:mbed --> This gets error.`
  
- Close the firewall and run the command above again. It works! 
- Don't forget to open the firewall. 
  
    `$ arduino-cli core list`
  
    `$ arduino-cli board list`  are not empty!

I updated the firmware without getting any errors (Step 4). 

Then, with the latest step `$edge-impulse-daemon`, I've achieved to load my device to edge impulse :)


    `Edge Impulse serial daemon v1.13.16
    Endpoints:
        Websocket: wss://remote-mgmt.edgeimpulse.com
        API:       https://studio.edgeimpulse.com/v1
        Ingestion: https://ingestion.edgeimpulse.com
    
    ? Which device do you want to connect to? COM3 (Microsoft)
    [SER] Connecting to COM3
    [SER] Serial is connected, trying to read config...
    [SER] Retrieved configuration
    [SER] Device is running AT command version 1.6.0
    
    ? To which project do you want to connect this device? Pelin / arduino_motion
    Setting upload host in device... OK
    Configuring remote management settings... OK
    Configuring API key in device... OK
    Configuring HMAC key in device... OK
    [SER] Device is not connected to remote management API, will use daemon
    [WS ] Connecting to wss://remote-mgmt.edgeimpulse.com
    [WS ] Connected to wss://remote-mgmt.edgeimpulse.com
    ? What name do you want to give this device? pelin's arduino
    [WS ] Device "pelin's arduino" is now connected to project "arduino_motion"
    [WS ] Go to https://studio.edgeimpulse.com/studio/62428/acquisition/training to build your machine learning model!`

<div class="fig figcenter fighighlight">
  <img src="/assets/tinyml_images/device.PNG" width="90%">
  <div class="figcaption">Figure 2: Finally! :) </div>
</div>


## Key Words
Tiny ML, Arduino, Edge Impulse, Timeout, arduino:mbed



