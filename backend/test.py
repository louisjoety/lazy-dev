from config import supabase
import aiohttp
import asyncio
from config import supabase
from helpers import input_tag_matcher, ai_code_picker

async def process_query():
    query = 'spotify api'
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
        project_source_code = supabase.table("projects").select("source_code").eq("id", project).execute()
        code_snippet = ai_code_picker(project_source_code, query)
        code_snippets.append(code_snippet)

    print(code_snippets)

# Run the async function
if __name__ == "__main__":
    asyncio.run(process_query())

