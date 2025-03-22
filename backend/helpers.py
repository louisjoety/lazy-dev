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



def ai_code_picker(source_code, user_prompt):
    response1 = ""
        
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.0-flash"
    contents = [
               
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=f"user_prompt: {user_prompt}\nsource code: {source_code}"),
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
            types.Part.from_text(text="""CONTEXT: You are an expert code analyser, specialized in extracting sections of code from larger source code

INSTRUCTIONS: You will be given a .txt file containing all the source code of the project. The code for each file is encompassed within HTML style tags containing filename. For example, the code of index.html is enclosed within <index.html> and </index.html>. You will be given the user prompt and you need to select the lines of code that is relevant to what the user is asking. It does not have to contain exactly the same thing but it could be its applications too.

RESPONSE FORMAT: return in json format like this {filename: relevant code snippets}. Ensure there is only one \"filename:\" for the snippets from the same file.

example input:<template.html>
<!DOCTYPE html>
<html lang=\"en\">
<head>
<meta charset=\"UTF-8\" />
<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\" />
<title>Quotes of the day</title>

<style>
    *,
    *::before,
    *::after {
    box-sizing: border-box;
    }

    html {
    font-family: sans-serif;
    line-height: 1.15;
    -webkit-text-size-adjust: 100%;
    -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
    }

    article, aside, figcaption, figure, footer, header, hgroup, main, nav, section {
    display: block;
    }

    h1 {
    margin-top: 0;
    margin-bottom: 30px;
    }

    p {
    margin-top: 0;
    margin-bottom: 1rem;
    }

    footer {
    margin-bottom: 10px;
    }

    body {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, \"Segoe UI\", Roboto, \"Helvetica Neue\", Arial, \"Noto Sans\", \"Liberation Sans\", sans-serif, \"Apple Color Emoji\", \"Segoe UI Emoji\", \"Segoe UI Symbol\", \"Noto Color Emoji\";
    font-size: 1rem;
    font-weight: 400;
    line-height: 1.5;
    color: #212529;
    text-align: left;
    background-color: #fff;
    }

    .container-fluid {
    width: 100%;
    padding-right: 15px;
    padding-left: 15px;
    margin-right: auto;
    margin-left: auto;
    margin-bottom: 30px;
    display: -ms-flexbox;
    display: flex;
    -ms-flex-wrap: wrap;
    flex-wrap: wrap;
    -ms-flex-align: center;
    align-items: center;
    -ms-flex-pack: justify;
    justify-content: space-between;
    }

    .card {
    position: relative;
    display: -ms-flexbox;
    display: flex;
    -ms-flex-direction: column;
    flex-direction: column;
    min-width: 0;
    word-wrap: break-word;
    background-color: #fff;
    background-clip: border-box;
    border: 1px solid rgba(0, 0, 0, 0.125);
    border-radius: 0.25rem;
    }

    .card-header {
    padding: 0.75rem 1.25rem;
    margin-bottom: 0;
    background-color: rgba(0, 0, 0, 0.03);
    border-bottom: 1px solid rgba(0, 0, 0, 0.125);
    }

    .card-header:first-child {
    border-radius: 0.1875rem 0.1875rem 0 0;
    }

    .card-body {
    -ms-flex: 1 1 auto;
    flex: 1 1 auto;
    min-height: 1px;
    padding: 1.25rem;
    }

    blockquote {
    margin: 0 0 1rem;
    }

    .blockquote {
    margin-bottom: 1rem;
    font-size: 1.25rem;
    }

    .blockquote-footer {
    display: block;
    font-size: 0.875em;
    color: #6c757d;
    }

    .blockquote-footer::before {
    content: \"\\2014\\00A0\";
    }

    .mb-0 {
    margin-bottom: 0 !important;
    }

    .blockquote-footer::before {
    content: \"\\2014\\00A0\";
    }

</style>
</head>
<body>
<header>
    <h1>Hello {{ name }}. These are your quotes for today.</h1>
</header>
<main>
    {% for item in collection %}
    <div class=\"container-fluid\">
        <div class=\"card\">          
        <div class=\"card-body\">
            <blockquote class=\"blockquote mb-0\">         
            <footer class=\"blockquote-footer\">
            <b>{{ item.author }} in <cite title=\"Source Title\">{{ item.title }}</cite></b>
            </footer>
            <p>\"{{ item.quote }}\"</p>
            </blockquote>
        </div>
        </div>
    </div>
    {% endfor %}
</main>
</body>
</html>
</template.html>

<readwise.py>
import csv, random, smtplib
from jinja2 import Template
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()

# Declaring important variables
NO_OF_QUOTES = 2
collection_of_quotes = []
name = \"{Your Name}\"                              # Change your name
sender_email = os.getenv(\"SENDER_EMAIL\")
app_password = os.getenv(\"GOOGLE_APP_PASSWORD\")   # This is the 16 character app password from Google account
receiver_email = os.getenv(\"RECEIVER_EMAIL\")

# Opening the csv file where highlights are stored, and appending all the highlights in the file to a list
with open('highlights.csv', encoding='utf-8') as csvFileObj:
    csvReader = csv.reader(csvFileObj)
    rows = []
    for row in csvReader:
        rows.append(row)

# Appends a certain number of quotes randomly selected from the list of quotes to a list. The quotes are stored as a dictionary containing title, author, and quote
for item in random.sample(rows, NO_OF_QUOTES):
    collection_of_quotes.append({\"title\": item[1], \"author\": item[2], \"quote\": item[4]})

context = {\"name\": name, \"collection\": collection_of_quotes, \"subject\": \"Quotes of the day\"}

with open(\"templates\\\\template.html\", 'r') as f:
    template = Template(f.read())

# Generating the HTML file
html_file = template.render(context)

html_message = EmailMessage()
html_message[\"Subject\"] = context['subject']
html_message[\"From\"] = sender_email
html_message[\"To\"] = receiver_email
html_message.add_alternative(html_file, subtype=\"html\")

# Sending the email
with smtplib.SMTP_SSL(\"smtp.gmail.com\", 465) as server:
    server.login(sender_email, app_password)
    server.send_message(html_message)

exit()
</readwise.py>

<README.md>
# Readwise quotes emailer
A script to send yourself daily emails containing quotes from your kindle highlights. The script can be run locally using windows task scheduler, or hosted remotely. 
## Step 1
Transfer the \"My Clippings.txt\" file from your kindle to your laptop.

## Step 2
Convert the text file to a csv file [here](https://kindle.brendantrinh.com/).

## Step 3
Move the csv file to the same directory as the python script.

## Step 4
Use windows task scheduler or any task scheduler to run the script daily. Alternatively, host the script on the cloud so you can receive emails when your computer is inactive.
</README.md>

<.gitignore>
.env
<.gitignore>

user prompt: Show me where I used csv library

sample output: readwise.py: 
import csv, random, smtplib

# Opening the csv file where highlights are stored, and appending all the highlights in the file to a list
with open('highlights.csv', encoding='utf-8') as csvFileObj:
    csvReader = csv.reader(csvFileObj)
    rows = []
    for row in csvReader:
        rows.append(row)
"""),
        ],
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        response1 = response1 + chunk.text

    return eval(response1[8:-4])

