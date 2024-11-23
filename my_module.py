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
            p2 = parent.replace('^', '')
            edges.append(f'    {p2} --> {commit}')

    mermaid_graph = "graph TD\n" + "\n".join(edges)
    return mermaid_graph

def visualize_graph(mermaid_graph, mermaid_path):
    """Визуализация графа с помощью Mermaid."""
    try:
        # Создание временного файла с кодом Mermaid
        with open('graph.mmd', 'w') as f:
            f.write(mermaid_graph)
        f.close()
        # Запуск Mermaid для генерации графа
        PWD=os.getcwd()
        PP= '-i  ' + PWD + '/graph.mmd'
        CC = mermaid_path + ' ' + PP
        CC += ' -o '  + PWD + '/graph.png'

        subprocess.run([CC], check=True, shell=True,capture_output=True)
        #subprocess.run(['/mmdc -i graph.mmd']  , check=True)
    except Exception as e:
        print(f"Ошибка при визуализации графа: {e}")


def main():
    parser = argparse.ArgumentParser(description='Visualize git commit dependencies as a Mermaid graph.')
    parser.add_argument('mermaid_path', type=str, help='Path to the Mermaid visualizer')
    parser.add_argument('git_path', type=str, help='Path to the git repository')

    args = parser.parse_args()
    #print( args.git_path)
    PWD = os.getcwd()
    mermaid_graph = build_mermaid_graph(args.git_path)
    os.chdir( PWD )
    visualize_graph(mermaid_graph, args.mermaid_path)

    #mermaid_graph = build_mermaid_graph(args.git_path)

    print(mermaid_graph)


if __name__ == "__main__":
    main()