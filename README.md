# Learning - Nim 
The AI learns to play [Nim](https://en.wikipedia.org/wiki/Nim) through model-free reinforcement learning, using Q-learning and epsilon-greedy action selection during training. The Q-learning formula is defined as:
> <img src="https://render.githubusercontent.com/render/math?math=\LARGE%20Q(s,a)%20\leftarrow%20Q(s,a)%20%2B%20\alpha(newEstimate%20-%20oldEstimate)"> <br>
> where learning rate $\alpha$=0.5, $\epsilon$=0.1, number of games n=10000 

# Running
python play.py 

# Demonstration
https://youtu.be/azi3Ndhd668
