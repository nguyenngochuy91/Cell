# Cell: 
## Purpose

In microbiology, a culture is an cultivation of bacteria or other microbial organism. This software is intended to track 
the culture density and ensure the culture stay in exponential growth phase. 

## Requirements
* [Python](https://www.python.org/)
* [networkx](https://networkx.github.io/)
* [pydot](https://github.com/erocarrera/pydot) 
* [graphviz](https://www.graphviz.org/)
## Installation
Users can either use github interface Download button or type the following command in command line:
```bash
git clone https://github.com/nguyenngochuy91/Cell.git
```
The users can either download the source codes of the requirements or use package management systems such as [brew](https://brew.sh/),
 or [conda](https://conda.io/miniconda.html). Users can also try [pip](https://pypi.org/project/pip/), but it has some problems for downloading 
both pydot and graphviz. 

## Usage
The easiest way to run the project is to execute the script [cellTracking](https://github.com/nguyenngochuy91/Cell/blob/master/cellTracking.py)
One can either run it by typing the following in command line:
```bash
./cellTracking.py
```
or :
```bash
python cellTracking.py
```

After that, just follow the instructions printing on the screen. The program will output a text file and a png file.
The text file is in json format, which is basically a dictionary. The dictionary stores all the information of the experiment such as
the name of the experiment, the type of media, the optical density value, the volume value, etc. The png file is a visualization of the process,
the node represent a culture, an edge from one culture to the next could be an update (blue color), or a dilution (black color). In each node, 
there are information of the culture at the date mark. Each edge is labeled with the amount of media added with the volume of the starting culture. 

## Examples:
Here are the examples of a text file and the png file.
1. data.txt


![data](https://github.com/nguyenngochuy91/Cell/blob/master/text.png)
2. data.png


![data](https://github.com/nguyenngochuy91/Cell/blob/master/data.png)