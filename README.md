# Minecraft-BST-Functions-Generator

# Usage
## Preparing Input
Go to `input.json` and specify all the fields:

`output_dir_path` := The directory to dump all the functions into

`mcfunction_path` := The mcfunction path corresponding to the output directory, in the form of "namespace:dir/path/in/datapack/". Note it must contain a slash in the end.

`obj_to_match` := The player selector and the objective score you are using as input, in the form of "@s\[selectors\] obj_score_name"

`data` := a bunch of key-commands pairs. The keys are the values of input objective score you are trying to match. The commands are lists of commands you want to run upon successful key match. 

## Run The Script
Before running the script you must first install `drawtree` package using `pip3 install drawtree` in powershell.

After installing the package, run the script by using `python3 bst-bootstrap.py` in powershell.

## Understanding the Output
The script will produce two outputs: a directory containing all the functions, a "tree_graph.txt" file printing the structure of the tree.

`The directory` along with the functions are not immediately usable, as it is not a complete datapack. Instead, you should put these mcfunction files into your datapack, at the position you specified in "mcfunction_path". When trying to match the score in game, run the function corresponding to the root node. (To find out which file that is, keep reading below.) 

All the mcfunction files are named "\[key\].mcfunction" or "\[key\]\_run.mcfunction". The latter one is a helper function in case there are multiple commands paired with a key. 

`tree_graph.txt` records the structure of the tree. The root node is the node at very top. In this implementation, when a node has less than or equal to four descendents, it will become a leaf node, and simply match all the descendents in its own file. Therefore the structure printed here is not completely accurate. (However, you can just easily re-imagine it in your mind.)
