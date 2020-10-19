---
layout: post
title:  "Style Transfer"
date:   2020-10-19
categories: General
---

```python
from google.colab import drive
drive.mount('/content/drive')
```

    Drive already mounted at /content/drive; to attempt to forcibly remount, call drive.mount("/content/drive", force_remount=True).



```python
import os
os.chdir("/content/drive/My Drive/Style_Transfer/notebook_ims")
!ls
```

    style_tx_cat.png  vgg19_convlayers.png



```python
# import resources
%matplotlib inline

from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np

import torch
import torch.optim as optim
import requests
from torchvision import transforms, models
```

Load VGG features, not classification part


```python
# get the "features" portion of VGG19 (we will not need the "classifier" portion)
# all convolutional and pooling layers are in features 
vgg = models.vgg19(pretrained=True).features

# freeze all VGG parameters since we're only optimizing the target image
for param in vgg.parameters():
    param.requires_grad_(False)
```

    Downloading: "https://download.pytorch.org/models/vgg19-dcbb9e9d.pth" to /root/.cache/torch/hub/checkpoints/vgg19-dcbb9e9d.pth



    HBox(children=(FloatProgress(value=0.0, max=574673361.0), HTML(value='')))


    



```python
# move the model to GPU, if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
vgg.to(device)

'''
(0) -> conv1_1
(1) -> conv1_2 (second in the first stack)
Max Pooling Layer
(5) -> conv2_1 (first in second stack)

'''
```




    '\n(0) -> conv1_1\n(1) -> conv1_2 (second in the first stack)\nMax Pooling Layer\n(5) -> conv2_1 (first in second stack)\n\n'



Load in Content and Style Images


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

Load images by file name and forcing the style image to be the same size as the content image.


```python
# load in content and style image
content = load_image('/content/drive/My Drive/Style_Transfer/images/octopus.jpg').to(device)
#content = load_image('/content/drive/My Drive/Style_Transfer/images/mother.jpeg').to(device)
# Resize style to match content, makes code easier
style = load_image('/content/drive/My Drive/Style_Transfer/images/hockney.jpg', 
                   shape=content.shape[-2:]).to(device)

content.shape
```




    torch.Size([1, 3, 400, 592])




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




    <matplotlib.image.AxesImage at 0x7fa1d6a85588>




![png](output_11_1.png)


Content and Style Features

TODO: complete the mapping of layer names to the names found in the paper for the _content representation_ and the _style representation_.


```python
def get_features(image, model, layers=None):
    """ Run an image forward through a model and get the features for 
        a set of layers. Default layers are for VGGNet matching Gatys et al (2016)
    """
    
    ## TODO: Complete mapping layer names of PyTorch's VGGNet to names from the paper
    ## Need the layers for the content and style representations of an image
    if layers is None:
        layers = {'0': 'conv1_1',
                  '5': 'conv2_1', 
                  '10': 'conv3_1',   
                  '19': 'conv4_1',
                  '21': 'conv4_2', # content representation
                  '28': 'conv5_1', 
                  }
        
        
    ## -- do not need to change the code below this line -- ##
    features = {}
    x = image
    # model._modules is a dictionary holding each module in the model
    for name, layer in model._modules.items():
        x = layer(x)
        if name in layers:
            features[layers[name]] = x
            
    return features
```

Gram Matrix :Complete the gram matrix


```python
def gram_matrix(tensor):
    """ Calculate the Gram Matrix of a given tensor 
        Gram Matrix: https://en.wikipedia.org/wiki/Gramian_matrix
    """
    
    ## get the batch_size, depth, height, and width of the Tensor
    ## reshape it, so we're multiplying the features for each channel
    ## calculate the gram matrix

    # My solution
    #tensor_reshaped = tensor.flatten(start_dim=0, end_dim=1)
    #tensor_reshaped = tensor_reshaped.flatten(start_dim=1, end_dim=2)
    #tensor_transposed = torch.transpose(tensor_reshaped, 0, 1)

    #gram = torch.matmul(tensor_reshaped, tensor_transposed)
    
    # get the batch_size, depth, height, and width of the Tensor
    _, d, h, w = tensor.size()
    
    # reshape so we're multiplying the features for each channel
    tensor = tensor.view(d, h * w)
    
    # calculate the gram matrix
    gram = torch.mm(tensor, tensor.t())

    return gram 
```

