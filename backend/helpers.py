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

def input_tag_matcher(user_prompt: str, id_to_tags):
    # Pass the query through Gemini to get search fields
    response=""


    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="User prompt: "+user_prompt+"\n"+"tags: "+id_to_tags),
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
            types.Part.from_text(text="""CONTEXT: You are an expert prompt analyser 

INSTRUCTIONS: You will be given a key-value pair. The value is a list of tags and the key is the project id. Your task is to analyse the tags and check whether the user prompt matches with the tags and see if there is significant similarity and relevance between the tags and what the user actually wants. If it is relevant, append the project id to the list of project ids. If there are none, return an empty list. Only output the list. Do not generate any extra text.

RESPONSE FORMAT: Python list containing project ids."""),
        ],
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        response = response + chunk.text

    return eval(response)


def id_to_output(ids: list, user_prompt)
    
    snippets = ""
    user_prompt=user_prompt
    # iterates(by id) the projects' source code to find relevant code snippets
    for id in ids:
        source_code = supabase_table[id]["source_code"]

        def ai_code_picker(source_code, user_prompt):
            # Gemini actually picking the code

        # Appending the relevant code to snippets with project metadata
        snippets = snippets + ai_code_picker(id, user_prompt)


# print(eval(input_tag_matcher("show me projects where I used weather api", 
# """1: ["react", "flask", "spotipy"]
# 2: ["next", "javascript","openweatherAPI","react"]
# 3: ["html", "css", "javascript", "bootstrap", "tailwind"]""")))

