
## Initial Set up
* clone the repo "maps"
* cd into the root of the repo, at the same level as the trackers and src folders
* You must have node.js or npm installed already on your computer, check if you do by running `node -v`
`npm -v` if you don't install it here https://docs.npmjs.com/downloading-and-installing-node-js-and-npm and then relaunch your terminal and then run `nvm install 18.17.0` `nvm use 18.17.0` OR latest version
* Run `npm install` (this will install the correct version of node and all node modules that the repo depends on by looking at the package.json and package-lock.json files)
* WARNING: If you are on a windows machine to test the maps you'll need to launch the server through a linux terminal, such as WSL. 


# running list of items the config.js files require
1. no underscores in variable names if name is in legend filter
2. country column should have a semicolon at the end so multiple countries can be handled correctly
3. capacityLabel when not a blank string initiates the unit summary feature, when it is empty the capacity and status get added to the modal details popup in the config's array. When it is not blank, the statusDisplayField capacityDisplayField are used in a function in site.js


* create a virtual environment and activate it

* `pip install -r requirements.txt`

  
* create the following Python file by running the following command:
    1. If on Mac/Linux: `cp creds_TEMPLATE.py creds.py`
    2. If on Windows: `copy creds_TEMPLATE.py creds.py`
    3. **This new file should not be committed to git**
    4. Open `creds.py` with a text editor or IDE, and populate this file with the following: 
       *  client_secret = "path to client secret json for google console api" with your local path to your client secret (if this is your first time setting that up check for support here https://developers.google.com/workspace/guides/create-credentials) 
       *  ACCESS_KEY = '' digital ocean access key stored here in [onepassword ]([[url](https://share.1password.com/s#R_Muz4jORFM9dJBZORUcopx69EGgKcgpKuzD96VKZXE)](if link expired you can find it in the data team vault)
       *  SECRET_KEY = '' digital ocean secret key stored here in [onepassword ]([[url](https://share.1password.com/s#R_Muz4jORFM9dJBZORUcopx69EGgKcgpKuzD96VKZXE)] (if link expired you can find it in the data team vault)



## Steps for updating maps for routine tracker releases

### Non IDE set up / external process
- Depending on the tracker:
* Save a copy of the new data to the: [Tracker official releases (data team copies)](https://drive.google.com/drive/folders/1Ql9V1GLLNuOGoJOotX-wK6wCtDq1dOxo)
* Update the map tracker log sheet ([tab name prep_file](https://docs.google.com/spreadsheets/d/15l2fcUBADkNVHw-Gld_kk7EaMiFFi8ysWt6aXVW26n8/edit?gid=1817870001#gid=1817870001) with the new data's google sheet key from the copy of official data saved above

- OR manually download geojson file and save to s3 (for example: GGIT, GOIT, GGIT-LNG)
            
Responsibilities of this repo (hint: maybe we separate this out to other repos soon)
- create files for map js code from final data
- create files for final data download from final data for multi-tracker maps (mostly regional as of writing)
- manage tracker maps (tile based and json based) via core map js code held in src folders and trackers/tracker folders
- save to s3 digital ocean raw data, map files, parquet of raw data tabs and metadata about these files from start to finish 
- test files at start to get ahead of data consistency or other problems for the map
- test files at end for data integrity


### IDE set up 
- adjust `all_config.py` based on your needs (primarily these initial four and any local file path)
    --`trackers_to_update = ['Bioenergy']` # official tracker tab name in map tracker log sheet
    --`new_release_date = 'June_2025'` # for find replace within about page NEEDS TO BE FULL MONTH
    --`releaseiso = '2025-06'` # YYYY-MM-DD (day optional)
    --`simplified = False` # True False
    --`priority = ['gbpt']` # allows you to prioritize global, regional or internal output files


### Run the processing code
- At the root run `python run_maps.py`
- The output will be all map and data download files related to the tracker that has new data (held in trackers_to_update, can be more than 1)
- You can find the output files in the appropriate `trackers/{mapname} subfolder`
- For example, the new Bioenergy output file will be in `trackers/bioenergy/compilation_output/` and the updated Africa output will be in `trackers/africa/compilation_output/`
- with that new file you'll paste the path to it into the relevant map's config.js file. It can be csv, or geojson. It usually will look like this:
`var config = {
  geojson: 'path/to/file'
  ....other config variables for that map}`

### Manually test the maps and data downloads
- To test the map locally you will just need to run `python -m http.server 8000` at the root of the repo and navigate to `trackers/map_folder_name`
- If the map also has a data download deliverable (all regional maps), you'd upload those to its own folder in [google drive]([url](https://drive.google.com/drive/u/0/folders/1I225d18KhpPXXwhp-q7oeBU3RLFx7N60)) and share with Carolina/Comms after checking the about pages and filtering look ok



### Creating a new testing map repo that pulls from official remote
- create folder on local machine where you want this to be
- git clone this repo git@github.com:GlobalEnergyMonitor/maps.git
- cd maps
- Add the testing repo as a new remote git remote add testing https://github.com/your/testing-repo.git
- Set the testing repo as your default push remote git remote set-url --push origin https://github.com/your/testing-repo.git
- add the original as a remote, only for pulling git remote add upstream git@github.com:GlobalEnergyMonitor/maps.git
- allow unrelated histories git pull upstream gitpages-production --allow-unrelated-histories
- then you'll likely need to force the first push to your new repo git push origin main --force
- be sure to rename the remotes so that you can only push to the original if you specify upstream git remote set-url origin NEW_URL git remote add upstream OLD_URL

- Pull from the original git pull upstream gitpages-production
- push only to the testing git push origin main


### Sharing a preview of the map with others
Warning: you'll have to have the [testing repo]([url](https://github.com/GlobalEnergyMonitor/testing-maps)) cloned to your machine and perhaps already open in an IDE window. You should also have set up two remotes repos, one called official that is linked to the [official repo]([url](https://github.com/GlobalEnergyMonitor/maps)) and the other that is linked to the testing repo. (see above section on Steps to creating a new testing map repo that pulls from official remote for how to do that, note you DO NOT need to create a new testing repo for this, just clone the testing repo instead of the maps one)

On the official repo IDE window, push the branch you have with the new data to the [official remote repo]([url](https://github.com/GlobalEnergyMonitor/maps)), do not merge into the live branch called "gitpages-production". Then go to your IDE window where you have the [testing repo]([url](https://github.com/GlobalEnergyMonitor/testing-maps)) cloned and set up. Pull from your branch name on  [official remote repo]([url](https://github.com/GlobalEnergyMonitor/maps)), accept all merges from official remote since they will override anything going on there, and then push to the test remote repo. Note that currently the test remote repo branch connected to its own gitpages is called "testmaplive". Now you can share the updated map preview via the testing repo's gitpages link. 

Here are the steps on my machine: 
git push origin yourbranchname [in official repo IDE window]
git pull official yourbranchname [in test repo IDE window]
_accept merges_
git push origin testmaplive [in test repo IDE window]





### About the maps repo from EarthGenome 

GEM Tracker Maps are served entirely staticly, with no build process. Each tracker only requires a JSON based configuration file, and a data file (mostly hosted in digital ocean as geojson files).

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

### Test Data Repo 

Maps spun up for PM review before pushed to live can be found in this repo: 

* https://github.com/GlobalEnergyMonitor/testing-maps/

Live branch is testmaplive

# Test Features Repo

* https://github.com/GlobalEnergyMonitor/features-maps/


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


