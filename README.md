# Installation
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