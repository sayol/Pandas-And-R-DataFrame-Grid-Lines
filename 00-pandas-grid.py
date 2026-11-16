try:
    import pandas as pd

    # Save the original dataframe HTML representation method
    _original_repr_html = pd.DataFrame._repr_html_

    def _grid_repr_html(self):
        # Get the standard, row-truncated HTML representation
        html = _original_repr_html(self)
        
        # Wrap it with a scoped style block that enforces green grid lines 
        # while preserving truncation for large dataframes
        return f"""
        <div>
            <style>
                table.dataframe, table.dataframe th, table.dataframe td {{
                    border: 1px solid green !important;
                    border-collapse: collapse !important;
                }}
            </style>
            {html}
        </div>
        """

    # Override the global pandas dataframe representation
    pd.DataFrame._repr_html_ = _grid_repr_html

except ModuleNotFoundError:
    # Pandas is not installed on this system; skip configuration safely
    pass