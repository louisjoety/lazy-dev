import base64
from dotenv import load_dotenv
import os
from google import genai
from google.genai import types

load_dotenv()

def code_to_tag_generator(project: str):
    # Calls the Gemini API to process the project code into a python list containing tags
    
    
    response = ""

    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=project),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        top_k=40,
        max_output_tokens=8192,
        response_mime_type="text/plain",
        system_instruction=[
            types.Part.from_text(text="""CONTEXT: You are an expert code analyser, specialized in extracting vital keywords from the source code of programs. 

INSTRUCTIONS: Your job is to analyse a .txt file containing all the source code of a project and come up with tags that are associated with categories such as Tech languages used, libraries used, frameworks used, APIs used, program type(Web App, Mobile App, CLI tool, etc).
the code for each file is contained within html styled tags. For example, index.html code is enclosed within <index.html> and </index.html>.
Ignore .gitignore and cache files. A tag should not look like  \"Tech languages used: HTML, Python\", instead the correct tags should be \"HTML\", \"Python\". Make sure there are no duplicate tags.

RESPONSE FORMAT: Respond in python list containing tags"""),
        ],
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        response = response + chunk.text

    # converting string output into a list type
    return eval(response[10:-4])