print(ai_code_picker("""<template.html>
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Quotes of the day</title>

  <style>
    *,
    *::before,
    *::after {
      box-sizing: border-box;
    }

    html {
      font-family: sans-serif;
      line-height: 1.15;
      -webkit-text-size-adjust: 100%;
      -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
    }

    article, aside, figcaption, figure, footer, header, hgroup, main, nav, section {
      display: block;
    }

    h1 {
      margin-top: 0;
      margin-bottom: 30px;
    }

    p {
      margin-top: 0;
      margin-bottom: 1rem;
    }

    footer {
      margin-bottom: 10px;
    }

    body {
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans", "Liberation Sans", sans-serif, "Apple Color Emoji", "Segoe UI Emoji", "Segoe UI Symbol", "Noto Color Emoji";
      font-size: 1rem;
      font-weight: 400;
      line-height: 1.5;
      color: #212529;
      text-align: left;
      background-color: #fff;
    }

    .container-fluid {
      width: 100%;
      padding-right: 15px;
      padding-left: 15px;
      margin-right: auto;
      margin-left: auto;
      margin-bottom: 30px;
      display: -ms-flexbox;
      display: flex;
      -ms-flex-wrap: wrap;
      flex-wrap: wrap;
      -ms-flex-align: center;
      align-items: center;
      -ms-flex-pack: justify;
      justify-content: space-between;
    }

    .card {
      position: relative;
      display: -ms-flexbox;
      display: flex;
      -ms-flex-direction: column;
      flex-direction: column;
      min-width: 0;
      word-wrap: break-word;
      background-color: #fff;
      background-clip: border-box;
      border: 1px solid rgba(0, 0, 0, 0.125);
      border-radius: 0.25rem;
    }

    .card-header {
      padding: 0.75rem 1.25rem;
      margin-bottom: 0;
      background-color: rgba(0, 0, 0, 0.03);
      border-bottom: 1px solid rgba(0, 0, 0, 0.125);
    }

    .card-header:first-child {
      border-radius: 0.1875rem 0.1875rem 0 0;
    }

    .card-body {
      -ms-flex: 1 1 auto;
      flex: 1 1 auto;
      min-height: 1px;
      padding: 1.25rem;
    }

    blockquote {
      margin: 0 0 1rem;
    }

    .blockquote {
      margin-bottom: 1rem;
      font-size: 1.25rem;
    }

    .blockquote-footer {
      display: block;
      font-size: 0.875em;
      color: #6c757d;
    }

    .blockquote-footer::before {
      content: "\2014\00A0";
    }

    .mb-0 {
      margin-bottom: 0 !important;
    }

    .blockquote-footer::before {
      content: "\2014\00A0";
    }

  </style>
</head>
<body>
  <header>
    <h1>Hello {{ name }}. These are your quotes for today.</h1>
  </header>
  <main>
    {% for item in collection %}
      <div class="container-fluid">
        <div class="card">          
          <div class="card-body">
            <blockquote class="blockquote mb-0">         
              <footer class="blockquote-footer">
              <b>{{ item.author }} in <cite title="Source Title">{{ item.title }}</cite></b>
              </footer>
              <p>"{{ item.quote }}"</p>
            </blockquote>
          </div>
        </div>
      </div>
    {% endfor %}
  </main>
</body>
</html>
</template.html>

<readwise.py>
import csv, random, smtplib
from jinja2 import Template
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()

# Declaring important variables
NO_OF_QUOTES = 2
collection_of_quotes = []
name = "{Your Name}"                              # Change your name
sender_email = os.getenv("SENDER_EMAIL")
app_password = os.getenv("GOOGLE_APP_PASSWORD")   # This is the 16 character app password from Google account
receiver_email = os.getenv("RECEIVER_EMAIL")

# Opening the csv file where highlights are stored, and appending all the highlights in the file to a list
with open('highlights.csv', encoding='utf-8') as csvFileObj:
    csvReader = csv.reader(csvFileObj)
    rows = []
    for row in csvReader:
        rows.append(row)

# Appends a certain number of quotes randomly selected from the list of quotes to a list. The quotes are stored as a dictionary containing title, author, and quote
for item in random.sample(rows, NO_OF_QUOTES):
    collection_of_quotes.append({"title": item[1], "author": item[2], "quote": item[4]})

context = {"name": name, "collection": collection_of_quotes, "subject": "Quotes of the day"}

with open("templates\\template.html", 'r') as f:
    template = Template(f.read())

# Generating the HTML file
html_file = template.render(context)

html_message = EmailMessage()
html_message["Subject"] = context['subject']
html_message["From"] = sender_email
html_message["To"] = receiver_email
html_message.add_alternative(html_file, subtype="html")

# Sending the email
with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
    server.login(sender_email, app_password)
    server.send_message(html_message)

exit()
</readwise.py>

<README.md>
# Readwise quotes emailer
A script to send yourself daily emails containing quotes from your kindle highlights. The script can be run locally using windows task scheduler, or hosted remotely. 
## Step 1
Transfer the "My Clippings.txt" file from your kindle to your laptop.

## Step 2
Convert the text file to a csv file [here](https://kindle.brendantrinh.com/).

## Step 3
Move the csv file to the same directory as the python script.

## Step 4
Use windows task scheduler or any task scheduler to run the script daily. Alternatively, host the script on the cloud so you can receive emails when your computer is inactive.
</README.md>

<.gitignore>
.env
<.gitignore>""", "show me where i used csv library"))