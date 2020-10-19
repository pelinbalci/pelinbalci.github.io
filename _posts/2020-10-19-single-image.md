
# Single Image

In this notebook, I will explain how to load an image with PIL and explain some operations with PyTorch and Numpy. These processes are part of Style Transfer in Convolutional Neural Networks, there are two images: content and style. The next post defines how to transfer the style of one image to the content of the other image.

This document is prepared by using Google Colab and the lecture notes from: https://classroom.udacity.com/courses/ud188

**First of all; make sure that you are in the right content in drive.**


```python
from google.colab import drive
drive.mount('/content/drive')
```

    Mounted at /content/drive


Use GPU if available


```python
# move the model to GPU, if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
```

Import libraries


```python
# import resources
%matplotlib inline

from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np

import torch
import requests
from torchvision import transforms, models
```

**Load Image**

The function below is useful for loading images. 
- img_path should be the path the image in your drive. 
- Since the large images slow down the process, max_size is defined as 400. 
- transforms from torchvision i used to crop, resize, normalize the image and we can turn it to tensor. 


Simply you can use following code: 
```
image = Image.open(img_path).convert('RGB')
```




```python
def load_image(img_path, max_size=400, shape=None):
    ''' Load in and transform an image, making sure the image
       is <= 400 pixels in the x-y dims.'''
    if "http" in img_path:
        response = requests.get(img_path)
        image = Image.open(BytesIO(response.content)).convert('RGB')
    else:
        image = Image.open(img_path).convert('RGB')
    
    # large images will slow down processing
    if max(image.size) > max_size:
        size = max_size
    else:
        size = max(image.size)
    
    if shape is not None:
        size = shape
        
    in_transform = transforms.Compose([
                        transforms.Resize(size),
                        transforms.ToTensor(),
                        transforms.Normalize((0.485, 0.456, 0.406), 
                                             (0.229, 0.224, 0.225))])

    # discard the transparent, alpha channel (that's the :3) and add the batch dimension
    image = in_transform(image)[:3,:,:].unsqueeze(0)
    
    return image
```

Load images by file name


```python
content = load_image('/content/drive/My Drive/Style_Transfer/images/octopus.jpg').to(device)
style = load_image('/content/drive/My Drive/Style_Transfer/images/hockney.jpg').to(device)

print(content.shape)
print(style.shape)
```

    torch.Size([1, 3, 400, 592])
    torch.Size([1, 3, 360, 263])


What does it look like? 


```python
content[0][0]
```




    tensor([[-1.8953, -1.9467, -1.9295,  ..., -0.1999, -0.1999, -0.3027],
            [-1.9980, -2.0152, -1.9467,  ..., -0.4568, -0.3369, -0.1657],
            [-1.9809, -1.9809, -1.9295,  ..., -0.8164, -0.5596, -0.3027],
            ...,
            [-1.9809, -1.9809, -1.9809,  ..., -1.0904, -1.1075, -1.1589],
            [-1.9809, -1.9809, -1.9809,  ..., -1.0733, -1.1418, -1.2103],
            [-1.9638, -1.9638, -1.9638,  ..., -1.0562, -1.1760, -1.2445]])



**Change the shape**

The shape of two images are different, we can force the style image to be the same size as the content image. 


```python
content.shape[-2:]
```




    torch.Size([400, 592])




```python
style = load_image('/content/drive/My Drive/Style_Transfer/images/hockney.jpg', 
                   shape=content.shape[-2:]).to(device)
print(style.shape)
```

    torch.Size([1, 3, 400, 592])


**Display the image**


```python
# helper function for un-normalizing an image 
# and converting it from a Tensor image to a NumPy image for display
def im_convert(tensor):
    """ Display a tensor as an image. """
    
    image = tensor.to("cpu").clone().detach()
    image = image.numpy().squeeze()
    image = image.transpose(1,2,0)
    image = image * np.array((0.229, 0.224, 0.225)) + np.array((0.485, 0.456, 0.406))
    image = image.clip(0, 1)

    return image
```


```python
# display the images
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
# content and style ims side-by-side
ax1.imshow(im_convert(content))
ax2.imshow(im_convert(style))
```




    <matplotlib.image.AxesImage at 0x7ff3dcbcafd0>




![png](output_18_1.png)


**See the explanation for each step of the function:**

**Copy content image & detach**

Ref: https://stackoverflow.com/questions/63582590/why-do-we-call-detach-before-calling-numpy-on-a-pytorch-tensor

torch.tensors are designed to be used in the context of gradient descent optimization, and therefore they hold not only a tensor with numeric values, but (and more importantly) the computational graph leading to these values. This computational graph is then used (using the chain rule of derivatives) to compute the derivative of the loss function w.r.t each of the independent variables used to compute the loss.

