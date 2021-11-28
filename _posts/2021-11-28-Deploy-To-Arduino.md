---
layout: post
title: "How to Deploy Model to Arduino?"
categories: tinyml
---

"You can deploy your impulse to any device. This makes the model run without an internet connection, 
minimizes latency, and runs with minimal power consumption."

Please check this website: [https://docs.edgeimpulse.com/docs/running-your-impulse-arduino](https://docs.edgeimpulse.com/docs/running-your-impulse-arduino)

- Go to your project from Edge Impulse, click Deployment.
- Select Arduino from Deploy your impulse part. 
- Select Arduino Nano 33 BLE Sense from Build Firmware.
- Select Quantized Version and click analyze. 
- Build your model.

It gives me arduino_motion-nano-33-ble-sense-v1.zip which includes flash.bat file. 
Reboot arduino and run flash.bat.
Lunch command prompt run $edge-impulse-run --> **This starts live classification.** 

But,  this is not what I want. I would like to download impulse library. 

    I click build again without selecting Arduino Nano 33 BLE Sense from Build Firmware, 
    it gives me ei-arduino-motion.zip this time. 

- Open Arduino IDE.
- Sketch --> include licbrary --> Add zip --> select arduino-motion.zip
- Tools --> board --> Mbed OS Nano Boards --> select Arduino Nan0 33 BLE
- File --> examples --> Arduino Motion Inferencing --> select Nano BLE 33 Sense Accelerometer
- Tools --> Port --> Select Arduino COM
- Click Upload  

I encountered to this error:

    Arduino_LSM9DS1.h: No such file or directory

Please check this website, I found it really heplpful: [https://www.programmingelectronics.com/no-such-file-error/](https://www.programmingelectronics.com/no-such-file-error/)

I installed  Arduino_LSM9DS1  from: 
    
    Open Arduino IDE: sketch --> include library --> manage libraries --> Arduino TensorflowLite. 

Upload completed with the errors below:

    `C:\Users\pelin\Documents\Arduino\libraries\arduino_motion_inferencing\src\edge-impulse-sdk\CMSIS\NN\Source\ConvolutionFunctions\arm_convolve_HWC_q7_RGB.c: In function 'arm_convolve_HWC_q7_RGB':
    C:\Users\pelin\Documents\Arduino\libraries\arduino_motion_inferencing\src\edge-impulse-sdk\CMSIS\NN\Source\ConvolutionFunctions\arm_convolve_HWC_q7_RGB.c:125:25: warning: dereferencing type-punned pointer will break strict-aliasing rules [-Wstrict-aliasing]
                             *__SIMD32(pBuffer) = 0x0;
                             ^
    C:\Users\pelin\Documents\Arduino\libraries\arduino_motion_inferencing\src\edge-impulse-sdk\CMSIS\NN\Source\ConvolutionFunctions\arm_convolve_HWC_q7_RGB.c:158:25: warning: dereferencing type-punned pointer will break strict-aliasing rules [-Wstrict-aliasing]
                             *__SIMD32(pBuffer) = __PKHBT(bottom.word, top.word, 0);
                             ^
    C:\Users\pelin\Documents\Arduino\libraries\arduino_motion_inferencing\src\edge-impulse-sdk\CMSIS\NN\Source\NNSupportFunctions\arm_nn_mult_q15.c: In function 'arm_nn_mult_q15':
    C:\Users\pelin\Documents\Arduino\libraries\arduino_motion_inferencing\src\edge-impulse-sdk\CMSIS\NN\Source\NNSupportFunctions\arm_nn_mult_q15.c:98:9: warning: dereferencing type-punned pointer will break strict-aliasing rules [-Wstrict-aliasing]
             *__SIMD32(pDst)++ = __PKHBT(out2, out1, 16);
             ^
    C:\Users\pelin\Documents\Arduino\libraries\arduino_motion_inferencing\src\edge-impulse-sdk\CMSIS\NN\Source\NNSupportFunctions\arm_nn_mult_q15.c:99:9: warning: dereferencing type-punned pointer will break strict-aliasing rules [-Wstrict-aliasing]
             *__SIMD32(pDst)++ = __PKHBT(out4, out3, 16);
             ^
    C:\Users\pelin\Documents\Arduino\libraries\arduino_motion_inferencing\src\edge-impulse-sdk\CMSIS\NN\Source\NNSupportFunctions\arm_nn_mult_q7.c: In function 'arm_nn_mult_q7':
    C:\Users\pelin\Documents\Arduino\libraries\arduino_motion_inferencing\src\edge-impulse-sdk\CMSIS\NN\Source\NNSupportFunctions\arm_nn_mult_q7.c:80:9: warning: dereferencing type-punned pointer will break strict-aliasing rules [-Wstrict-aliasing]
             *__SIMD32(pDst)++ = __PACKq7(out1, out2, out3, out4);
             ^
    C:\Users\pelin\Documents\Arduino\libraries\arduino_motion_inferencing\src\edge-impulse-sdk\CMSIS\NN\Source\NNSupportFunctions\arm_q7_to_q15_reordered_no_shift.c: In function 'arm_q7_to_q15_reordered_no_shift':
    C:\Users\pelin\Documents\Arduino\libraries\arduino_motion_inferencing\src\edge-impulse-sdk\CMSIS\NN\Source\NNSupportFunctions\arm_q7_to_q15_reordered_no_shift.c:106:9: warning: dereferencing type-punned pointer will break strict-aliasing rules [-Wstrict-aliasing]
             *__SIMD32(pDst)++ = in2;
             ^
    C:\Users\pelin\Documents\Arduino\libraries\arduino_motion_inferencing\src\edge-impulse-sdk\CMSIS\NN\Source\NNSupportFunctions\arm_q7_to_q15_reordered_no_shift.c:107:9: warning: dereferencing type-punned pointer will break strict-aliasing rules [-Wstrict-aliasing]
             *__SIMD32(pDst)++ = in1;
             ^
    C:\Users\pelin\Documents\Arduino\libraries\arduino_motion_inferencing\src\edge-impulse-sdk\CMSIS\NN\Source\PoolingFunctions\arm_pool_q7_HWC.c: In function 'compare_and_replace_if_larger_q7':
    C:\Users\pelin\Documents\Arduino\libraries\arduino_motion_inferencing\src\edge-impulse-sdk\CMSIS\NN\Source\PoolingFunctions\arm_pool_q7_HWC.c:78:9: warning: dereferencing type-punned pointer will break strict-aliasing rules [-Wstrict-aliasing]
             *__SIMD32(pIn)++ = in.word;
             ^
    C:\Users\pelin\Documents\Arduino\libraries\arduino_motion_inferencing\src\edge-impulse-sdk\CMSIS\NN\Source\PoolingFunctions\arm_pool_q7_HWC.c: In function 'accumulate_q7_to_q15':
    C:\Users\pelin\Documents\Arduino\libraries\arduino_motion_inferencing\src\edge-impulse-sdk\CMSIS\NN\Source\PoolingFunctions\arm_pool_q7_HWC.c:122:9: warning: dereferencing type-punned pointer will break strict-aliasing rules [-Wstrict-aliasing]
             *__SIMD32(pCnt)++ = __QADD16(vo1, in);
             ^
    C:\Users\pelin\Documents\Arduino\libraries\arduino_motion_inferencing\src\edge-impulse-sdk\CMSIS\NN\Source\PoolingFunctions\arm_pool_q7_HWC.c:125:9: warning: dereferencing type-punned pointer will break strict-aliasing rules [-Wstrict-aliasing]
             *__SIMD32(pCnt)++ = __QADD16(vo2, in);
             ^
    C:\Users\pelin\Documents\Arduino\libraries\arduino_motion_inferencing\src\edge-impulse-sdk\dsp\image\processing.cpp: In function 'int ei::image::processing::yuv422_to_rgb888(unsigned char*, const unsigned char*, unsigned int, ei::image::processing::YUV_OPTIONS)':
    C:\Users\pelin\Documents\Arduino\libraries\arduino_motion_inferencing\src\edge-impulse-sdk\dsp\image\processing.cpp:73:32: warning: comparison between signed and unsigned integer expressions [-Wsign-compare]
         for (unsigned int i = 0; i < in_size_pixels; ++i) {
                                  ~~^~~~~~~~~~~~~~~~
    C:\Users\pelin\Documents\Arduino\libraries\arduino_motion_inferencing\src\edge-impulse-sdk\tensorflow\lite\core\api\op_resolver.cpp: In function 'TfLiteStatus tflite::GetRegistrationFromOpCode(const tflite::OperatorCode*, const tflite::OpResolver&, tflite::ErrorReporter*, const TfLiteRegistration**)':
    C:\Users\pelin\Documents\Arduino\libraries\arduino_motion_inferencing\src\edge-impulse-sdk\tensorflow\lite\core\api\op_resolver.cpp:34:20: warning: comparison is always false due to limited range of data type [-Wtype-limits]
           builtin_code < BuiltinOperator_MIN) {
           ~~~~~~~~~~~~~^~~~~~~~~~~~~~~~~~~~~
    
    Sketch uses 153392 bytes (15%) of program storage space. Maximum is 983040 bytes.
    Global variables use 48248 bytes (18%) of dynamic memory, leaving 213896 bytes for local variables. Maximum is 262144 bytes.
    Device       : nRF52840-QIAA
    Version      : Arduino Bootloader (SAM-BA extended) 2.0 [Arduino:IKXYZ]
    Address      : 0x0
    Pages        : 256
    Page Size    : 4096 bytes
    Total Size   : 1024KB
    Planes       : 1
    Lock Regions : 0
    Locked       : none
    Security     : false
    Erase flash
    
    Done in 0.000 seconds
    Write 153400 bytes to flash (38 pages)
    [==============================] 100% (38/38 pages)
    Done in 6.438 seconds`
`

Open Serial Monitor for Live Classification. 
Despite the errors, live classification is working well:)

    Starting inferencing in 2 seconds...
    Sampling...
    Predictions (DSP: 21 ms., Classification: 0 ms., Anomaly: 0 ms.): 
        circle: 0.00000
        idle: 0.03516
        left-right: 0.00000
        up-down: 0.96484
    
    Starting inferencing in 2 seconds...
    Sampling...
    Predictions (DSP: 20 ms., Classification: 0 ms., Anomaly: 0 ms.): 
        circle: 0.91406
        idle: 0.00000
        left-right: 0.08594
        up-down: 0.00000
    
    Starting inferencing in 2 seconds...
    Sampling...
    Predictions (DSP: 20 ms., Classification: 0 ms., Anomaly: 0 ms.): 
        circle: 0.00000
        idle: 0.99219
        left-right: 0.00781
        up-down: 0.00000

Let's open the metadata:
    
    C:\Users\pelin\Documents\Arduino\libraries -->  arduino_motion_inferencing --> src --> model_parameters

Open model_metadata.h.

Here is the error: 
  
    #error "Cannot use full TensorFlow Lite with EON"

I installed  Arduino TensorflowLite via: 

    Open Arduino IDE: sketch --> include library --> manage libraries --> Arduino TensorflowLite. 

Start upload again. Same old :(

    C:\Users\pelin\Documents\Arduino\libraries\arduino_motion_inferencing\src\edge-impulse-sdk\CMSIS\NN\Source\PoolingFunctions\arm_pool_q7_HWC.c:125:9: warning: dereferencing type-punned pointer will break strict-aliasing rules [-Wstrict-aliasing]
             *__SIMD32(pCnt)++ = __QADD16(vo2, in);
             ^
    C:\Users\pelin\Documents\Arduino\libraries\arduino_motion_inferencing\src\edge-impulse-sdk\dsp\image\processing.cpp: In function 'int ei::image::processing::yuv422_to_rgb888(unsigned char*, const unsigned char*, unsigned int, ei::image::processing::YUV_OPTIONS)':
    C:\Users\pelin\Documents\Arduino\libraries\arduino_motion_inferencing\src\edge-impulse-sdk\dsp\image\processing.cpp:73:32: warning: comparison between signed and unsigned integer expressions [-Wsign-compare]
         for (unsigned int i = 0; i < in_size_pixels; ++i) {
                                  ~~^~~~~~~~~~~~~~~~
    C:\Users\pelin\Documents\Arduino\libraries\arduino_motion_inferencing\src\edge-impulse-sdk\tensorflow\lite\core\api\op_resolver.cpp: In function 'TfLiteStatus tflite::GetRegistrationFromOpCode(const tflite::OperatorCode*, const tflite::OpResolver&, tflite::ErrorReporter*, const TfLiteRegistration**)':
    C:\Users\pelin\Documents\Arduino\libraries\arduino_motion_inferencing\src\edge-impulse-sdk\tensorflow\lite\core\api\op_resolver.cpp:34:20: warning: comparison is always false due to limited range of data type [-Wtype-limits]
           builtin_code < BuiltinOperator_MIN) {
           ~~~~~~~~~~~~~^~~~~~~~~~~~~~~~~~~~~


Yet, when I open:

    File -> examples -> arduino_motion_inferencing -> arduino nano ble33 sense accelerometer contionuous

Upload and open serial monitor: 

    Predictions (DSP: 28 ms., Classification: 0 ms., Anomaly: 0 ms.): idle  [ 0, 10, 0, 0, 0, 0, ]
    Predictions (DSP: 28 ms., Classification: 1 ms., Anomaly: 0 ms.): idle  [ 0, 10, 0, 0, 0, 0, ]
    Predictions (DSP: 28 ms., Classification: 0 ms., Anomaly: 0 ms.): idle  [ 0, 10, 0, 0, 0, 0, ]
    Predictions (DSP: 28 ms., Classification: 0 ms., Anomaly: 0 ms.): idle  [ 0, 10, 0, 0, 0, 0, ]
    Predictions (DSP: 28 ms., Classification: 1 ms., Anomaly: 0 ms.): idle  [ 0, 10, 0, 0, 0, 0, ]
    Predictions (DSP: 28 ms., Classification: 1 ms., Anomaly: 0 ms.): idle  [ 0, 10, 0, 0, 0, 0, ]
    Predictions (DSP: 28 ms., Classification: 1 ms., Anomaly: 0 ms.): idle  [ 0, 10, 0, 0, 0, 0, ]
    Predictions (DSP: 28 ms., Classification: 1 ms., Anomaly: 0 ms.): idle  [ 0, 10, 0, 0, 0, 0, ]
    Predictions (DSP: 28 ms., Classification: 0 ms., Anomaly: 0 ms.): uncertain  [ 3, 0, 4, 0, 3, 0, ]
    Predictions (DSP: 26 ms., Classification: 0 ms., Anomaly: 0 ms.): uncertain  [ 3, 0, 4, 0, 3, 0, ]
    Predictions (DSP: 26 ms., Classification: 1 ms., Anomaly: 0 ms.): uncertain  [ 4, 0, 4, 0, 2, 0, ]
    Predictions (DSP: 28 ms., Classification: 0 ms., Anomaly: 0 ms.): uncertain  [ 5, 0, 4, 0, 1, 0, ]
    Predictions (DSP: 28 ms., Classification: 1 ms., Anomaly: 0 ms.): uncertain  [ 6, 0, 3, 0, 1, 0, ]
    ....
    Predictions (DSP: 28 ms., Classification: 1 ms., Anomaly: 0 ms.): up-down  [1, 0, 1, 8, 0, 0, ]

No errors!

First 4 numbers in the list represents:
- 1: circle
- 2: idle 
- 3: left_right
- 4: up_down

## Key Words
Tiny ML, Arduino, Edge Impulse, Deployment



