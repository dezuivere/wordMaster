import google.generativeai as palm
import re
import gradio as gr
from gtts import gTTS
from dotenv import load_dotenv
import os

# to load the env variable from .env file
load_dotenv()

apiKey = os.getenv("API_KEY")

palm.configure(api_key=apiKey)

# It will select one of the model
models = [m for m in palm.list_models(
) if 'generateText' in m.supported_generation_methods]
model = models[0].name

forms = [
    "Opposite of {}: ",
    "meaning of {}: ",
    "synonyms of {}: ",
    "antonyms of {} :",
    "tense forms of {} :",
]


def genResp(text):
    completion = palm.generate_text(
        model=model,
        prompt=text,
        temperature=0,
        max_output_tokens=400  # The maximum length of the response
    )

    # Ensure the result is a string
    if isinstance(completion.result, str):
        return completion.result
    else:
        return str(completion.result)


def chatWithAI(word, forms):

    # Generate response based on word inputed
    res = re.sub(r"\n", "<br>", genResp(forms.format(word)))
    response = f'<h2>{forms.format(word)}</h2><p>{res}</p>'
    return response

# this function will convert our text response into speech


def text_to_speech(text):
    newText = text
    stars = ['**', '*']
    for star in stars:
        newText = newText.replace(star, '')

    # Remove HTML tags from the text
    icons = ['<br>', '<h2>', '<p>', '</br>', '</h2>', '</p>', '**', '*']
    for icon in icons:
        text = text.replace(icon, '')

    # Convert text to speech
    tts = gTTS(text=text, lang='en', slow=False)

    # Save the speech audio into a file
    filename = "speech.mp3"
    # every time when user inputs the input the audio file is overwrittem
    tts.save(filename)

    return filename, newText


inputs = [gr.Textbox(lines=1, label="Enter a word"), gr.Radio(
    forms, label="What Do You Want to Know?")]
outputs = [gr.Audio(
    type='filepath', label="Audio"), gr.HTML(label="response")]

# Create a Gradio interface
chatInterface = gr.Interface(
    fn=lambda x, y: text_to_speech(chatWithAI(x, y)),
    inputs=inputs,
    outputs=outputs,
    title="wordMaster",
    description=" Meet WordMaster, your go-to bot for synonyms, antonyms, and tense forms of any word. Enhance your vocabulary in a snap!",
    theme=gr.themes.Base(),
)

chatInterface.launch()
