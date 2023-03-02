import openai
import tiktoken
from rich.console import Console
from rich.markdown import Markdown
import sys

openai.organization = "org-QoDeyx1e44qC6UefQo7tgnCl"
openai.api_key_path = "API_KEY"

max_tokens = 4096


def truncate_messages(messages):
    encoding = tiktoken.get_encoding("cl100k_base")
    total_tokens = 0
    messages_trunc = []
    for m in reversed(messages):
        total_tokens += len(encoding.encode(m["content"]))
        if total_tokens > max_tokens:
            break
        messages_trunc.append(m)
    return list(reversed(messages_trunc))


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
        sys.stdout.write("Sending...")
        sys.stdout.flush()
        messages.append({"role": "user", "content": prompt})
        messages = truncate_messages(messages)
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        sys.stdout.write("\b" * len("Sending..."))
        sys.stdout.write(" " * len("Sending..."))
        sys.stdout.flush()
        msg = response["choices"][0]["message"]
        messages.append(msg)

        rendered = Markdown(msg["content"])
        console.print()
        console.print(rendered)
        console.print()