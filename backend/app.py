from fastapi import FastAPI, Path, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from dotenv import load_dotenv
from helpers import create_project_json

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

# Upload code repository for a project to supabase
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    return {"filename": file.filename}

@app.post("/query")
async def process_query(query: str):
    # Pass the query through the LLM to get search fields
    extract_search_fields(query)
    # Retrieve projects from project information database based on search fields
    # Search for code within the project code database corresponding to the projects retrieved
    # Return code snippets from the project code database along with information on where the snippet was retrived from
    return {"project": project}