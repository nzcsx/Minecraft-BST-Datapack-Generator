# Minecraft-BST-Functions-Generator

# Usage
## Preparing Input
Go to `input.json` and specify all the fields:

`output_dir_path` := The directory to dump all the functions into

`mcfunction_path` := The mcfunction path corresponding to the output directory, in the form of "namespace:dir/path/in/datapack/". Note it must contain a slash in the end.

`obj_to_match` := The player selector and the objective score you are using as input, in the form of "@s\[selectors\] obj_score_name"

`data` := a bunch of key-commands pairs. The keys are the values of input objective score you are trying to match. The commands are lists of commands you want to run upon successful key match. 

## Run The Script
Before running the script you must install `drawtree` package first using `pip3 install drawtree` in powershell.

After installing, run the script by using `python bst-bootstrap.py` in powershell.

## Understanding the Output
The script will produce two outputs: a directory containing all the functions, a `tree_graph.txt` file printing the structure of the tree.
