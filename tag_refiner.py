#!/usr/bin/env python3
"""
Automatically classify Obsidian notes under Clippings/ into predefined tags
and update their frontmatter with the 'tags' property via LLMs (OpenAI, Gemini, Ollama).
"""
import os
import sys
import json
import argparse
import subprocess
import yaml
from embedding_classifier import OpenAIEmbeddingProvider, GeminiEmbeddingProvider, OllamaEmbeddingProvider

def build_classification_prompts(text, tags_list):
    """
    Build system and user prompts for Obsidian note classification.
    Returns (system_prompt, user_prompt) for LLM calls.
    """
    system_prompt = (
        "You are a helpful assistant that classifies Obsidian notes into the given tags. "
        "Only output a JSON array of valid tags."
    )
    tag_lines = '\n'.join(f"- {t}" for t in tags_list)
    user_prompt = (
        f"""以下は Obsidian ノートの本文です。
タグ一覧:
{tag_lines}

出力は JSON 配列のみで、例: [\"dev/agents\",\"dev/tools\"]。
ノート本文:
{text}
"""
    )
    return system_prompt, user_prompt

def load_tags_file(path):
    """
    Load tag taxonomy from a YAML file.
    Supports:
      - A top-level list of tag strings.
      - A dict with key 'tags' mapping to a list.
      - A dict where keys are parent categories and values are lists of children;
        these will be flattened as 'parent/child'.
    """
    with open(path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    # Recursively flatten nested dict/list into hierarchical tags
    def recurse(node, prefix=""):
        if isinstance(node, dict):
            for key, value in node.items():
                new_prefix = f"{prefix}/{key}" if prefix else str(key)
                yield from recurse(value, new_prefix)
        elif isinstance(node, list):
            for item in node:
                yield from recurse(item, prefix)
        elif isinstance(node, str):
            tag = f"{prefix}/{node}" if prefix else node
            yield tag
        else:
            return
    tags = list(recurse(data))
    if not tags:
        raise ValueError(f"Invalid tags file format: {path}")
    return tags

class BaseProvider:
    def classify(self, text, tags_list):
        raise NotImplementedError

class OpenAIProvider(BaseProvider):
    def __init__(self, api_key, model=None):
        import openai
        openai.api_key = api_key
        self.openai = openai
        # Use latest high-performance model by default
        self.model = model or "gpt-4.1"

    def classify(self, text, tags_list):
        system_prompt, user_prompt = build_classification_prompts(text, tags_list)
        resp = self.openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0
        )
        content = resp.choices[0].message.content.strip()
        try:
            tags = json.loads(content)
            return [t for t in tags if t in tags_list]
        except Exception:
            print(f"Warning: failed to parse JSON response: {content}", file=sys.stderr)
            return []

class GeminiProvider(BaseProvider):
    def __init__(self, api_key, model=None):
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        self.genai = genai
        # Default to latest Gemini 2.5 Flash preview
        self.model = model or "gemini-2.5-flash-preview-05-20"

    def classify(self, text, tags_list):
        system_prompt, user_prompt = build_classification_prompts(text, tags_list)
        response = self.genai.chat.completions.create(
            model=self.model,
            messages=[
                {"author": "system", "content": system_prompt},
                {"author": "user", "content": user_prompt}
            ],
            temperature=0
        )
        content = response.choices[0].message.content.strip()
        try:
            tags = json.loads(content)
            return [t for t in tags if t in tags_list]
        except Exception:
            print(f"Warning: failed to parse JSON response: {content}", file=sys.stderr)
            return []

class OllamaProvider(BaseProvider):
    def __init__(self, model=None):
        # Default to latest Llama 4 model
        self.model = model or "llama4"

    def classify(self, text, tags_list):
        system_prompt, user_prompt = build_classification_prompts(text, tags_list)
        prompt = system_prompt + "\n" + user_prompt
        try:
            result = subprocess.run(
                ["ollama", "run", self.model, "--prompt", prompt],
                capture_output=True, check=True, text=True
            )
            content = result.stdout.strip()
            tags = json.loads(content)
            return [t for t in tags if t in tags_list]
        except subprocess.CalledProcessError as e:
            print(f"Error running ollama: {e}", file=sys.stderr)
            return []
        except Exception:
            print(f"Warning: failed to parse JSON response: {result.stdout}", file=sys.stderr)
            return []

def parse_args():
    parser = argparse.ArgumentParser(
        description="Refine Obsidian note tags using completion or embedding (OpenAI), Gemini, or Ollama."
    )
    parser.add_argument(
        "--provider",
        choices=["openai", "gemini", "ollama", "embedding"],
        default="openai",
        help=(
            "Which provider to use: openai (completion), gemini (completion), ollama (completion), "
            "or embedding (embedding-based classification). "
            "For embedding, use --embed-provider and --embed-model to select the embedding service and model."
        )
    )
    parser.add_argument(
        "--model",
        help="Model identifier for the chosen provider (for completion) or default embedding model if --embed-model is not specified."
    )
    parser.add_argument(
        "--embed-provider",
        choices=["openai", "gemini", "ollama"],
        default="openai",
        help="Embedding provider to use when --provider is 'embedding' (openai, gemini, or ollama)."
    )
    parser.add_argument(
        "--embed-model",
        help="Embedding model identifier for the chosen embedding provider. Overrides --model when embedding."
    )
    parser.add_argument(
        "--api-key",
        help="API key for OpenAI or Google (Gemini)."
    )
    parser.add_argument(
        "--input-dir",
        required=True,
        help="Directory containing markdown notes to process."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print planned updates without writing files."
    )
    parser.add_argument(
        "--tags-file",
        help="YAML file containing the tag taxonomy."
    )
    parser.add_argument(
        "--dry-run-limit",
        type=int,
        default=10,
        help="Number of files to process in dry-run mode (default: 10)."
    )
    return parser.parse_args()

