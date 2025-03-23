from fastapi import FastAPI, Path, Depends, HTTPException, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from dotenv import load_dotenv
from helpers import code_to_tag_generator, input_tag_matcher, ai_code_picker
from config import supabase
import json
from typing import Dict
import aiohttp
import os
from pydantic import BaseModel  # Add this import at the top

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

# Create a model for the request body
class ProjectUploadRequest(BaseModel):
    project_name: str

class ChatbotRequest(BaseModel):
    query: str

@app.get("/get_all_projects")
def get_all_projects():
    """
    Get all projects from Supabase with their names and tags.
    Returns a list of projects with their names and associated tags.
    """
    try:
        response = supabase.table("projects").select("project_name, tags").execute()
        if response.data:
            return {"projects": response.data}
        return {"projects": []}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch projects: {str(e)}"
        )

@app.post("/upload_project")
async def upload_project(request: ProjectUploadRequest):
    """
    Upload project files from a Supabase bucket and store project information.
    
    Args:
        request: ProjectUploadRequest containing project_name
    """
    try:
        # Get list of files from the bucket
        bucket_name = 'project-files'
        files = supabase.storage.from_(bucket_name).list()

        source_code = ''
        # Download and process each file
        async with aiohttp.ClientSession() as session:
            for file in files:
                '''
                # Get the file URL
                try:
                    # file_url = supabase.storage.from_(bucket_name).get_public_url(file['name'])
                    file_url = f'https://cfptchtfrdemsuheznmr.supabase.co/storage/v1/object/public/project-files//{file["name"]}'
                except Exception as e:
                    print(e)
                '''
                
                try:
                    # Download file content directly from Supabase
                    response = supabase.storage.from_(bucket_name).download(file['name'])
                    
                    # For text files, decode the bytes to string
                    try:
                        content = response.decode('utf-8')
                        source_code += f'<{file["name"]}>\n{content}\n</{file["name"]}>\n'
                        print(f"Successfully processed {file['name']}")
                    except UnicodeDecodeError:
                        print(f"Skipping binary file: {file['name']}")
                        continue
                        
                except Exception as e:
                    print(f"Failed to download file: {file['name']}, error: {str(e)}")
        
        # Create project JSON using the helper function
        project_tags = code_to_tag_generator(source_code)
        
        # Store project information in Supabase using the project name from the request
        project_data = {
            "project_name": request.project_name,  # Use the project name from the request
            "source_code": source_code,
            "tags": project_tags
        }
        
        try:
            result = supabase.table("projects").insert(project_data).execute()
            supabase.storage.empty_bucket(bucket_name)
            print(result)
            return result
        
        except Exception as exception:
            print(exception)
            return exception
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing project upload: {str(e)}"
        )

@app.post("/query")
async def process_query(request: ChatbotRequest):
    query = request.query
    projects_with_tags = {}

    try:
        response = supabase.table("projects").select("id, tags").execute()
        for project in response.data:
            projects_with_tags[project['id']] = project['tags']
    except Exception as e:
        print(e)
        return e
    
    selected_project_ids = input_tag_matcher(query, projects_with_tags)
    code_snippets = []

    for project in selected_project_ids:
        response = supabase.table("projects").select("project_name, source_code").eq("id", project).execute()
        response = response.data[0]
        code_snippet = ai_code_picker(response['source_code'], query)
        # code_snippets[response['project_name']] = code_snippet

        code_snippets.append({"project_name": response['project_name'], "matched_files": list(code_snippet.keys()), "snippets": code_snippet})

    return {"code_snippets": code_snippets}