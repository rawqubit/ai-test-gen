import os
import click
from openai import OpenAI
from rich.console import Console
from rich.markdown import Markdown

# Initialize OpenAI client
client = OpenAI()
console = Console()

@click.command()
@click.argument('file_path', type=click.Path(exists=True))
@click.option('--framework', default='pytest', help='Testing framework (e.g., pytest, unittest).')
def test_gen(file_path, framework):
    """AI-powered unit test generator for code files."""
    with open(file_path, 'r') as f:
        code = f.read()

    console.print(f"[bold blue]Generating {framework} tests for {file_path}...[/bold blue]")

    prompt = f"""
    Generate basic unit tests for the following code using the {framework} framework.
    Format your response in Markdown.

    Code:
    ```{os.path.splitext(file_path)[1][1:]}
    {code}
    ```
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {{"role": "system", "content": "You are an expert software tester."}},
                {{"role": "user", "content": prompt}}
            ]
        )
        test_text = response.choices[0].message.content
        console.print(Markdown(test_text))
    except Exception as e:
        console.print(f"[bold red]Error during test generation:[/bold red] {e}")

if __name__ == '__main__':
    test_gen()
