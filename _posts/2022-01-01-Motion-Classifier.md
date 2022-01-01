---
layout: post
title: "Motion Classifier with Edge Impulse"
categories: tinyml
---
Hello!

Happy new year everyone:) On the very first day of the year, I completed a motion classifier project with edge impulse & Arduino. I would like to tell you the steps of the project, some problems I've faced with and how to solve them.


### 1. Connection

After creating a new project on edge impulse, I plugged in my Arduino board to my laptop, 
then **update the firmware** ---> this is very important do not skip this step. 

Then I open the command prompt and write:

    edge-impulse-daemon --clean

I can connect my Arduino board with my new project in edge impulse. Go back to your project on the edge impulse website 
and check if the Arduino is connected. If you encountered with a problem, you can read my previous [post](https://pelinbalci.com/tinyml/2021/11/22/Arduino-Edge-Impulse.html)

### 2. Collect Data

This is the funny part. You need to choose an item in your home that you can collect motion data. 
I wish to have a remote-controlled car :( Anyway, I decided to use my hairdryer and taped the board to the hairdryer 
as you can see below.

<div class="fig figcenter fighighlight">
  <img src="/assets/tinyml_images/hairdryer.jpeg" width="90%">
  <div class="figcaption">Setup </div>
</div>

Select Data- Acquisition, write the label name, and start sampling! There are 4 classes in my project, off, light, light_move, and heavy.

    off: not working
    light: working in mode 1
    light_move: working in mode 1 and waving
    heavy: working in mode 2

Here is a short video of the collecting data process:

<div class="fig figcenter fighighlight">
  <img src="/assets/tinyml_images/datacollect.mp4" width="90%">
  <div class="figcaption">Setup </div>
</div>

I've collected 8 minutes of data (2 minutes for each class) and 2 minutes for test data.

### 3. Train & Test Model

Impulse design is really easy thanks to edge impulse. First, you need to create impulse. 
You will select processing block and learning block. The processing block will help you to generate 
features, and the learning block is actually your model.

<div class="fig figcenter fighighlight">
  <img src="/assets/tinyml_images/impulse_design.PNG" width="90%">
  <div class="figcaption">Impulse Design </div>
</div>


You can check my previous post about [Fourier Transform](https://pelinbalci.com/2021/12/19/Fast-Fourier-Tranform.html), 
It is used for generating features, fortunately, the edge impulse handles the Fouirer Transform for us.

After feature generation, I desging a neural network with 2 hidden layers and dropout layer with probability of 0.2 

    import tensorflow as tf
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense, InputLayer, Dropout, Conv1D, Conv2D, Flatten, Reshape, MaxPooling1D, MaxPooling2D, BatchNormalization, TimeDistributed
    from tensorflow.keras.optimizers import Adam
    
    # model architecture
    model = Sequential()
    model.add(Dense(64, activation='relu',
        activity_regularizer=tf.keras.regularizers.l1(0.00001)))
    model.add(Dense(32, activation='relu',
        activity_regularizer=tf.keras.regularizers.l1(0.00001)))
    model.add(Dropout(0.2))
    model.add(Dense(classes, activation='softmax', name='y_pred'))
    
    # this controls the learning rate
    opt = Adam(lr=0.0005, beta_1=0.9, beta_2=0.999)
    # this controls the batch size, or you can manipulate the tf.data.Dataset objects yourself
    BATCH_SIZE = 32
    train_dataset = train_dataset.batch(BATCH_SIZE, drop_remainder=False)
    validation_dataset = validation_dataset.batch(BATCH_SIZE, drop_remainder=False)
    callbacks.append(BatchLoggerCallback(BATCH_SIZE, train_sample_count))
    
    # train the neural network
    model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])
    model.fit(train_dataset, epochs=30, validation_data=validation_dataset, verbose=2, callbacks=callbacks)

Here is the validation score:

<div class="fig figcenter fighighlight">
  <img src="/assets/tinyml_images/valid_acc.PNG" width="90%">
  <div class="figcaption">Validation Accuracy :) </div>
</div>


Then I choose model testing. The test score is 71.45%. I am happy with this result.

<div class="fig figcenter fighighlight">
  <img src="/assets/tinyml_images/test_acc.PNG" width="90%">
  <div class="figcaption">Test Accuracy :) </div>
</div>


### 4. Deployment
You can read my previous post about deployment. Click Deployment, select Arduino, and the quantized version of the project (Please read more about Tensorflow Lite). Click build --> this will give you a zip file.

Now please close the terminal if it still opens. (I got "port is busy" error during uploading before I close the terminal)

Open Arduino IDE.

- Sketch --> Include library --> Add Zip Library
- File --> Examples --> motion_classifier_inferencing --> nano_ble33_sense_accelerometer --> upload --> this will take around 10 minutes.

Then you can open Serial Monitor for live classification. Here is a short video for live classification. 
There are some errors between light and heavy but that's ok :)

<div class="fig figcenter fighighlight">
  <img src="/assets/tinyml_images/live_classification.PNG" width="90%">
  <div class="figcaption">Live Classification </div>
</div>


VIDEO