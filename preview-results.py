import pandas as pd
import webbrowser

# Example data
data = {'Column1': [1, 2, 3], 'Column2': ['A', 'B', 'C']}
df = pd.DataFrame(data)

# Convert DataFrame to HTML
html_table = df.to_html()

# Save to an HTML file
with open("data_results.html", "w") as f:
    f.write(html_table)

import os

# Open the HTML file in the default web browser
file_path = os.path.abspath("data_results.html")
webbrowser.open(f"file://{file_path}")