import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os

# Google Sheets setup
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
CREDS_FILE = 'path/to/your/credentials.json'  # Update with your credentials file path
SPREADSHEET_ID = 'your_spreadsheet_id'        # Update with your spreadsheet ID
TEMPLATE_SHEET_NAME = 'Templates'             # Update with your sheet name

def get_gspread_client():
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPES)
    client = gspread.authorize(creds)
    return client

def fetch_templates():
    client = get_gspread_client()
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(TEMPLATE_SHEET_NAME)
    templates = sheet.get_all_records()
    return templates

def load_tracker_variables(tracker_name):
    # Placeholder: Load variables for a tracker from your repo files
    # For example, you might read from a JSON/YAML file
    # Return a dict of variables
    return {
        "tracker_name": tracker_name,
        "description": "Sample description",
        # Add more variables as needed
    }

def render_template(template_text, variables):
    # Simple variable substitution using str.format
    return template_text.format(**variables)

def make_about_pages():
    templates = fetch_templates()
    trackers = ['tracker1', 'tracker2']  # Replace with dynamic tracker list
    for tracker in trackers:
        variables = load_tracker_variables(tracker)
        for template in templates:
            template_text = template.get('TemplateText', '')
            about_page = render_template(template_text, variables)
            output_path = os.path.join('about_pages', f'{tracker}_about.html')
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w') as f:
                f.write(about_page)
            print(f'Generated: {output_path}')

if __name__ == "__main__":
    make_about_pages()