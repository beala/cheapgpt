A python script for interacting with [ChatGPT over the API](https://openai.com/blog/introducing-chatgpt-and-whisper-apis). Possibly cheaper than ChatGPT Plus.

<img width="843" alt="Screenshot 2023-03-01 at 11 21 45 PM" src="https://user-images.githubusercontent.com/455163/222347451-6d5743e1-ace0-4441-aa40-5b67f599602b.png">

# Setup
Set up a virtualenv and install the python dependencies:
```shell
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create a file called `API_KEY` with your API key in it.
```shell
echo your_key_goes_here > API_KEY
```

In `cheapgpt.py`, set `openai.organization` to your organization ID.
