# main.py (crie na pasta todo_app)
from todo import TodoList

lista = TodoList()
lista.add_task("Fazer atividade de GC")
lista.add_task("Gravar os videos")
lista.complete_task(1)

print("=== Todas as tarefas ===")
for t in lista.get_all_tasks():
    status = "✓" if t["completed"] else "○"
    print(f"  [{status}] {t['id']}. {t['description']}")

print("\n=== Pendentes ===")
for t in lista.get_pending_tasks():
    print(f"  ○ {t['id']}. {t['description']}")