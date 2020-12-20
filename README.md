# Uncertainty - PageRank 
Estimating page importance using 2 calculation methods:
1. Sampling - random surfer model where:
> where number of samples n=10000 and damping factor d=0.85
2. Iteration - random surfer model where:<br>
> <img src="https://render.githubusercontent.com/render/math?math=PR(p)%20=%20\frac{1-d}{N}%20%2Bd\sum_i{\frac{PR(i)}{NumLinks(i)}}">
> with damping factor d = 0.85 and iteration terminates when each PR(p) changes no more than 0.001

# Corpora 
* corpus0 - 4 pages
* corpus1 - 7 pages
* corpus2 - 8 pages

# Running
python pagerank.py [corpus]

# Demonstration
https://youtu.be/a3GJ973ctQQ
