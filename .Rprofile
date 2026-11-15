library(repr)
library(utils)

# Safely fetch the original HTML representation method using the utils namespace
orig_repr_html_df <- utils::getS3method("repr_html", "data.frame")

# Create a wrapper that automatically injects grid line CSS
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

# Register the method so it catches data frames and tibbles automatically
registerS3method("repr_html", "data.frame", repr_html.data.frame)