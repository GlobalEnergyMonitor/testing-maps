## this should be updated at key points in the run_maps.py script 
## it then gets pushed to s3 to live in the folder like TRACKER/RELEASEISO
### maybe we push them and let each overwrite so we always have it in s3 but wed need to rename to be blander like tracker-releaseiso

# took from make_map_tracker_objs

            
        # # save to metadata
        # mfile_actual = f"/Users/gem-tah/GEM_INFO/GEM_WORK/earthrise-maps/gem_tracker_maps/metadata_files/{map_obj.mapname}_{releaseiso}_{iso_today_date}_metadata.yaml"
        # print(f'this is mfile_actual: {mfile_actual}')
        # input('check if it matches')
        # # Prepare dictionary representations, but do not convert tracker_source_obj.data or map_obj.trackers
        # tracker_dict = tracker_source_obj.__dict__.copy()
        # map_dict = map_obj.__dict__.copy()

        # # Replace DataFrames/lists with their lengths for reporting
        # if isinstance(tracker_dict.get('data', None), pd.DataFrame):
        #     df = tracker_dict['data']
        #     tracker_dict['data'] = {
        #     "info": f"DataFrame with {len(df)} rows",
        #     "columns": [{col: str(df[col].dtype)} for col in df.columns],
        #     "columns2": [df.info()]
        #     }
        # if isinstance(map_dict.get('trackers', None), list):
        #     map_dict['trackers'] = f"List with {len(map_dict['trackers'])} TrackerObjects"

        # # Remove DataFrames (not serializable) or convert to string
        # for d in [tracker_dict, map_dict]:
        #     for k, v in list(d.items()):
        #         if isinstance(v, pd.DataFrame):
        #             d[k] = v.to_dict()  # or v.to_json() if preferred
        #         elif isinstance(v, list) and v and isinstance(v[0], TrackerObject):
        #             # For map_obj.trackers, store acros or dicts
        #             d[k] = [t.__dict__.copy() for t in v]

        # # Append to YAML file instead of overwriting

        # # Check if file exists and load existing data
        # if os.path.exists(mfile_actual):
        #     with open(mfile_actual, "r") as f:
        #         try:
        #             existing_data = yaml.safe_load(f) or []
        #         except Exception:
        #             existing_data = []
        # else:
        #     existing_data = []

        # # Ensure existing_data is a list
        # if not isinstance(existing_data, list):
        #     existing_data = [existing_data] if existing_data else []

        # # Append new entry
        # existing_data.append({'tracker': tracker_dict, 'map': map_dict})

        # # Write back the updated list
        # with open(mfile_actual, "w") as f:
        #     yaml.dump(existing_data, f, default_flow_style=False)


import os
import yaml
import sys

METADATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'metadata_files')
os.makedirs(METADATA_DIR, exist_ok=True)

def get_metadata_path(run_id):
    return os.path.join(METADATA_DIR, f"{run_id}.yaml")

def create_or_load_metadata(run_id):
    path = get_metadata_path(run_id)
    if os.path.exists(path):
        with open(path, 'r') as f:
            data = yaml.safe_load(f) or {}
    else:
        data = parse_run_id(run_id)
        with open(path, 'w') as f:
            yaml.dump(data, f, default_flow_style=False)
    return data

def save_metadata(run_id, data):
    path = get_metadata_path(run_id)
    print(f'{path}')
    with open(path, 'w') as f:
        yaml.dump(data, f, default_flow_style=False)


def parse_run_id(mfile):
    parsed = mfile.split('_')
    class Metadata:
        def __init__(self, tracker, releaseiso, today):
            self.tracker_name = tracker
            self.release_iso = releaseiso
            self.today_date = today


        def to_dict(self):
            return {
                'tracker_name': self.tracker_name,
                'release_iso': self.release_iso,
                'today_date': self.today_date,

            }

    tracker = parsed[0]
    releaseiso = parsed[1]
    today = parsed[2]

    metadata_obj = Metadata(tracker, releaseiso, today)
    metadata = metadata_obj.to_dict()

    return metadata

# Example usage:
if __name__ == "__main__":
    # run_id = "example_run_001"
    if len(sys.argv) < 2:
        print("Usage: python make_metadata.py <mfile>")
        sys.exit(1)
    mfile = sys.argv[1]
    metadata = create_or_load_metadata(mfile)
    save_metadata(mfile, metadata)
