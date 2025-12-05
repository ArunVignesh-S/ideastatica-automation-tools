
async def extract_ids_from_ideacon(ideacon_file_path):
    proj_id = None
    con_id = None
    baseUrl = "http://localhost:5000"
    
    import ideastatica_connection_api.connection_api_service_attacher as connection_api_service_attacher
    from ideastatica_connection_api.models import con_mprl_cross_section
    from ideastatica_connection_api import models
    import os
    
    with connection_api_service_attacher.ConnectionApiServiceAttacher(baseUrl).create_api_client() as api_client:
        uploadRes = api_client.project.open_project_from_filepath(ideacon_file_path)
        #Get the project and connection ids
        proj_id = api_client.project.active_project_id
        connections = api_client.connection.get_connections(proj_id)
        con_id = connections[0].id
        
        api_client.settings.get_settings(proj_id, "Report")

        api_client.project.close_project(proj_id)
    
    return proj_id, con_id

def get_idea_materials(grade, thickness, is_closed_section=False):

    """Get IdeaStatica materials based on grade and thickness.
    Args:
        grade (str): Material grade.
        thickness (float): Material thickness in mm.
        is_closed_section (bool): Whether the section is closed or not.
    Returns:
        str: Material name.
    """
    material_map = {
        "material_grade": {
            False: {(0, 16): "material_grade",
                    (16, 40): "material_grade",
                    (40, 60): "material_grade",
                    (60, 100): "material_grade"},
            True: {(0, 16): "material_grade",
                    (16, 40): "material_grade",
                    (40, 60): "material_grade",
                    (60, 100): "material_grade"},
        },
        "material_grade": {
            False: {(0, 16): "material_grade",
                    (16, 40): "material_grade",
                    (40, 60): "material_grade",
                    (60, 100): "material_grade"},
            True: {(0, 16): "material_grade",
                    (16, 40): "material_grade",
                    (40, 60): "material_grade"},
        }
    }

    if grade in material_map:
        thickness_map = None
        if is_closed_section:
            thickness_map = material_map[grade][True]
        else:
            thickness_map = material_map[grade][False]
        
        for (min_thick, max_thick), material_name in thickness_map.items():
            if min_thick < thickness <= max_thick:
                return material_name
    return "Unknown Material"
   

if __name__ == "__main__":
    
    # Required Imports
    from file_and_folder_utilities import get_ideacon_files
    import asyncio
    
    # Example usage
    input_folder = r"folder_path"
    
    ideacon_files = get_ideacon_files(input_folder)
    print(f".ideaCon files found: {ideacon_files}")
    
    for file in ideacon_files:
        proj_id, con_id = asyncio.run(extract_ids_from_ideacon(file))
        print(f"File: {file} => Project ID: {proj_id}, Connection ID: {con_id}")