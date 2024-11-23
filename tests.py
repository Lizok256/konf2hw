import unittest
from my_module import get_git_commits, get_commit_parents, build_mermaid_graph

class TestGitDependencyVisualizer(unittest.TestCase):

    def test_get_git_commits(self):
        # Здесь можно создать временный git-репозиторий для тестирования
        commits = get_git_commits('/Users/elizaveta/PycharmProjects/PythonProject/mermaid/Shell_Emulator')
        self.assertIsInstance(commits, list)
        self.assertGreater(len(commits), 0)

    def test_get_commit_parents(self):
        # Проверка на существующий коммит
        parents = get_commit_parents('some_commit_hash')
        self.assertIsInstance(parents, list)

    def test_build_mermaid_graph(self):
        graph = build_mermaid_graph('/Users/elizaveta/PycharmProjects/PythonProject/mermaid/Shell_Emulator')
        self.assertIn('graph TD\n', graph)

if __name__ == '__main__':
    unittest.main()