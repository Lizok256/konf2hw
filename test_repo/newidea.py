import os
import sys
import subprocess


def get_commit_dependencies(repo_path):
    """Получение всех коммитов и их зависимостей из git-репозитория."""
    try:
        repo = git.Repo(repo_path)
        commits = list(repo.iter_commits('main'))  # Получаем все коммиты на основной ветке
    except Exception as e:
        print(f"Ошибка при доступе к репозиторию: {e}")
        return []

    dependencies = {}
    for commit in commits:
        parent_commits = [parent.hexsha for parent in commit.parents]  # Родительские коммиты
        dependencies[commit.hexsha] = parent_commits

    return dependencies


def generate_mermaid_graph(dependencies):
    """Генерация кода Mermaid для визуализации графа зависимостей."""
    mermaid_code = 'graph TD\n'

    for commit, parents in dependencies.items():
        for parent in parents:
            mermaid_code += f'    {parent} --> {commit}\n'

    return mermaid_code


def visualize_graph(mermaid_code, mermaid_path):
    """Визуализация графа с помощью Mermaid."""
    try:
        # Создание временного файла с кодом Mermaid
        with open('graph.mmd', 'w') as f:
            f.write(mermaid_code)

        # Запуск Mermaid для генерации графа
        subprocess.run([mermaid_path, 'graph.mmd'], check=True)
    except Exception as e:
        print(f"Ошибка при визуализации графа: {e}")


def main():
    if len(sys.argv) != 3:
        print("Использование: python visualize_dependencies.py <path_to_mermaid> <path_to_repo>")
        sys.exit(1)

    mermaid_path = sys.argv[1]
    repo_path = sys.argv[2]

    if not os.path.exists(repo_path):
        print(f"Репозиторий по пути {repo_path} не найден.")
        sys.exit(1)

    # Получаем зависимости из репозитория
    dependencies = get_commit_dependencies(repo_path)

    if not dependencies:
        print("Не удалось получить зависимости из репозитория.")
        sys.exit(1)

    # Генерация графа в формате Mermaid
    mermaid_code = generate_mermaid_graph(dependencies)

    # Визуализация графа
    visualize_graph(mermaid_code, mermaid_path)

