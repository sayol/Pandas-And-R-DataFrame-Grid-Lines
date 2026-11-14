# IPython Startup Script

## Setup

This is the IPython startup directory

.py and .ipy files in this directory will be run *prior* to any code or files specified
via the exec_lines or exec_files configurables whenever you load this profile.

Files will be run in lexicographical order, so you can control the execution order of files
with a prefix, e.g.::

    00-first.py
    50-middle.py
    99-last.ipy

## Show Grid Lines of Pandas DataFrame

1. Create new file called `00-pandas-grid.py` in the directory `C:\Users\<User>\.ipython\profile_default\startup`
2. Include the follow contents into `00-pandas-grid.py` file:

```python
# Default Style: show some rows (default)
import pandas as pd

# Save the original dataframe HTML representation method
_original_repr_html = pd.DataFrame._repr_html_

def _grid_repr_html(self):
    # Get the standard, row-truncated HTML representation
    html = _original_repr_html(self)
    
    # Wrap it with a scoped style block that enforces grid lines 
    # while preserving truncation for large dataframes
    return f"""
    <div>
        <style>
            table.dataframe, table.dataframe th, table.dataframe td {{
                border: 1px solid black !important;
                border-collapse: collapse !important;
            }}
        </style>
        {html}
    </div>
    """

# Override the global pandas dataframe representation
pd.DataFrame._repr_html_ = _grid_repr_html
```

## Create Jupyter Notebook

1. Create a Jupyter notebook file called `example.ipynb`
2. Create a notebook cell with the code
```python
import pandas as pd
import seaborn as sns

df = sns.load_dataset("penguins")
df
```
3. Execute the code cell and enjoy!