As mentioned before, np.ndarray object does not have this extra "computational graph" layer and therefore, when converting a torch.tensor to np.ndarray you must explicitly remove the computational graph of the tensor using the detach() command.


```python
image = content.to("cpu").clone().detach()
print(image.shape)
print(image.type)
```

    torch.Size([1, 3, 400, 592])
    <built-in method type of Tensor object at 0x7ff3dcba6e10>


**Turn to numpy**


```python
image = image.numpy()
print(image.shape)
print(image.dtype)
```

    (1, 3, 400, 592)
    float32


**Use squeeze**

numpy.squeeze() : Remove single-dimensional entries from the shape of an array.


```python
image = image.squeeze()
print(image.shape)
```

    (3, 400, 592)


**Transpose**

Transpose the dimension such that: Height, Width, Channel
- Original: 3, 400, 592
- Transpose(1,2,0) --> 400, 592, 3 


```python
image = image.transpose(1,2,0)
image.shape
```




    (400, 592, 3)



**Normalize**

Ref: https://pytorch.org/docs/stable/torchvision/models.html

All pre-trained models expect input images normalized in the same way, i.e. mini-batches of 3-channel RGB images of shape (3 x H x W), where H and W are expected to be at least 224. The images have to be loaded in to a range of [0, 1] and then normalized using mean = [0.485, 0.456, 0.406] and std = [0.229, 0.224, 0.225]. 

You can use the following transform to normalize:

        normalize = transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225])   


```python
image = image * np.array((0.229, 0.224, 0.225)) + np.array((0.485, 0.456, 0.406))
image.shape
```




    (400, 592, 3)



**Clip the values**

Ref: https://numpy.org/doc/stable/reference/generated/numpy.clip.html

Given an interval, values outside the interval are clipped to the interval edges. For example, if an interval of [0, 1] is specified, values smaller than 0 become 0, and values larger than 1 become 1.



```python
image = image.clip(0, 1)
image
```




    array([[[0.05098039, 0.0509804 , 0.05882353],
            [0.03921567, 0.03921569, 0.04705882],
            [0.04313724, 0.04313725, 0.0509804 ],
            ...,
            [0.43921568, 0.43921569, 0.40000002],
            [0.43921568, 0.43921569, 0.40000002],
            [0.41568626, 0.41568628, 0.37647061]],
    
           [[0.02745098, 0.02745099, 0.03529412],
            [0.02352938, 0.02352943, 0.03137254],
            [0.03921567, 0.03921569, 0.04313725],
            ...,
            [0.38039215, 0.37254903, 0.33725492],
            [0.40784313, 0.40392158, 0.3647059 ],
            [0.44705881, 0.43921569, 0.40392159]],
    
           [[0.03137252, 0.03137255, 0.03529412],
            [0.03137252, 0.03137255, 0.03529412],
            [0.04313724, 0.04313725, 0.04313725],
            ...,
            [0.29803922, 0.28627453, 0.25098042],
            [0.35686274, 0.34509805, 0.30980394],
            [0.41568626, 0.40392158, 0.36862747]],
    
           ...,
    
           [[0.03137252, 0.02352943, 0.02745099],
            [0.03137252, 0.02352943, 0.02745099],
            [0.03137252, 0.02352943, 0.02745099],
            ...,
            [0.23529412, 0.21568628, 0.14117649],
            [0.23137252, 0.21176472, 0.13333336],
            [0.21960783, 0.20000002, 0.12156863]],
    
           [[0.03137252, 0.02352943, 0.02745099],
            [0.03137252, 0.02352943, 0.02745099],
            [0.03137252, 0.02352943, 0.02745099],
            ...,
            [0.23921566, 0.21960786, 0.14117649],
            [0.2235294 , 0.2039216 , 0.12549024],
            [0.20784311, 0.18823531, 0.10980393]],
    
           [[0.0352941 , 0.02745099, 0.03137254],
            [0.0352941 , 0.02745099, 0.03137254],
            [0.0352941 , 0.02745099, 0.03137254],
            ...,
            [0.24313724, 0.22352942, 0.14509807],
            [0.21568625, 0.19607846, 0.11764705],
            [0.19999996, 0.1803922 , 0.10196077]]])



Use matplotlib imshow to show the image


```python
plt.imshow(image)
```




    <matplotlib.image.AxesImage at 0x7ff3dae27cc0>




![png](output_33_1.png)


**Summary:**

- Load the image by using PIL
- Turn it to Tensor
- Change the shape
- Visualize the image
    - Why are we using constant terms when we normalize the image?
    - What is squeeze?
    - Transpose the 3 dimensional numpy array.
    - How can we use clip?
