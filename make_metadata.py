## this should be updated at key points in the run_maps.py script 
## it then gets pushed to s3 to live in the folder like TRACKER/RELEASEISO
### maybe we push them and let each overwrite so we always have it in s3 but wed need to rename to be blander like tracker-releaseiso



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
