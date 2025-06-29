import pandas as pd# convert to combustion capacity table 

# input csv file /Users/gem-tah/GEM_INFO/GEM_WORK/earthrise-maps/gem_tracker_maps/trackers/gist/compilation_output/Iron & Steel-map-file-2025-03-25.csv
gistfile = "/Users/gem-tah/GEM_INFO/GEM_WORK/earthrise-maps/gem_tracker_maps/trackers/gist/compilation_output/Iron & Steel-map-file-2025-03-25.csv"
gist_unitlevel = "/Users/gem-tah/GEM_INFO/GEM_WORK/earthrise-maps/gem_tracker_maps/trackers/gist/compilation_output/Iron & Steel-map-file-2025-03-18.csv"

gistdf = pd.read_csv(gist_unitlevel)

print(gistdf['main-production-equipment'].unique())