def process_file(path, provider, tags_list, dry_run=False):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    if text.startswith('---'):
        parts = text.split('---', 2)
        fm_text = parts[1]
        body = parts[2]
    else:
        fm_text = ''
        body = text
    # classify based on body
    content_for_classify = body.strip()
    tags = provider.classify(content_for_classify, tags_list)
    if not tags:
        tags = ['misc/uncategorized']
    # parse existing frontmatter
    if fm_text:
        try:
            fm_dict = yaml.safe_load(fm_text) or {}
        except Exception as e:
            print(f"Warning: failed to parse YAML in {path}: {e}", file=sys.stderr)
            fm_dict = {}
    else:
        fm_dict = {}
    fm_dict['tags'] = tags
    new_fm = yaml.safe_dump(fm_dict, allow_unicode=True, sort_keys=False).strip()
    new_text = f"---\n{new_fm}\n---\n{body.lstrip()}"
    if text != new_text:
        print(f"Updating {path}: {tags}")
        if not dry_run:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_text)
        return True
    return False

def main():
    args = parse_args()
    if args.provider == 'openai':
        api_key = args.api_key or os.environ.get('OPENAI_API_KEY')
        if not api_key:
            print('Error: OpenAI API key is required.', file=sys.stderr)
            sys.exit(1)
        provider = OpenAIProvider(api_key, args.model)
    elif args.provider == 'embedding':
        embed_provider = args.embed_provider
        embed_model = args.embed_model or args.model
        if embed_provider == 'openai':
            api_key = args.api_key or os.environ.get('OPENAI_API_KEY')
            if not api_key:
                print('Error: OpenAI API key is required for embedding provider.', file=sys.stderr)
                sys.exit(1)
            provider = OpenAIEmbeddingProvider(api_key, embed_model)
        elif embed_provider == 'gemini':
            api_key = args.api_key or os.environ.get('GOOGLE_API_KEY')
            if not api_key:
                print('Error: Google API key is required for Gemini embedding provider.', file=sys.stderr)
                sys.exit(1)
            provider = GeminiEmbeddingProvider(api_key, embed_model)
        elif embed_provider == 'ollama':
            provider = OllamaEmbeddingProvider(embed_model)
        else:
            print(f"Error: unsupported embedding provider: {embed_provider}", file=sys.stderr)
            sys.exit(1)
    elif args.provider == 'gemini':
        api_key = args.api_key or os.environ.get('GOOGLE_API_KEY')
        if not api_key:
            print('Error: Google API key is required for Gemini.', file=sys.stderr)
            sys.exit(1)
        provider = GeminiProvider(api_key, args.model)
    else:
        provider = OllamaProvider(args.model)
    # Load tag taxonomy from YAML
    tags_file = args.tags_file or os.path.join(os.path.dirname(__file__), 'tags.yml')
    # Print configuration details
    print("=== Tag Refiner Configuration ===")
    print(f"Provider: {args.provider}")
    if args.provider == 'embedding':
        print(f"Embedding provider: {args.embed_provider}")
        print(f"Embedding model: {provider.model}")
    else:
        print(f"Completion model: {provider.model}")
    print(f"Tags file: {tags_file}")
    print(f"Input directory: {args.input_dir}")
    print(f"Dry-run: {args.dry_run}, Dry-run limit: {args.dry_run_limit}")
    try:
        tags_list = load_tags_file(tags_file)
    except Exception as e:
        print(f"Error loading tags file {tags_file}: {e}", file=sys.stderr)
        sys.exit(1)
    # Prepare processed-files manifest (skip already processed)
    manifest_path = os.path.join(args.input_dir, '.tag_refiner_processed')
    processed_set = set()
    if not args.dry_run and os.path.exists(manifest_path):
        with open(manifest_path, 'r', encoding='utf-8') as mf:
            processed_set = set(line.strip() for line in mf if line.strip())
    # Collect markdown files, skipping processed ones
    markdown_files = []
    for root, _, files in os.walk(args.input_dir):
        for fn in files:
            if fn.lower().endswith('.md'):
                full = os.path.join(root, fn)
                rel = os.path.relpath(full, args.input_dir)
                if not args.dry_run and rel in processed_set:
                    continue
                markdown_files.append(full)
    # If dry-run, limit to first N files
    if args.dry_run:
        count = args.dry_run_limit
        markdown_files = markdown_files[:count]
    # Process selected markdown files
    updated_rel_paths = []
    for path in markdown_files:
        updated = process_file(path, provider, tags_list, dry_run=args.dry_run)
        if updated and not args.dry_run:
            rel = os.path.relpath(path, args.input_dir)
            updated_rel_paths.append(rel)
    # Update manifest with newly processed files
    if not args.dry_run and updated_rel_paths:
        new_set = processed_set.union(updated_rel_paths)
        with open(manifest_path, 'w', encoding='utf-8') as mf:
            for rel in sorted(new_set):
                mf.write(rel + '\n')

if __name__ == '__main__':
    main()