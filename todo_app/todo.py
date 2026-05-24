"""
To-Do List Application
Métodos simples para gerenciamento de tarefas.
"""


class TodoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task: str) -> dict:
        """
        Adiciona uma nova tarefa à lista.

        Args:
            task: Descrição da tarefa (não pode ser vazia)

        Returns:
            dict com id, descrição e status da tarefa criada

        Raises:
            ValueError: Se a tarefa for vazia ou None
        """
        if not task or not task.strip():
            raise ValueError("A tarefa não pode ser vazia.")

        new_task = {
            "id": len(self.tasks) + 1,
            "description": task.strip(),
            "completed": False,
        }
        self.tasks.append(new_task)
        return new_task

    def complete_task(self, task_id: int) -> dict:
        """
        Marca uma tarefa como concluída pelo seu ID.

        Args:
            task_id: ID da tarefa a ser concluída

        Returns:
            dict com os dados atualizados da tarefa

        Raises:
            ValueError: Se o task_id não existir na lista
        """
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                return task

        raise ValueError(f"Tarefa com ID {task_id} não encontrada.")

    def get_pending_tasks(self) -> list:
        """
        Retorna todas as tarefas pendentes (não concluídas).

        Returns:
            Lista de tarefas com completed=False
        """
        return [task for task in self.tasks if not task["completed"]]

    def get_all_tasks(self) -> list:
        """
        Retorna todas as tarefas da lista.

        Returns:
            Lista com todas as tarefas
        """
        return self.tasks
