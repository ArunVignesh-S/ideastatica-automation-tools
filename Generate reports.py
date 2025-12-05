import os
from pathlib import Path
import ideastatica_connection_api as idea

# --- Fixed Input Handling ---
source_folder = r"Folder Path"
target_folder = r"Folder Path"

# Validate folders
if not os.path.exists(source_folder):
    print(f"Error: Source folder '{source_folder}' does not exist.")
    exit()

# Create target folder
os.makedirs(target_folder, exist_ok=True)

# REST API setup
api_url = "http://localhost:5000"

configuration = idea.Configuration(host=api_url)

configuration.api_key['ClientId'] = 'MyPythonScript'
api_client = idea.ApiClient(configuration)

project_api = idea.ProjectApi(api_client)
report_api = idea.ReportApi(api_client)

idea_files = list(Path(source_folder).glob("*.ideaCon"))

if not idea_files:
    print("No .ideaCon files found.")
    exit()

print(f"Found {len(idea_files)} files.")

for file_path in idea_files:
    print(f"Processing: {file_path.name}")
    try:
        # Open project
        project_data = project_api.open_project(str(file_path))
        project_id = project_data.project_id

        connections = project_data.connections or []

        for conn in connections:
            conn_id = conn.id
            conn_name = conn.name or f"Conn_{conn_id}"

            pdf_filename = f"{file_path.stem}_{conn_name}.pdf"
            pdf_path = os.path.join(target_folder, pdf_filename)

            # --- FIX: get pdf bytes ---
            pdf_response = report_api.generate_pdf(project_id, conn_id, _preload_content=False)
            pdf_data = pdf_response.data

            with open(pdf_path, "wb") as f:
                f.write(pdf_data)

            print(f"  ✓ Saved: {pdf_filename}")

        project_api.close_project(project_id)

    except Exception as e:
        print(f"  ✗ Error: {e}")
        continue

print("\n✓ All reports exported.")
