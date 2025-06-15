#!/usr/bin/env python3
"""
Generate a YAML tag taxonomy (tags.yml) from a directory of Obsidian notes.
Supports OpenAI, Google Gemini, and Ollama LLM providers via completion.
"""
import os
import sys
import argparse
import subprocess

def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate tags.yml taxonomy from Obsidian notes via LLM completion."
    )
    parser.add_argument(
        "--provider",
        choices=["openai", "gemini", "ollama"],
        default="openai",
        help="LLM provider to use for taxonomy generation."
    )
    parser.add_argument(
        "--model",
        help="Model identifier (e.g., gpt-4.1, gemini-2.5-flash-preview-05-20, llama4)."
    )
    parser.add_argument(
        "--api-key",
        help="API key for OpenAI or Google Gemini."
    )
    parser.add_argument(
        "--input-dir",
        required=True,
        help="Directory containing Obsidian markdown notes."
    )
    parser.add_argument(
        "--output",
        default="tags.yml",
        help="Output file path for generated taxonomy YAML."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print generated taxonomy to stdout without writing file."
    )
    return parser.parse_args()

def collect_titles(input_dir):
    """Collect first-line titles (or filenames) from markdown files."""
    titles = []
    for root, _, files in os.walk(input_dir):
        for fn in files:
            if fn.lower().endswith('.md'):
                path = os.path.join(root, fn)
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        first = f.readline().strip()
                except Exception:
                    first = ''
                title = first.lstrip('# ').strip() or os.path.splitext(fn)[0]
                titles.append(title)
    return titles

def build_prompt(titles_list):
    """Build system and user prompts for taxonomy generation."""
    system_prompt = (
        "You are an expert AI taxonomy designer. "
        "Group the following note titles into a hierarchical tag taxonomy and output it as YAML."
    )
    items = '\n'.join(f"- {t}" for t in titles_list)
    user_prompt = (
        f"""Here is a list of Obsidian note titles:
{items}

Please categorize them into parent/child tags. Output only valid YAML mapping. Example:
category:
  - subtag1
  - subtag2
"""
    )
    return system_prompt, user_prompt

def main():
    args = parse_args()
    titles = collect_titles(args.input_dir)
    if not titles:
        sys.exit("No markdown files found in input directory.")
    system_prompt, user_prompt = build_prompt(titles)

    taxonomy = None
    if args.provider == 'openai':
        try:
            import openai
        except ImportError:
            sys.exit("Error: openai package required for provider=openai.")
        openai.api_key = args.api_key or os.getenv('OPENAI_API_KEY')
        if not openai.api_key:
            sys.exit('Error: OPENAI_API_KEY is not set.')
        model = args.model or 'gpt-4.1'
        resp = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0
        )
        taxonomy = resp.choices[0].message.content
    elif args.provider == 'gemini':
        try:
            import google.generativeai as genai
        except ImportError:
            sys.exit("Error: google-generativeai package required for provider=gemini.")
        key = args.api_key or os.getenv('GOOGLE_API_KEY')
        if not key:
            sys.exit('Error: GOOGLE_API_KEY is not set.')
        genai.configure(api_key=key)
        model = args.model or 'gemini-2.5-flash-preview-05-20'
        resp = genai.chat.completions.create(
            model=model,
            messages=[
                {"author": "system", "content": system_prompt},
                {"author": "user", "content": user_prompt}
            ],
            temperature=0
        )
        taxonomy = resp.choices[0].message.content
    else:
        model = args.model or 'llama4'
        full_prompt = system_prompt + "\n" + user_prompt
        try:
            result = subprocess.run(
                ["ollama", "run", model, "--prompt", full_prompt],
                capture_output=True, check=True, text=True
            )
            taxonomy = result.stdout
        except subprocess.CalledProcessError as e:
            sys.exit(f"Error running ollama: {e}")

    if not taxonomy:
        sys.exit('Error: received empty taxonomy from LLM.')

    if args.dry_run:
        print(taxonomy)
    else:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(taxonomy)
        print(f"Generated taxonomy saved to {args.output}")

if __name__ == '__main__':
    main()