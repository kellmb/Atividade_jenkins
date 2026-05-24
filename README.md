# To-Do List — Jenkins CI/CD Demo

Projeto didático para demonstração de pipeline CI/CD com **Jenkins + GitHub**.

## Estrutura

```
todo_app/
├── todo.py          # Aplicação principal (2 métodos: add_task, complete_task)
├── test_todo.py     # 10 casos de teste (unit test)
├── Jenkinsfile      # Pipeline declarativo 
└── README.md        # Este arquivo
``

# Rodar localmente

```bash
# Instalar dependências
pip install pytest pytest-cov

# Executar testes
pytest todo_app/test_todo.py -v

# Executar com cobertura
pytest todo_app/test_todo.py --cov=todo_app --cov-report=html -v
```

---

# Cenários do Jenkins

Configure a variável `SCENARIO` no job antes de executar:

| Cenário | SCENARIO      | Resultado esperado         |
|---------|---------------|----------------------------|
| 1       | `success`     |  Build + Testes OK        |
| 2       | `build_fail`  |  Falha no Build           |
| 3       | `test_fail`   |  Build OK, Testes FALHAM  |
| 4       | `success`     |  Agendado via cron        |
| Bônus   | `coverage`    |  Build + Testes + Cobertura|

---

# Configurar variável SCENARIO no Jenkins

1. Abra o job > **Configure**
2. Marque **"This project is parameterized"**
3. Adicione **String Parameter**: Nome = `SCENARIO`, Default = `success`
4. Ao clicar em **Build with Parameters**, escolha o valor desejado

---

# Métodos implementados

### `add_task(task: str) → dict`
Adiciona uma tarefa à lista. Retorna dict com `id`, `description` e `completed`.  
Lança `ValueError` se a tarefa for vazia.

### `complete_task(task_id: int) → dict`
Marca a tarefa do ID informado como concluída.  
Lança `ValueError` se o ID não existir.

### `get_pending_tasks() → list`
Retorna apenas as tarefas ainda não concluídas.

---

## Plugins Jenkins necessários

- **Git Plugin** — integração com GitHub
- **JUnit Plugin** — relatório de testes
- **Coverage Plugin** (ou Cobertura) — cobertura de código (Bônus)
- **Pipeline Plugin** — suporte ao Jenkinsfile

---

## Links

- Repositório: https://github.com/kellmb/Atividade_jenkins.git
- Vídeos: 
