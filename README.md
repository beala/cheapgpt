A python script for interacting with [ChatGPT over the API](https://openai.com/blog/introducing-chatgpt-and-whisper-apis). Possibly cheaper than ChatGPT Plus.

https://user-images.githubusercontent.com/455163/222349511-fc2690e6-00d1-4585-bd02-c6032d61fffd.mov

Start a prompt with three of the same character (eg, `"""` but can be any character) to start multiline input. End the prompt by repeating those same characters on their own line.

# Setup
Set up a virtualenv and install the python dependencies:
```shell
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a file called `API_KEY` with your API key in it.
```shell
echo your_key_goes_here > ~/.openai_key
```

In `cheapgpt.py`, set `openai.organization` to your organization ID.
