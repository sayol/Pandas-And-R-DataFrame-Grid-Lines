# style1: show all rows

import pandas as pd

# Save the original dataframe HTML representation method
_original_repr_html = pd.DataFrame._repr_html_

def _grid_repr_html(self):
    # Automatically wraps every dataframe in your desired style configuration
    return (
        self.style.set_table_styles([
            {"selector": "th, td", "props": [("border", "1px solid black")]}
        ])
        .set_table_attributes('style="border-collapse: collapse;"')
        ._repr_html_()
    )

# Override the global pandas dataframe representation
pd.DataFrame._repr_html_ = _grid_repr_html