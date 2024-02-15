# Objective

This tool intends to put a condition in each trigger from ```triggers.txt```, 
just before the ```BEGIN``` of the trigger itself and before the ```END``` of the trigger (the last ```END``` keyword)

## Usage

You should run the query in your data base:

```select trigger_declaration || 'endoffile' from your_triggers```

The concatenation with "endoffile" is needed in order to the script detect each trigger as a single trigger

The result of that query shall be put in the ```triggers.txt``` file, and so you run ```py run.py```

Then, the ```output.txt``` shall be filled with the updated triggers

If you need to edit the conditional, just type what you want in the assignment of the variable ```main_condition``` inside ```run.py```