- extracting features
- computing the gram matrix of a given convolutional layer


```python
# get content and style features only once before forming the target image
content_features = get_features(content, vgg)
style_features = get_features(style, vgg)

# calculate the gram matrices for each layer of our style representation
style_grams = {layer: gram_matrix(style_features[layer]) for layer in style_features}

# create a third "target" image and prep it for change
# it is a good idea to start off with the target as a copy of our *content* image
# then iteratively change its style
target = content.clone().requires_grad_(True).to(device)
```


```python
for key, values in content_features.items():
  print(key)

print(content_features['conv1_1'].shape)

# stayle feature is the same 
```

    conv1_1
    conv2_1
    conv3_1
    conv4_1
    conv4_2
    conv5_1
    torch.Size([1, 64, 400, 592])


Weights


```python
# weights for each style layer 
# weighting earlier layers more will result in *larger* style artifacts
# notice we are excluding `conv4_2` our content representation 

style_weights = {'conv1_1': 1.,
                 'conv2_1': 0.75,
                 'conv3_1': 0.2,
                 'conv4_1': 0.2,
                 'conv5_1': 0.2}

# you may choose to leave these as is
content_weight = 1  # alpha
style_weight = 1e6  # beta, set the style_weight to achieve the ratio you want.
```

Loss & Optimization 


```python
# for displaying the target image, intermittently
show_every = 400

# iteration hyperparameters
optimizer = optim.Adam([target], lr=0.003)
steps = 2000  # decide how many iterations to update your image (5000)

for ii in range(1, steps+1):
    
    # get the features from your target image
    target_features = get_features(target, vgg)
    
    # the content loss
    content_loss = torch.mean((target_features['conv4_2'] - content_features['conv4_2'])**2)
    
    # the style loss
    # initialize the style loss to 0
    style_loss = 0
    # then add to it for each layer's gram matrix loss
    for layer in style_weights:
        # get the "target" style representation for the layer
        target_feature = target_features[layer]
        target_gram = gram_matrix(target_feature)
        _, d, h, w = target_feature.shape
        # get the "style" style representation
        style_gram = style_grams[layer]
        # the style loss for one layer, weighted appropriately
        layer_style_loss = style_weights[layer] * torch.mean((target_gram - style_gram)**2)
        # add to the style loss
        style_loss += layer_style_loss / (d * h * w)
        
    # calculate the *total* loss
    total_loss = content_weight * content_loss + style_weight * style_loss
    
    # update your target image
    optimizer.zero_grad()
    total_loss.backward()
    optimizer.step()
    
    # display intermediate images and print the loss
    if  ii % show_every == 0:
        print('Total loss: ', total_loss.item())
        plt.imshow(im_convert(target))
        plt.show()
```

    Total loss:  46602708.0



![png](output_22_1.png)


    Total loss:  9589644.0



![png](output_22_3.png)


    Total loss:  5005656.5



![png](output_22_5.png)


    Total loss:  3033171.25



![png](output_22_7.png)


    Total loss:  1945939.25



![png](output_22_9.png)


## Display the Target Image


```python
# display content and final, target image
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(20, 10))
ax1.imshow(im_convert(content))
ax2.imshow(im_convert(target))
```




    <matplotlib.image.AxesImage at 0x7fa1d627def0>




![png](output_24_1.png)


# Detailed Explanation

### Style Transfer with Deep Neural Networks


