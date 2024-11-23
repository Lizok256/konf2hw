import os
import subprocess
import argparse


def get_git_commits(repo_path):
    """Получает список коммитов в указанном репозитории."""
    os.chdir(repo_path)
    result = subprocess.run(['git', 'log', '--pretty=format:%H'], capture_output=True, text=True)
    return result.stdout.splitlines()


def get_commit_parents(commit_hash):
    """Получает хеши родительских коммитов для данного коммита."""
    result = subprocess.run(['git', 'rev-parse', f'{commit_hash}^'], capture_output=True, text=True)
    parents = result.stdout.strip().splitlines()
    return parents


def build_mermaid_graph(repo_path):
    """Строит граф зависимостей в формате Mermaid."""
    commits = get_git_commits(repo_path)
    edges = []

    for commit in commits:
        parents = get_commit_parents(commit)
        for parent in parents:
            edges.append(f'    {parent} --> {commit}')

    mermaid_graph = "graph TD;\n" + "\n".join(edges)
    return mermaid_graph


def main():
    parser = argparse.ArgumentParser(description='Visualize git commit dependencies as a Mermaid graph.')
    parser.add_argument('visualizer_path', type=str, help='Path to the Mermaid visualizer')
    parser.add_argument('repo_path', type=str, help='Path to the git repository')

    args = parser.parse_args()

    mermaid_graph = build_mermaid_graph(args.repo_path)

    print(mermaid_graph)


if __name__ == "__main__":
    main()