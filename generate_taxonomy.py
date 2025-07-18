#!/usr/bin/env python3
"""
Generate a YAML tag taxonomy (tags.yml) from a directory of Obsidian notes.
Supports OpenAI, Google Gemini, and Ollama LLM providers via completion.
"""
import os
import sys
from datetime import date
import argparse
import subprocess
import yaml
import numpy as np
from sklearn.cluster import KMeans
from embedding_classifier import OpenAIEmbeddingProvider, GeminiEmbeddingProvider, OllamaEmbeddingProvider

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
        help="Output file path for generated taxonomy YAML."
        " If unspecified, defaults to tags_YYMMDD.yml."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print generated taxonomy to stdout without writing file."
    )
    parser.add_argument(
        "--depth",
        type=int,
        default=3,
        help="Maximum depth of taxonomy hierarchy (default: 3)."
    )
    parser.add_argument(
        "--use-embedding",
        action="store_true",
        help="Use embedding-based clustering to summarize note titles before taxonomy generation."
    )
    parser.add_argument(
        "--embed-provider",
        choices=["openai", "gemini", "ollama"],
        default="openai",
        help="Embedding provider for summarization (default: openai)."
    )
    parser.add_argument(
        "--embed-model",
        help="Embedding model identifier for summarization (overrides default)."
    )
    parser.add_argument(
        "--clusters",
        type=int,
        default=10,
        help="Number of clusters to form for title summarization (default: 10)."
    )
    return parser.parse_args()

def collect_titles(input_dir):
    """Collect first-line titles (or filenames) from markdown files."""
    titles = []
    for root, _, files in os.walk(input_dir):
        for fn in files:
            # Skip hidden files and dotfiles
            if fn.startswith('.'):
                continue
            if fn.lower().endswith('.md'):
                path = os.path.join(root, fn)
                # Extract first meaningful line (skip YAML frontmatter '---')
                title = ''
                try:
                    with open(path, 'r', encoding='utf-8') as f:
                        for line in f:
                            text = line.strip()
                            if not text or text.startswith('---'):
                                continue
                            title = text.lstrip('# ').strip()
                            break
                except Exception:
                    title = ''
                # Fallback to filename without extension
                if not title:
                    title = os.path.splitext(fn)[0]
                titles.append(title)
    return titles

def build_prompt(titles_list, depth):
    """Build system and user prompts for taxonomy generation with max depth."""
    # Japanese prompt: generate taxonomy in Japanese without titles
    system_prompt = (
        f"あなたは優れたAIタクソノミー設計者です。以下のObsidianノートタイトル一覧をもとに、"
        f"最大{depth}階層のカテゴリ/サブカテゴリを日本語で生成し、YAML形式で出力してください。"
        "不要な説明やタイトルは含めず、YAMLマッピングのみを返してください。"
    )
    items = '\n'.join(f"- {t}" for t in titles_list)
    user_prompt = (
        f"ノートタイトル一覧:\n{items}\n\n"
        "上記のタイトルをもとに、日本語のカテゴリ/サブカテゴリ階層を生成してください。"
        "出力はYAMLマッピングのみで、カテゴリごとにサブカテゴリのリストを示してください。"
    )
    return system_prompt, user_prompt

def main():
    args = parse_args()
    titles = collect_titles(args.input_dir)
    if not titles:
        sys.exit("No markdown files found in input directory.")
    # Optionally summarize titles via embedding clustering
    if args.use_embedding:
        # Initialize embedding provider
        if args.embed_provider == 'openai':
            emb = OpenAIEmbeddingProvider(args.api_key or os.getenv('OPENAI_API_KEY'), args.embed_model)
        elif args.embed_provider == 'gemini':
            emb = GeminiEmbeddingProvider(args.api_key or os.getenv('GOOGLE_API_KEY'), args.embed_model)
        else:
            emb = OllamaEmbeddingProvider(args.embed_model)
        # Embed titles
        emb.load_tags(titles)
        embs = np.array(emb.tag_embeddings)
        # Cluster embeddings
        n_clusters = min(args.clusters, len(titles))
        try:
            kmeans = KMeans(n_clusters=n_clusters, random_state=0)
            labels = kmeans.fit_predict(embs)
        except Exception as e:
            sys.exit(f"Error during clustering: {e}")
        # Select representative title per cluster (closest to centroid)
        rep_titles = []
        for ci in range(n_clusters):
            idxs = [i for i, lbl in enumerate(labels) if lbl == ci]
            if not idxs:
                continue
            centroid = kmeans.cluster_centers_[ci]
            # find index with minimal distance to centroid
            dists = [np.linalg.norm(embs[i] - centroid) for i in idxs]
            rep_idx = idxs[int(np.argmin(dists))]
            rep_titles.append(titles[rep_idx])
        print(f"Summarized {len(titles)} titles into {len(rep_titles)} representatives.")
        titles = rep_titles
    # Build prompts for taxonomy generation
    system_prompt, user_prompt = build_prompt(titles, args.depth)

    taxonomy = None
    if args.provider == 'openai':
        try:
            import openai
        except ImportError:
            sys.exit("Error: openai package required for provider=openai.")
        openai.api_key = args.api_key or os.getenv('OPENAI_API_KEY')
        if not openai.api_key:
            sys.exit('Error: OPENAI_API_KEY is not set.')
        # Default to cost-effective o4-mini model
        model = args.model or 'o4-mini'
        # Use new OpenAI chat completion API
        resp = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0,
            max_tokens=2048
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
            temperature=0,
            max_output_tokens=2048
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
        # Determine output path with timestamp if not specified
        output_path = args.output
        if not output_path:
            today = date.today().strftime("%y%m%d")
            output_path = f"tags_{today}.yml"
        # Write taxonomy to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(taxonomy)
        print(f"Generated taxonomy saved to {output_path}")

if __name__ == '__main__':
    main()