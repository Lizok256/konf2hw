import subprocess
import argparse
import os


def get_commits(repo_path):
    os.chdir(repo_path)  # Переходим в папку репозитория
    result = subprocess.run(['git', 'rev-list', '--all'], capture_output=True, text=True)
    commits = result.stdout.splitlines()
    return commits


def get_dependencies(repo_path, commit_hash):
    try:
        result = subprocess.run(['git', 'show', '--pretty=format:%h', commit_hash], capture_output=True, text=True)
        return result.stdout.splitlines()
    except Exception as e:
        print(f"Ошибка получения зависимостей для коммита {commit_hash}: {e}")
        return []


def generate_mermaid_graph(repo_path):
    commits = get_commits(repo_path)
    mermaid_graph = "graph TD;n"

    # Создаем узлы для каждого коммита
    for commit in commits:
        mermaid_graph += f"    {commit}({commit})n"

    # Добавляем зависимостей (здесь можно добавить свою логику получения зависимостей)
    for commit in commits:
        dependencies = get_dependencies(repo_path, commit)
        for dep in dependencies:
            mermaid_graph += f"    {dep} --> {commit}n"

    return mermaid_graph


def visualize_graph(mermaid_graph, visualizer_path):
    with open("graph.mmd", "w") as f:
        f.write(mermaid_graph)
    subprocess.run([visualizer_path, "graph.mmd"])  # Здесь запускаем визуализатор


def main():
    parser = argparse.ArgumentParser(description='Visualize git commit dependencies as a Mermaid graph.')
    parser.add_argument('visualizer_path', help='Path to the graph visualization tool.')
    parser.add_argument('repo_path', help='Path to the git repository.')

    args = parser.parse_args()

    mermaid_graph = generate_mermaid_graph(args.repo_path)
    visualize_graph(mermaid_graph, args.visualizer_path)


if __name__ == "__main__":
    main()