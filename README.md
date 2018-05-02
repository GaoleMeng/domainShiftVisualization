# Domain Transition Detection

Detect and visulize the domain changes occur around SIGIR conference

## Algorithm Explaination

The final goal of this algorithm is to compute the 2D embedding of the papers points around SIGIR conference. To accomplish this, we need to construct a reference graph <a href="https://www.codecogs.com/eqnedit.php?latex=\inline&space;G&space;=&space;(V,&space;E)" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\inline&space;G&space;=&space;(V,&space;E)" title="G = (V, E)" /></a> and use largeVis to compute the graph embedding in two-dimensional space.

1. Treat each paper in [Aminer](https://aminer.org/open-academic-graph) as a point, two paper are connected with a directed edge if one cites another.

2. BFS the graph starting from all papers belong to SIGIR, which create a subset of all paper points. The set of paper nodes is denoted as <a href="https://www.codecogs.com/eqnedit.php?latex=\inline&space;V_{papers}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\inline&space;V_{papers}" title="V_{papers}" /></a>. We then construct all the conference that <a href="https://www.codecogs.com/eqnedit.php?latex=\inline&space;V_{papers}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\inline&space;V_{papers}" title="V_{papers}" /></a> has touched, which is to say <a href="https://www.codecogs.com/eqnedit.php?latex=\inline&space;S_{conf}&space;=&space;\{&space;conf|v\in&space;V_{paper}\&space;\wedge\&space;v\&space;belongs\&space;to\&space;conf\}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\inline&space;S_{conf}&space;=&space;\{&space;conf|v\in&space;V_{paper}\&space;\wedge\&space;v\&space;belongs\&space;to\&space;conf\}" title="S_{conf} = \{ conf|v\in V_{paper}\ \wedge\ v\ belongs\ to\ conf\}" /></a>.

3. Since that this may introduce too much possible conferences around SIGIR, like if only one paper in <a href="https://www.codecogs.com/eqnedit.php?latex=\inline&space;V_{papers}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\inline&space;V_{papers}" title="V_{papers}" /></a> belongs Nature, we still need to include Nature in <a href="https://www.codecogs.com/eqnedit.php?latex=\inline&space;S_{conf}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\inline&space;S_{conf}" title="S_{conf}" /></a>. So we need to continue on filtering out more conferences in <a href="https://www.codecogs.com/eqnedit.php?latex=\inline&space;S_{conf}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\inline&space;S_{conf}" title="S_{conf}" /></a> by introducing an important score of each conference. The score of conference <a href="https://www.codecogs.com/eqnedit.php?latex=\inline&space;c" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\inline&space;c" title="c" /></a> is computed as <a href="https://www.codecogs.com/eqnedit.php?latex=\inline&space;score_c&space;=&space;\frac{\&hash;points\&space;in\&space;V_{papers}\&space;belongs\&space;to\&space;c}{\&hash;total\&space;points\&space;belongs\&space;to\&space;c}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\inline&space;score_c&space;=&space;\frac{\&hash;points\&space;in\&space;V_{papers}\&space;belongs\&space;to\&space;c}{\&hash;total\&space;points\&space;belongs\&space;to\&space;c}" title="score_c = \frac{\#points\ in\ V_{papers}\ belongs\ to\ c}{\#total\ points\ belongs\ to\ c}" /></a>. The intuition is simple, if the points in <a href="https://www.codecogs.com/eqnedit.php?latex=\inline&space;c" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\inline&space;c" title="c" /></a> that BFS can touch is not enough, we then consider this conference as irrelevent to the SIGIR. We only take the conference that has higher score than a certain creteria, <a href="https://www.codecogs.com/eqnedit.php?latex=\inline&space;S_{conf,&space;smaller}=\{c\&space;|\&space;c\in&space;S_{conf}\wedge&space;score_c>threshold\}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\inline&space;S_{conf,&space;smaller}=\{c\&space;|\&space;c\in&space;S_{conf}\wedge&space;score_c>threshold\}" title="S_{conf, smaller}=\{c\ |\ c\in S_{conf}\wedge score_c>threshold\}" /></a>. (One possible future improvement is to filter out the conference with not enough paper in it).

<div align="center">
<img src="image.png" width="500" style="margin-left:auto;margin-right:auto">
</div>


4. Take all the points of paper that belongs to one of the conference in <a href="https://www.codecogs.com/eqnedit.php?latex=\inline&space;S_{conf,&space;smaller}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\inline&space;S_{conf,&space;smaller}" title="S_{conf, smaller}" /></a>, which is to say <a href="https://www.codecogs.com/eqnedit.php?latex=\inline&space;V_{extract}&space;=&space;\{v|v\&space;belongs\&space;to\&space;c\wedge&space;c&space;\in&space;S_{conf,&space;smaller}\}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\inline&space;V_{extract}&space;=&space;\{v|v\&space;belongs\&space;to\&space;c\wedge&space;c&space;\in&space;S_{conf,&space;smaller}\}" title="V_{extract} = \{v|v\ belongs\ to\ c\wedge c \in S_{conf, smaller}\}" /></a>.

5. Also, treat each conference in <a href="https://www.codecogs.com/eqnedit.php?latex=\inline&space;S_{conf,&space;smaller}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\inline&space;S_{conf,&space;smaller}" title="S_{conf, smaller}" /></a> as a node, connect each conf node with each paper belongs to it, denoted all the conf node as <a href="https://www.codecogs.com/eqnedit.php?latex=\inline&space;V_{conf}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\inline&space;V_{conf}" title="V_{conf}" /></a>, then we have <a href="https://www.codecogs.com/eqnedit.php?latex=\inline&space;V&space;=&space;V_{extract}\cup&space;V_{conf}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?\inline&space;V&space;=&space;V_{extract}\cup&space;V_{conf}" title="V = V_{extract}\cup V_{conf}" /></a> 

At visualization stage, we only visualize the paper node without the conference node, the purpose of conference node here is to draw the points that belongs to a same conference closer, and get rid of the points that has no edges connecting to it.


## Code Structure and Running

Most of the code logic resides in `largeScaleGraph/cpp`, the code logic is split by multiple excutable files so as not to re-run the whole since from beginning.

```
# enter the code file
cd largeScaleGraph/cpp

# optional: to support c++17, load module
module load gcc/7.2.0

# before compiling, revise each cpp file's input and output directory
# compile each bfs layer generator
g++ --std=c++17  generate_first.cpp -o generate_first -lstdc++fs -pthread
g++ --std=c++17  generate_second.cpp -o generate_second -lstdc++fs -pthread
g++ --std=c++17  generate_third.cpp -o generate_third -lstdc++fs -pthread


# run the three layer bfs
./generate_first
./generate_second
./generate_third

# each layer will generate an intermediate representation as
# paper_id \t conf_name \t year \t citation_id_1 \space citation_id_2 \space ....

```













