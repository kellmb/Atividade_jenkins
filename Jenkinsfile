//  Jenkinsfile — To-Do List 
//  Suporta os 4 cenários + cenário bonus
//
//  Variável de ambiente:
//    SCENARIO  →  "success" | "build_fail" | "test_fail" | "coverage"
//  Deixar em branco ou "success" para o cenário padrão (1 e 4).

pipeline {
    agent any

    environment {
        PYTHON = 'python3'
        APP_DIR = 'todo_app'
    }

    triggers {
        // Cenário 4: build agendada — toda hora no minuto 0
        cron('0 * * * *')
    }

    stages {

        // ----------------------------------------------------------
        // STAGE 1 — Preparar ambiente virtual
        // ----------------------------------------------------------
        stage('Setup') {
            steps {
                echo '>>> Criando ambiente virtual Python...'
                sh """
                    ${PYTHON} -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install pytest pytest-cov
                """
            }
        }

        // ----------------------------------------------------------
        // STAGE 2 — Build / "Compilação"
        // Para Python usamos py_compile para simular compilação.
        // Cenário 2: SCENARIO=build_fail injeta erro de sintaxe.
        // ----------------------------------------------------------
        stage('Build') {
            steps {
                echo '>>> Verificando sintaxe dos fontes (py_compile)...'
                script {
                    if (env.SCENARIO == 'build_fail') {
                        echo 'SIMULANDO FALHA DE BUILD — introduzindo erro de sintaxe...'
                        sh """
                            echo 'def broken(: pass' >> ${APP_DIR}/todo.py
                            . venv/bin/activate
                            ${PYTHON} -m py_compile ${APP_DIR}/todo.py
                        """
                    } else {
                        sh """
                            . venv/bin/activate
                            ${PYTHON} -m py_compile ${APP_DIR}/todo.py
                            ${PYTHON} -m py_compile ${APP_DIR}/test_todo.py
                            echo 'Build OK — nenhum erro de sintaxe encontrado.'
                        """
                    }
                }
            }
        }

        // ----------------------------------------------------------
        // STAGE 3 — Testes
        // Cenário 3: SCENARIO=test_fail usa arquivo com bug proposital.
        // Cenário Bônus: SCENARIO=coverage ativa relatório de cobertura.
        // ----------------------------------------------------------
        stage('Test') {
            steps {
                echo '>>> Executando testes...'
                script {
                    if (env.SCENARIO == 'test_fail') {
                        // Injeta bug no add_task para causar falha nos testes
                        echo 'SIMULANDO FALHA DE TESTE — introduzindo bug no add_task...'
                        sh """
                            sed -i 's/len(self.tasks) + 1/len(self.tasks)/' ${APP_DIR}/todo.py
                            . venv/bin/activate
                            pytest ${APP_DIR}/test_todo.py \
                                --junitxml=reports/junit.xml \
                                -v || true
                        """
                    } else if (env.SCENARIO == 'coverage') {
                        // Cenário Bônus — cobertura de código
                        sh """
                            mkdir -p reports
                            . venv/bin/activate
                            pytest ${APP_DIR}/test_todo.py \
                                --junitxml=reports/junit.xml \
                                --cov=${APP_DIR} \
                                --cov-report=xml:reports/coverage.xml \
                                --cov-report=html:reports/htmlcov \
                                --cov-fail-under=80 \
                                -v
                        """
                    } else {
                        // Cenários 1 e 4 — execução normal
                        sh """
                            mkdir -p reports
                            . venv/bin/activate
                            pytest ${APP_DIR}/test_todo.py \
                                --junitxml=reports/junit.xml \
                                -v
                        """
                    }
                }
            }
        }
    }

    // ----------------------------------------------------------
    // POST — Publicar relatórios sempre que possível
    // ----------------------------------------------------------
    post {
        always {
            echo '>>> Publicando relatórios...'

            // Relatório JUnit (testes)
            junit allowEmptyResults: true,
                  testResults: 'reports/junit.xml'

            // Relatório de cobertura 
            script {
                if (fileExists('reports/coverage.xml')) {
                    publishCoverage adapters: [coberturaAdapter('reports/coverage.xml')],
                                   sourceFileResolver: sourceFiles('NEVER_STORE')
                }
            }
        }

        success {
            echo 'Pipeline finalizado com SUCESSO!'
        }

        unstable {
            echo 'Pipeline INSTÁVEL — testes falharam!'
        }

        failure {
            echo 'Pipeline FALHOU — verifique os logs acima.'
        }
    }
}
