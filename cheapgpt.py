import openai
import tiktoken
from rich.console import Console
from rich.markdown import Markdown
import sys

openai.organization = "org-QoDeyx1e44qC6UefQo7tgnCl"
openai.api_key_path = "API_KEY"

max_tokens = 4096 - 200  # 4096 is the max, but our token count is off by a bit.


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


if __name__ == "__main__":
    # readline.parse_and_bind("set editing-mode vi")
    messages = [{"role": "system", "content": "You are a helpful assistant."}]
    console = Console()
    while True:
        prompt = multiline_input(console)
        messages.append({"role": "user", "content": prompt})
        messages, total_tokens = truncate_messages(messages)
        status_msg = f"Sending {total_tokens} tokens..."
        sys.stdout.write(status_msg)
        sys.stdout.flush()
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        sys.stdout.write("\b" * len(status_msg))
        sys.stdout.write(" " * len(status_msg))
        sys.stdout.flush()
        msg = response["choices"][0]["message"].to_dict()
        messages.append(msg)

        rendered = Markdown(msg["content"])
        console.print()
        console.print(rendered)
        console.print()