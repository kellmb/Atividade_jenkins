//  Jenkinsfile — To-Do List 
//  Suporta os 4 cenários + cenário bonus
//
//  Variável de ambiente:
//    SCENARIO  →  "success" | "build_fail" | "test_fail" | "coverage"
//  Deixar em branco ou "success" para o cenário padrão (1 e 4).

pipeline {
    agent any

    environment {
        APP_DIR = 'todo_app'
    }

    triggers {
        cron('0 * * * *')
    }

    stages {

        stage('Setup') {
            steps {
                echo '>>> Criando ambiente virtual Python...'
                bat """
                    python -m venv venv
                    call venv\\Scripts\\activate.bat
                    pip install --upgrade pip
                    pip install pytest pytest-cov
                """
            }
        }

        stage('Build') {
            steps {
                echo '>>> Verificando sintaxe dos fontes (py_compile)...'
                script {
                    if (env.SCENARIO == 'build_fail') {
                        echo 'SIMULANDO FALHA DE BUILD...'
                        bat """
                            echo def broken(: pass >> ${APP_DIR}\\todo.py
                            call venv\\Scripts\\activate.bat
                            python -m py_compile ${APP_DIR}\\todo.py
                        """
                    } else {
                        bat """
                            call venv\\Scripts\\activate.bat
                            python -m py_compile ${APP_DIR}\\todo.py
                            python -m py_compile ${APP_DIR}\\test_todo.py
                            echo Build OK.
                        """
                    }
                }
            }
        }

        stage('Test') {
            steps {
                echo '>>> Executando testes...'
                script {
                    if (env.SCENARIO == 'test_fail') {
                        bat """
                            powershell -Command "(Get-Content ${APP_DIR}\\todo.py) -replace 'len\\(self\\.tasks\\) \\+ 1', 'len(self.tasks)' | Set-Content ${APP_DIR}\\todo.py"
                            call venv\\Scripts\\activate.bat
                            if not exist reports mkdir reports
                            pytest ${APP_DIR}\\test_todo.py --junitxml=reports\\junit.xml -v
                            exit /b 0
                        """
                    } else if (env.SCENARIO == 'coverage') {
                        bat """
                            if not exist reports mkdir reports
                            call venv\\Scripts\\activate.bat
                            pytest ${APP_DIR}\\test_todo.py --junitxml=reports\\junit.xml --cov=${APP_DIR} --cov-report=xml:reports\\coverage.xml --cov-report=html:reports\\htmlcov --cov-fail-under=80 -v
                        """
                    } else {
                        bat """
                            if not exist reports mkdir reports
                            call venv\\Scripts\\activate.bat
                            pytest ${APP_DIR}\\test_todo.py --junitxml=reports\\junit.xml -v
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            echo '>>> Publicando relatórios...'
            junit allowEmptyResults: true, testResults: 'reports\\junit.xml'
            script {
                if (fileExists('reports/coverage.xml')) {
                    recordCoverage(
                        tools: [[parser: 'COBERTURA', pattern: 'reports/coverage.xml']]
                    )
                }
            }   
        }
        success  { echo ' Pipeline finalizado com sucesso!' }
        unstable { echo ' Pipeline INSTÁVEL — testes falharam!' }
        failure  { echo ' Pipeline FALHOU!' }
    }
}