"""
Casos de teste para a To-Do List Application.
Utiliza unittest — compatível com o plugin JUnit do Jenkins.
"""

import unittest
from todo import TodoList


class TestAddTask(unittest.TestCase):
    """Testes para o método add_task"""

    def setUp(self):
        self.todo = TodoList()

    # Caso de Teste 1 
    def test_add_task_returns_correct_fields(self):
        """CT-01: Adicionar tarefa válida deve retornar dict com campos corretos."""
        result = self.todo.add_task("Comprar leite")

        self.assertEqual(result["id"], 1)
        self.assertEqual(result["description"], "Comprar leite")
        self.assertFalse(result["completed"])

    # Caso de Teste 2 
    def test_add_task_increments_id(self):
        """CT-02: IDs devem ser incrementados a cada nova tarefa."""
        t1 = self.todo.add_task("Tarefa A")
        t2 = self.todo.add_task("Tarefa B")
        t3 = self.todo.add_task("Tarefa C")

        self.assertEqual(t1["id"], 1)
        self.assertEqual(t2["id"], 2)
        self.assertEqual(t3["id"], 3)

    # Caso de Teste 3 
    def test_add_task_empty_raises_value_error(self):
        """CT-03: Tarefa com string vazia deve lançar ValueError."""
        with self.assertRaises(ValueError):
            self.todo.add_task("")

    # Caso de Teste 4
    def test_add_task_whitespace_raises_value_error(self):
        """CT-04: Tarefa apenas com espaços deve lançar ValueError."""
        with self.assertRaises(ValueError):
            self.todo.add_task("   ")

    # Caso de Teste 5
    def test_add_task_strips_whitespace(self):
        """CT-05: Tarefa com espaços nas bordas deve ser salva sem eles."""
        result = self.todo.add_task("  Estudar Jenkins  ")
        self.assertEqual(result["description"], "Estudar Jenkins")


class TestCompleteTask(unittest.TestCase):
    """Testes para o método complete_task"""

    def setUp(self):
        self.todo = TodoList()
        self.todo.add_task("Ler documentação")
        self.todo.add_task("Fazer deploy")

    # Caso de Teste 6
    def test_complete_task_marks_as_completed(self):
        """CT-06: Concluir tarefa existente deve setar completed=True."""
        result = self.todo.complete_task(1)
        self.assertTrue(result["completed"])

    # Caso de Teste 7 
    def test_complete_task_invalid_id_raises_value_error(self):
        """CT-07: ID inexistente deve lançar ValueError."""
        with self.assertRaises(ValueError):
            self.todo.complete_task(999)

    # Caso de Teste 8
    def test_complete_task_only_affects_target(self):
        """CT-08: Concluir tarefa 1 não deve alterar tarefa 2."""
        self.todo.complete_task(1)
        all_tasks = self.todo.get_all_tasks()
        task_2 = next(t for t in all_tasks if t["id"] == 2)
        self.assertFalse(task_2["completed"])


class TestGetPendingTasks(unittest.TestCase):
    """Testes para o método get_pending_tasks"""

    def setUp(self):
        self.todo = TodoList()
        self.todo.add_task("Tarefa 1")
        self.todo.add_task("Tarefa 2")
        self.todo.add_task("Tarefa 3")

    # Caso de Teste 9
    def test_pending_tasks_excludes_completed(self):
        """CT-09: Tarefas concluídas não devem aparecer nas pendentes."""
        self.todo.complete_task(2)
        pending = self.todo.get_pending_tasks()
        ids = [t["id"] for t in pending]

        self.assertIn(1, ids)
        self.assertNotIn(2, ids)
        self.assertIn(3, ids)

    # Caso de Teste 10
    def test_pending_tasks_empty_when_all_completed(self):
        """CT-10: Lista pendente deve ser vazia quando todas concluídas."""
        self.todo.complete_task(1)
        self.todo.complete_task(2)
        self.todo.complete_task(3)

        self.assertEqual(len(self.todo.get_pending_tasks()), 0)


if __name__ == "__main__":
    unittest.main()
