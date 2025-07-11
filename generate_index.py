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
        help="Output directory for index files (default: <input-dir>/00_index)."
    )
    return parser.parse_args()

def load_taxonomy(path):
    with open(path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def generate_toc(node, level=0):
    lines = []
    indent = "  " * level
    if isinstance(node, dict):
        for key, value in node.items():
            lines.append(f"{indent}- [[#{key}]]")
            if isinstance(value, (dict, list)):
                lines.extend(generate_toc(value, level + 1))
    elif isinstance(node, list):
        for item in node:
            if isinstance(item, dict):
                lines.extend(generate_toc(item, level))
            else:
                lines.append(f"{indent}- [[#{item}]]")
    return lines

def render_taxonomy(node, prefix='', level=2, input_folder=None):
    lines = []
    
    if isinstance(node, dict):
        for key, value in node.items():
            lines.append(f"{'#' * level} {key}")
            lines.append("[[#Index|↑ Index]]")
            lines.append("")
            tag_path = f"{prefix}/{key}".lstrip('/')
            
            lines.append('```dataview')
            lines.append('TABLE created as "Date", description as "Description", tags as "Tags"')
            lines.append(f'FROM "{input_folder}"')
            lines.append(f'WHERE contains(tags, "{tag_path}")')
            lines.append('SORT created DESC')
            lines.append('```\n')

            if isinstance(value, (dict, list)):
                lines.extend(render_taxonomy(value, tag_path, level + 1, input_folder))

    elif isinstance(node, list):
        for item in node:
            if isinstance(item, dict):
                 lines.extend(render_taxonomy(item, prefix, level, input_folder))
            else:
                lines.append(f"{'#' * level} {item}")
                lines.append("[[#Index|↑ Index]]")
                lines.append("")
                tag_path = f"{prefix}/{item}".lstrip('/')

                lines.append('```dataview')
                lines.append('TABLE created as "Date", description as "Description", tags as "Tags"')
                lines.append(f'FROM "{input_folder}"')
                lines.append(f'WHERE contains(tags, "{tag_path}")')
                lines.append('SORT created DESC')
                lines.append('```\n')
    return lines

def main():
    args = parse_args()
    tax = load_taxonomy(args.tags_file)
    if not tax:
        sys.exit(f"Empty or invalid taxonomy file: {args.tags_file}")

    output_dir = args.output or os.path.join(args.input_dir, '00_index')
    os.makedirs(output_dir, exist_ok=True)
    print(f"Index directory set to: {output_dir}")

    input_folder_name = os.path.basename(os.path.normpath(args.input_dir))

    for category, sub_node in tax.items():
        output_path = os.path.join(output_dir, f"{category}.md")
        
        header = [f"# {category}", ""]
        toc_header = ["## Index", ""]
        toc_body = generate_toc(sub_node)
        
        body = render_taxonomy(sub_node, category, 2, input_folder_name)
        
        content = '\n'.join(header + toc_header + toc_body + [""] + body)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Generated index for '{category}' at {output_path}")

if __name__ == '__main__':
    main()
