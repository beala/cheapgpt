from typing import Callable

import openai
import tiktoken
from rich.console import Console
from rich.markdown import Markdown
import sys

openai.organization = "org-QoDeyx1e44qC6UefQo7tgnCl"
openai.api_key_path = "API_KEY"

max_tokens = 4096 - 100  # 4096 is the max, but our token count is off by a bit.

SYSTEM_MESSAGE = {"role": "system", "content": "You are a helpful assistant."}

expansions = {
    "rw": "Rewrite the following to be more concise and less wordy. Aim for clarity.\n\n",
    "conf": "When answering the following question, annotate all statements with a confidence score from 0 to 10. 0 "
            "means you are completely unsure, 10 means you are completely sure. Please be honest and think step by "
            "step.\n\n",
    "sbs": "Think step by step.",
    "clear": "Clear the chat history.",
}

def truncate_messages(messages):
    encoding = tiktoken.get_encoding("cl100k_base")
    total_tokens = 0
    messages_trunc = []
    # https://github.com/openai/openai-cookbook/blob/main/examples/How_to_count_tokens_with_tiktoken.ipynb
    for m in reversed(messages):
        this_message = 4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
        for key, value in m.items():
            this_message += len(encoding.encode(value))
            if key == "name":  # if there's a name, the role is omitted
                this_message += -1  # role is always required and always 1 token

        if total_tokens + this_message > max_tokens:
            break
        total_tokens += this_message
        messages_trunc.append(m)
    return list(reversed(messages_trunc)), total_tokens


def three_same(s: str) -> bool:
    return len(s) == 3 and s[0] == s[1] == s[2]


def multiline_input(console: Console) -> str:
    line = console.input("[bold cyan]>>>[/bold cyan] ")
    if not three_same(line):
        return line
    end = line
    lines = []
    while True:
        line = console.input()
        if line != end:
            lines.append(line)
        else:
            break
    text = '\n'.join(lines)
    return text


def expand_magic_strings(s: str) -> str:
    for key, value in expansions.items():
        s = s.replace(f"%{key}%", value)
    return s


def print_temporary(msg: str) -> Callable:
    sys.stdout.write(msg)
    sys.stdout.flush()
    def erase():
        sys.stdout.write("\b" * len(msg))
        sys.stdout.write(" " * len(msg))
        sys.stdout.flush()
    return erase


if __name__ == "__main__":
    # readline.parse_and_bind("set editing-mode vi")
    messages = [SYSTEM_MESSAGE]
    console = Console(soft_wrap=True)
    while True:
        prompt = multiline_input(console)
        if prompt == "%":
            for key, value in expansions.items():
                console.print(f"%{key}%: {repr(value)}")
            continue
        if prompt == "%clear%":
            messages = [SYSTEM_MESSAGE]
            continue

        prompt = expand_magic_strings(prompt)
        messages.append({"role": "user", "content": prompt})
        messages, total_tokens = truncate_messages(messages)
        erase = print_temporary(f"Sending {total_tokens} tokens...")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        erase()
        msg = response["choices"][0]["message"].to_dict()
        messages.append(msg)

        rendered = Markdown(msg["content"])
        console.print()
        console.print(rendered)
        console.print()