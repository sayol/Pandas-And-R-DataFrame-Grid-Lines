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

## Python Pandas DataFrame Green Grid Lines

1. Create new file called `00-pandas-grid.py` in the directory `C:\Users\<User>\.ipython\profile_default\startup`
2. Include the follow contents into `00-pandas-grid.py` file:

```python
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
```

## Python Pandas DataFrame Example

1. Create a Jupyter notebook file called `example-python.ipynb`
2. Create a notebook cell with the code
```python
import pandas as pd
import seaborn as sns

df = sns.load_dataset("penguins")
df.sample(n=10, random_state=42)
```
3. Execute the code cell and enjoy!

# IRkernel Startup Script

## R DataFrame/Tibble Green Grid Lines

1. Check where the `.Rprofile` lives in
```R
normalizePath("~")
```
2. Create the `.Rprofile` in the location

```R
file.edit("~/.Rprofile")
```
3. Include the following contents into `.Rprofile` file:
```R
# Safely apply green grid lines only if the 'repr' package is available
tryCatch({
  if (requireNamespace("repr", quietly = TRUE)) {
    library(repr)
    library(utils)
    
    # Safely fetch the original HTML representation method
    orig_repr_html_df <- utils::getS3method("repr_html", "data.frame")
    
    # Create a wrapper that automatically injects green grid line CSS
    repr_html.data.frame <- function(obj, ...) {
      html_code <- orig_repr_html_df(obj, ...)
      paste0(
        '<style>
          .dataframe, .dataframe th, .dataframe td {
            border: 1px solid green !important;
            border-collapse: collapse !important;
          }
          .dataframe th, .dataframe td {
            padding: 6px 10px !important;
          }
        </style>',
        html_code
      )
    }
    
    # Register the method for data frames and tibbles automatically
    registerS3method("repr_html", "data.frame", repr_html.data.frame)
  }
}, error = function(e) {
  # Fail silently if any error occurs during configuration
})
```
## R DataFrame/Tibble Example

1. Create a Jupyter notebook file called `example-r.ipynb`
2. Create a notebook cell with the code
```R
data("mtcars")
head(mtcars, n = 10)
```

## All-in-One Installation

1. Create a PowerShell script `Install-GridSettings.ps1`
2. Include the following script into `Install-GridSettings.ps1`
```pwsh
<#
.SYNOPSIS
    Automated installer for global green grid lines in Jupyter (Python/Pandas & R).
#>

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host " Installing Global Green Grid Line Configurations..." -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan

# ----------------------------------------------------
# 1. PYTHON / IPYTHON (PANDAS) SETUP
# ----------------------------------------------------
$ipythonStartupDir = Join-Path $HOME ".ipython\profile_default\startup"

if (-not (Test-Path $ipythonStartupDir)) {
    New-Item -ItemType Directory -Force -Path $ipythonStartupDir | Out-Null
    Write-Host "[+] Created IPython startup directory." -ForegroundColor DarkGray
}

$pythonScriptPath = Join-Path $ipythonStartupDir "00-pandas-grid.py"
$pythonContent = @"
try:
    import pandas as pd

    # Save the original dataframe HTML representation method
    _original_repr_html = pd.DataFrame._repr_html_

    def _grid_repr_html(self):
        # Get standard row-truncated HTML representation
        html = _original_repr_html(self)
        
        # Wrap with scoped green border styling
        return f"""
        <div>
            <style>
                table.dataframe, table.dataframe th, table.dataframe td {{
                    border: 1px solid green !important;
                    border-collapse: collapse !important;
                }}
            </style>
            {{html}}
        </div>
        """

    # Override global pandas dataframe representation safely
    pd.DataFrame._repr_html_ = _grid_repr_html

except ModuleNotFoundError:
    # Pandas is not installed on this system; skip configuration safely
    pass
"@

Set-Content -Path $pythonScriptPath -Value $pythonContent -Encoding UTF8
Write-Host "[SUCCESS] Python Pandas configuration installed at:" -ForegroundColor Green
Write-Host "          $pythonScriptPath" -ForegroundColor White


# ----------------------------------------------------
# 2. R (.RPROFILE) SETUP
# ----------------------------------------------------
$documentsDir = [Environment]::GetFolderPath('MyDocuments')
$rProfilePath = Join-Path $documentsDir ".Rprofile"

$rContent = @"

# --- Global Green Grid Lines for R Data Frames & Tibbles ---
tryCatch({
  if (requireNamespace("repr", quietly = TRUE)) {
    library(repr)
    library(utils)
    
    # Safely fetch the original HTML representation method
    orig_repr_html_df <- utils::getS3method("repr_html", "data.frame")
    
    # Create wrapper that injects green grid lines
    repr_html.data.frame <- function(obj, ...) {
      html_code <- orig_repr_html_df(obj, ...)
      paste0(
        '<style>
          .dataframe, .dataframe th, .dataframe td {
            border: 1px solid green !important;
            border-collapse: collapse !important;
          }
          .dataframe th, .dataframe td {
            padding: 6px 10px !important;
          }
        </style>',
        html_code
      )
    }
    
    # Register the method automatically
    registerS3method("repr_html", "data.frame", repr_html.data.frame)
  }
}, error = function(e) {
  # Fail silently if any error occurs during startup
})
"@

if (Test-Path $rProfilePath) {
    Add-Content -Path $rProfilePath -Value $rContent -Encoding UTF8
    Write-Host "[SUCCESS] Appended R grid configuration to existing .Rprofile at:" -ForegroundColor Green
} else {
    Set-Content -Path $rProfilePath -Value $rContent -Encoding UTF8
    Write-Host "[SUCCESS] Created new .Rprofile with R grid configuration at:" -ForegroundColor Green
}
Write-Host "          $rProfilePath" -ForegroundColor White

Write-Host "====================================================" -ForegroundColor Cyan
Write-Host " Installation Complete! Restart your Jupyter kernels." -ForegroundColor Cyan
Write-Host "====================================================" -ForegroundColor Cyan
```
3. Run the script using **Window PowerShell** or **PowerShell**
4. Enjoy the `green grid lines` of Python pandas data frame, R data frame and R dplyr tibble!