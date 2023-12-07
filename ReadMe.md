AppLoop is using LLM with long context windows to iterativing improve an app based on a text description.

The main idea is to predict the filename additions using a tree structure.

Then when it knows the filenames, it will populate the contents.
Then update the contents of the other files.
Repeat. 

use main.py