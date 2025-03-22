from fastapi import FastAPI, Path, Depends, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from dotenv import load_dotenv
from helpers import code_to_tag_generator
from config import supabase
import json
from typing import Dict
import aiohttp
import os

app = FastAPI()

load_dotenv()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to the specific origins you want to allow
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/get_all_projects")
def get_all_projects():
    # Get all projects from supabase
    return {"projects": []}

# Create a project entry in supabase
@app.post("/create_project")
async def create_project(project: Project):
    # Calls a function that calls the Gemini API to process the project code into a json file
    create_project_json(project)
    # Add the project to supabase
    return {"project": project}

@app.post("/upload_project")
async def upload_project(project_name: str = 'default'):
    """
    Upload project files from a Supabase bucket and store project information.
    
    Args:
        bucket_url: URL of the Supabase bucket containing project files
        project_name: Name of the project to store in the database
    """
    try:
        # Get list of files from the bucket
        bucket_name = 'project-files'
        files = supabase.storage.from_(bucket_name).list()

        source_code = ''
        
        # Download and process each file
        async with aiohttp.ClientSession() as session:
            for file in files:
                # Get the file URL
                file_url = supabase.storage.from_(bucket_name).get_public_url(file['name'])
                
                # Download file content
                async with session.get(file_url) as response:
                    if response.status == 200:
                        content = await response.text()
                        source_code += f'<{file['name']}>\n{content}\n</{file['name']}>'
                    else:
                        print(f"Failed to download file: {file['name']}")
        
        # Create project JSON using the helper function
        project_tags = code_to_tag_generator(source_code)
        
        # Store project information in Supabase
        project_data = {
            "project_name": project_name,
            "source_code": source_code,
            "project_tags": project_tags
        }
        
        try:
            result = supabase.table("projects").insert(project_data).execute()
            supabase.storage.empty_bucket(bucket_name)
            return result
        
        except Exception as exception:
            return exception
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing project upload: {str(e)}"
        )

@app.post("/query")
async def process_query(query: str):
    # Pass the query through the LLM to get search fields
    extract_search_fields(query)
    # Retrieve projects from project information database based on search fields
    # Search for code within the project code database corresponding to the projects retrieved
    # Return code snippets from the project code database along with information on where the snippet was retrived from
    return {"project": project}