Reference: [Image Style Transfer Using Convolutional Neural Networks, by Gatys](https://www.cv-foundation.org/openaccess/content_cvpr_2016/papers/Gatys_Image_Style_Transfer_CVPR_2016_paper.pdf) in PyTorch.

Use the features found in the 19-layer VGG Network.
- Conv_1_1 is the first convolutional layer that an image is passed through, in the first stack. 
- Conv_2_1 is the first convolutional layer in the *second* stack. - The deepest convolutional layer in the network is conv_5_4.


### Separating Style and Content

* objects and their arrangement are similar to that of the **content image**
* style, colors, and textures are similar to that of the **style image**

### Load in VGG19 (features)

VGG19 is split into two portions:
* `vgg19.features`, which are all the convolutional and pooling layers
* `vgg19.classifier`, which are the three linear, classifier layers at the end

We only need the `features` portion, which we're going to load in and "freeze" the weights of, below.

### Load in Content and Style Images

The `load_image` function also converts images to normalized Tensors.

Additionally, it will be easier to have smaller images and to squish the content and style images so that they are of the same size.

### VGG19 Layers

To get the content and style representations of an image, we have to pass an image forward through the VGG19 network until we get to the desired layer(s) and then get the output from that layer.

all_layers = {'0': 'conv1_1', 
              '1': 'conv1_2', 
              '5': 'conv2_1', 
              '7': 'conv2_2', 
              '10': 'conv3_1', 
              '12': 'conv3_2',
              '14': 'conv3_3',
              '16': 'conv3_4',
              '19': 'conv4_1',
              '21': 'conv4_2',
              '23': 'conv4_3',
              '25': 'conv4_4',
              '28': 'conv5_1',
              '30': 'conv5_2',
              '32': 'conv5_3',
              '34': 'conv5_4',
                  }

### Gram Matrix 

The output of every convolutional layer is a Tensor with dimensions associated with the `batch_size`, a depth, `d` and some height and width (`h`, `w`). The Gram matrix of a convolutional layer can be calculated as follows:
* Get the depth, height, and width of a tensor using `batch_size, d, h, w = tensor.size()`
* Reshape that tensor so that the spatial dimensions are flattened
* Calculate the gram matrix by multiplying the reshaped tensor by it's transpose 

*Note: You can multiply two matrices using `torch.mm(matrix1, matrix2)`.*


```python
# How to reshape? 

# Reshape: https://stackoverflow.com/questions/55546873/how-do-i-flatten-a-tensor-in-pytorch

import torch
input = torch.rand(3, 8, 8)
print(input.shape) # torch.Size([3, 8, 8])
print(input.flatten(start_dim=1, end_dim=2).shape) # torch.Size([3, 64])
reshape_input  = input.flatten(start_dim=1, end_dim=2)
reshape_input.shape # torch.Size([3, 64])

transposed = torch.transpose(reshape_input, 0, 1)
transposed.shape # torch.Size([64, 3])
```

    torch.Size([3, 8, 8])
    torch.Size([3, 64])





    torch.Size([64, 3])



### Putting it all Together

Now that we've written functions for extracting features and computing the gram matrix of a given convolutional layer; let's put all these pieces together! We'll extract our features from our images and calculate the gram matrices for each layer in our style representation.

### Loss and Weights

#### Individual Layer Style Weights

Below, you are given the option to weight the style representation at each relevant layer. It's suggested that you use a range between 0-1 to weight these layers. By weighting earlier layers (`conv1_1` and `conv2_1`) more, you can expect to get _larger_ style artifacts in your resulting, target image. Should you choose to weight later layers, you'll get more emphasis on smaller features. This is because each layer is a different size and together they create a multi-scale style representation!

#### Content and Style Weight

Just like in the paper, we define an alpha (`content_weight`) and a beta (`style_weight`). This ratio will affect how _stylized_ your final image is. It's recommended that you leave the content_weight = 1 and set the style_weight to achieve the ratio you want.

## Updating the Target & Calculating Losses

You'll decide on a number of steps for which to update your image, this is similar to the training loop that you've seen before, only we are changing our _target_ image and nothing else about VGG19 or any other image. Therefore, the number of steps is really up to you to set! **I recommend using at least 2000 steps for good results.** But, you may want to start out with fewer steps if you are just testing out different weight values or experimenting with different images.

Inside the iteration loop, you'll calculate the content and style losses and update your target image, accordingly.

#### Content Loss

The content loss will be the mean squared difference between the target and content features at layer `conv4_2`. This can be calculated as follows: 
```
content_loss = torch.mean((target_features['conv4_2'] - content_features['conv4_2'])**2)
```

#### Style Loss

The style loss is calculated in a similar way, only you have to iterate through a number of layers, specified by name in our dictionary `style_weights`. 
> You'll calculate the gram matrix for the target image, `target_gram` and style image `style_gram` at each of these layers and compare those gram matrices, calculating the `layer_style_loss`. 
> Later, you'll see that this value is normalized by the size of the layer.

#### Total Loss

Finally, you'll create the total loss by adding up the style and content losses and weighting them with your specified alpha and beta!

Intermittently, we'll print out this loss; don't be alarmed if the loss is very large. It takes some time for an image's style to change and you should focus on the appearance of your target image rather than any loss value. Still, you should see that this loss decreases over some number of iterations.

TODO: Define content, style, and total losses.
