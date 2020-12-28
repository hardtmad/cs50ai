# Neural Networks - Traffic 
Using TensorFlow's Convolutional Neural Network, traffic sign images are pre-processed and classified into 43 types of road sign. The model uses [ReLU activation](https://ml-cheatsheet.readthedocs.io/en/latest/activation_functions.html#relu), three [convolution layers](https://ml-cheatsheet.readthedocs.io/en/latest/layers.html#convolution) with 3x3 kernals, two [max-pooling layers](https://ml-cheatsheet.readthedocs.io/en/latest/layers.html#pooling) with 2x2 pool sizes, 30% [dropout](https://ml-cheatsheet.readthedocs.io/en/latest/layers.html#dropout) to avoid overfitting, and [softmax classification](https://ml-cheatsheet.readthedocs.io/en/latest/activation_functions.html?highlight=softmax#softmax) in the output layer. The model's performance is measured using [cross-entropy loss](https://ml-cheatsheet.readthedocs.io/en/latest/loss_functions.html#cross-entropy).
 
> Train size: 60% <br>
> Test size: 40% <br> 
> Epochs: 10 

> Model accuracy: ~96%

# Dataset
[German Traffic Sign Recognition Benchmark (GTSRB)](https://benchmark.ini.rub.de) -- over 25,000 images

# Installing requirements
`pip3 install -r requirements.txt`

# Running
`python traffic.py gtsrb`

# Demonstration
https://youtu.be/cfDAJVSXqi8
