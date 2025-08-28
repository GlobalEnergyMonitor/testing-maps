
## Initial Set up
* clone the repo "maps"
* cd into the root of the repo, at the same level as the trackers and src folders
* run npm install (this will install the correct version of node and all node modules that the repo depends on by looking at the package.json and package-lock.json files)
* create a virtual environment and activate it 
* pip install -r requirements.txt 
* create the following Python file by running the following command:
    1. If on Mac/Linux: `cp creds_TEMPLATE.py creds.py`
    2. If on Windows: `copy creds_TEMPLATE.py creds.py`
    3. **This new file should not be committed to git**
    4. Open `creds.py` with a text editor or IDE, and populate this file with the following: 
       *  client_secret = "path to client secret json for google console api" with your local path to client secret 
       *  ACCESS_KEY = '' digital ocean access key stored here in [onepassword ]([[url](https://share.1password.com/s#VKz54HWgtkNU5GVblRPnQSq6Bm_uhJV6aRknYUDGNh4)](https://share.1password.com/s#VKz54HWgtkNU5GVblRPnQSq6Bm_uhJV6aRknYUDGNh4)) (if link expired you can find it in the data team vault)
       *  SECRET_KEY = '' digital ocean secret key stored here in [onepassword ]([[url](https://share.1password.com/s#VKz54HWgtkNU5GVblRPnQSq6Bm_uhJV6aRknYUDGNh4)](https://share.1password.com/s#VKz54HWgtkNU5GVblRPnQSq6Bm_uhJV6aRknYUDGNh4)) (if link expired you can find it in the data team vault)


# gem_tracker_maps

GEM Tracker Maps is served entirely staticly, with no build process. Each tracker only requires a JSON based configuration file, and a data file (mostly hosted in digital ocean as geojson files).

* `/src/` contains the site code, styling information, layout, and supporting assets like images.
* `site-config.js` contains site wide configuration that applies to all trackers
* `/trackers/` contains a director for each tracker
  

## Create a new tracker

Clone the repo. Create a new directory under `/trackers/`. Place the data for the tracker there. Create a symlink to `index.html`: while in the new directory, `ln -s ../../src/index.html`. Create a `config.js`. Commit to GitHub.

## Configure a tracker

First, there are sitewide configurations with [`site-config.js`](site-config.js). Any parameter can be configured site wide. Documentation on the typical site wide parameters is in that file.

The [`config.js for coal-plant`](/trackers/coal-plant/config.js) has documentation on the parameters typically set for a tracker.

## Update tracker data

Create a new branch. Place new data file in the appropriate tracker directory. Test and do quality checks locally by running python -m http.server 8000 at the root of the directory. When ready, make a pull request to the main repository. And accept the pull request to make the update.

## Sharing a preview of the map with others
Warning: you'll have to have the [testing repo]([url](https://github.com/GlobalEnergyMonitor/testing-maps)) cloned to your machine and perhaps already open in an IDE window. You should also have set up two remotes repos, one called official that is linked to the [official repo]([url](https://github.com/GlobalEnergyMonitor/maps)) and the other that is linked to the testing repo. 
On the official repo IDE window, push the branch you have with the new data to the [official remote repo]([url](https://github.com/GlobalEnergyMonitor/maps)), do not merge into the live branch called "gitpages-production". Then go to your IDE window where you have the [testing repo]([url](https://github.com/GlobalEnergyMonitor/testing-maps)) cloned and set up. Pull from your branch name on  [official remote repo]([url](https://github.com/GlobalEnergyMonitor/maps)), accept all merges from official remote since they will override anything going on there, and then push to the test remote repo. Note that currently the test remote repo branch connected to its own gitpages is called "testmaplive". Now you can share the updated map preview via the testing repo's gitpages link. 

Here are the steps on my machine: 
git push origin yourbranchname [in official repo IDE window]
git pull official yourbranchname [in test repo IDE window]
_accept merges_
git push origin testmaplive [in test repo IDE window]


## Routine tracker releases
Non IDE set up / external process duties
- manual copy excel file to google drive then update map tracker log sheet
- manual download geojson file, save to s3
  
* Save a copy of the new data to the: [Tracker official releases (data team copies)](https://drive.google.com/drive/folders/1Ql9V1GLLNuOGoJOotX-wK6wCtDq1dOxo)
* Update the map tracker log sheet ([tab name prep_file](https://docs.google.com/spreadsheets/d/15l2fcUBADkNVHw-Gld_kk7EaMiFFi8ysWt6aXVW26n8/edit?gid=1817870001#gid=1817870001) with the new data's google sheet key from the copy of official data saved above

            
Responsibilities of this repo (hint: maybe we separate this out to other repos soooon)
- create files for map js code from final data
- create files for final data download from final data for multi-tracker maps (mostly regional as of writing)
- manage tracker maps (tile based and json based) via core map js code held in src folders and trackers/tracker folders
- save to s3 digital ocean raw data, map files, parquet of raw data tabs and metadata about these files from start to finish 
- test files at start to get ahead of data consistency or other problems for the map
- test files at end for data integrity


IDE set up 
- adjust all_config.py based on your needs (primarily these initial four and any local file path)
    --trackers_to_update = ['Integrated-simple']# official tracker tab name in map tracker log sheet
    --new_release_date = 'June_2025' # for find replace within about page NEEDS TO BE FULL MONTH
    --releaseiso = '2025-06' # YYYY-MM-DD (day optional)
    --simplified = False # True False
    --priority = [''] # allows you to prioritize global, regional or internal output files

- If you have a new tracker to set up, add to the renaming_cols_dict in all_config.py and add net new columns to final_cols, currently you may want to run the script and check the final names first, since the js map code requires certain formatting, so the dictioanry renaming_cols_dict may not be the final col name



### Pre and Post Tests
* [Testing and data set up for multi tracker map files and data download files](https://docs.google.com/document/d/1LacVuubl4T4CtGzy1KT_GsWrjV-DOI8XQFuLsUliT88/edit?tab=t.0#heading=h.eooqz1k5afdy)
* Tests final dataframe size to original
* Tests capacity values to be sure none after converting to joules are larger than capacity in original units for a country


## Building vector tiles

Currently only used for GIPT map. Adjusted in the tracker/map's config file with the flag "tile" instead of "csv" or "json"

[Detailed GEM Specific Instructions for creating and updating GIPT tiles](https://docs.google.com/document/d/1Lh2GbscAGpM-UKx2UIo2ajHrmII_RWDDiLvGfhMktZg/edit)

Install [csv2geojson](https://github.com/mapbox/csv2geojson) and [tippecanoe](https://github.com/mapbox/tippecanoe)

`% csv2geojson --numeric-fields "Capacity (MW)" Global\ Integrated\ Power\ data\ 2024-02-14.xlsx\ -\ Sheet1.csv > integrated.geojson`

`% tippecanoe -e integrated-2024-02-14.dir --no-tile-compression -r1 -pk -pf --force -l integrated < integrated.geojson`

Copy local files to digital ocean spaces recursively and set public
`aws s3 cp --endpoint-url https://nyc3.digitaloceanspaces.com PATH/TO/DIR/TILES/FROM/TIPPECANOE s3://$BUCKETEER_BUCKET_NAME/NAME_OF_FOLDER_IN_DIGITAL_OCEAN/NAME_OF_SUB_FOLDER_IN_DIGITAL_OCEAN --recursive --acl public-read`



## Hosting 

This can be hosted directly from GitPages.

If hosting on another webserver, the entire repo should be available from a directory on the webserver.

Official Maps can be found at this repo: 

* https://github.com/GlobalEnergyMonitor/maps

Live branch is gitpages-production

### Test Repo 

Maps spun up for PM review before pushed to live can be found in this repo: 

* https://github.com/GlobalEnergyMonitor/testing-maps/

Live branch is testmaplive


## Libraries Used
* Mapbox GL JS for maps
* jQuery for document manipulation / querying
* bootstrap for styling
* DataTables for table view


## New Features Planned
* Fly to unit
* Area based scaling
* Legend overhaul
* Search overhaul 


