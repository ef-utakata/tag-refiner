#!/usr/bin/env python3
"""
Generate an Obsidian note with Dataview index for notes by taxonomy categories.
"""
import os
import sys
import argparse
import yaml

def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate an index note with Dataview blocks for each taxonomy category."
    )
    parser.add_argument(
        "--tags-file",
        default="tags.yml",
        help="YAML file defining tag taxonomy."
    )
    parser.add_argument(
        "--input-dir",
        required=True,
        help="Directory containing categorized markdown notes."
    )
    parser.add_argument(
        "--output",
        help="Output index markdown file path (default: <input-dir>/Index.md)."
    )
    return parser.parse_args()

def load_taxonomy(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def render_taxonomy(node, prefix='', level=2, input_folder=None):
    lines = []
    for key, value in node.items() if isinstance(node, dict) else []:
        # heading
        lines.append(f"{'#' * level} {key}")
        # dataview block for this tag path
        tag_path = f"{prefix}/{key}".lstrip('/')
        folder = input_folder or ''
        lines.append('```dataview')
        # List Title, author, created, description, source from frontmatter
        # Show frontmatter fields; Dataview always displays file name by default
        lines.append('table author as Author, created as Created, description as Description, source as Source')
        if folder:
            lines.append(f'from "{folder}"')
        lines.append(f'where contains(tags, "{tag_path}")')
        lines.append('```')
        # recurse for children
        if isinstance(value, dict):
            # recurse into nested dict categories
            lines += render_taxonomy(value, tag_path, level+1, input_folder)
        elif isinstance(value, list):
            # for each subcategory, render a Dataview block
            for sub in value:
                lines.append(f"{'#' * (level+1)} {sub}")
                leaf = f"{tag_path}/{sub}"
                lines.append('```dataview')
                lines.append('table author as Author, created as Created, description as Description, source as Source')
                if folder:
                    lines.append(f'from "{folder}"')
                lines.append(f'where contains(tags, "{leaf}")')
                lines.append('```')
    return lines

def main():
    args = parse_args()
    tax = load_taxonomy(args.tags_file)
    if not tax:
        sys.exit(f"Empty or invalid taxonomy file: {args.tags_file}")
    # Determine output path
    out = args.output
    if not out:
        out = os.path.join(args.input_dir, 'Index.md')
    # Determine folder name for Dataview 'from'
    folder = os.path.basename(os.path.normpath(args.input_dir))
    # Build lines
    header = ["# Notes Index by Tag", "", f"Generated from {args.tags_file}", ""]
    body = render_taxonomy(tax, '', 2, folder)
    content = '\n'.join(header + body)
    with open(out, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Index note generated at {out}")

if __name__ == '__main__':
    main()