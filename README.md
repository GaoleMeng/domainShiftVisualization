# Domain Transition Detection

Detect and visulize the domain changes occur around SIGIR conference

## Algorithm Explaination

The final goal of this algorithm is to compute the 2D embedding of the papers points around SIGIR conference. To accomplish this, we first need to construct a reference graph <a href="https://www.codecogs.com/eqnedit.php?latex=\inline&space;G&space;=&space;(V,&space;E)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\inline&space;G&space;=&space;(V,&space;E)" title="G = (V, E)" /></a> and use largeVis to compute its embedding.

The current algorithm start with finding all the 


