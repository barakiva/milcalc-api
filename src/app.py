from dotenv import load_dotenv
from flask import Flask, request
from openai import OpenAI
import os

app = Flask(__name__)

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


@app.route("/")
def hello_world():
    return "Hello, World!"


@app.route("/gpt")
def gpt():
    prompt = "Compose a poem that explains the concept of recursion in programming."
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a poetic assistant, skilled in explaining complex programming concepts with creative flair.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
    )
    
    response = completion.choices[0].message.content
    formatted_response = response.replace('\n', '<br>')
    # return f"<h1>GPT</h1><h2>{completion.choices[0].message['content']}</h2><p>{response}</p>"
    return f"<h1>GPT</h1><h2>{prompt}</h2><p>{formatted_response}</p>"


@app.route("/assistant", methods=["POST"])
def assistant():
    # Get the user's message from the request
    user_message = request.json["message"]

assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a personal math tutor. Write and run code to answer math questions.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4-1106-preview"
)

    # Get the assistant's response from the API response
    assistant_response = response.choices[0].text.strip()

    # Return the assistant's response
    return {"response": assistant_response}


if __name__ == "__main__":
    app.run()
