# FriendlyCachex
##### A nice and friendly Cachex (a game designed by UoM COMP30024-AI 2022-Sem1) player.

# Contributors
###### by FriendlyAI Devs
___Your Prefered Name___  \
___Leo Xinqi Yu___ xinqiy@student.unimelb.edu.au

# Run & Debug
### Path Finding
Members are expected to execute using
#### Single In
``python path/__main__.py path_to_input.json `` for running the path finding algorithm on (**SINGLE**) input json file you specified.
#### Highthroughput In
``python path/__main__.py -m full_or_relative_path_to_folder `` -m flag (MULTIPLE) followed by path to a folder, to run on all inputs in the specified folder. \
``python path/__main__.py -m folder_name `` **(RECOMMEND)** a single folder name, asking the program to locate it in the ```./in``` folder.
#### Single Out
``./out `` will be the folder you'd find the output file, **together with a copy of it's input file**. 
#### Highthroughput Out
``./out/XXX_out `` will be the folder containing all output files, **together copys of their input file**. XXX is the name of your input folder. 


### Game Play
TODO::

# IO
### Stage 1: Manuel inputs .json
#### Input file naming suggested format
```r5_4_0_leo_0.json```  \
**r5**: AI play as RED, board size N = 5. \
**4_0**: 4 opponent's and 0 our cells exist on the board. \
**leo**: Creator name. \
**0**: An int uniquely identifies the input file with same head arguments. 

#### Output file naming convension
in ```r5_4_0_leo_0.json``` out ```r5_4_0_leo_OUT_0.txt```  \
in ```r6_3_3_leo_0.json``` out ```r6_3_3_selena_OUT_0.txt``` 

### Stage 2: generate inputs with GUI and enable PvC/CvC mode


# References & Thanks
