from flask import Flask, render_template, redirect, request, flash
import mysql.connector
from mysql.connector import Error
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'EXTENCAO'

# Configuração do banco de dados MySQL
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'tabela_escola',
}

# Tela de login do diretor
@app.route('/')
def login():
    return render_template("AcessoDiretor.html")

# Rota para processar o login do diretor
@app.route('/login_diretor', methods=['POST'])
def login_diretor():
    usuario = request.form.get('usuario')
    senha = request.form.get('senha')
    alunos = alunos_cadastrados()
    

    if usuario == 'diretor' and senha == '123':
        return render_template('diretor_tela1.html', alunos=alunos)
    else:
        flash('Usuário ou senha inválidos, por favor tente novamente.')
        return redirect('/')

# Rota para adicionar aluno
@app.route('/adicionar_aluno', methods=['POST'])
def adicionar_aluno():
    return render_template("adicionar_pfs_aln.html")

# Rota para adicionar professor
@app.route('/adicionar_professor', methods=['POST'])
def adicionar_professor():
    return render_template("cadastro_professor.html")

@app.route('/cadastro_prof', methods=['POST'])
def cadastro_profe():
    conn = None
    cursor = None

    try:
        # Conectando ao banco de dados
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Coletando os dados do formulário
        nome = request.form.get('nome')                # Nome do professor
        cpf = request.form.get('cpf')                  # CPF do professor
        turma = request.form.get('turma')              # Turma que o professor leciona
        numero = request.form.get('numero')            # Número de telefone do professor
        email = request.form.get('email')              # Email do professor
        idade = request.form.get('idade')              # Idade do professor
        senha = request.form.get('senha')              # Senha de acesso do professor
        materia = request.form.get('materia')          # Matéria que o professor leciona
        horario = request.form.get('horario')          # Horário em que o professor irá dar aula

        # Inserindo os dados na tabela PROFESSOR
        cursor.execute(
            "INSERT INTO PROFESSOR (nome, cpf, turma, numero, email, idade, materia, horario, senha) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",  # Placeholders para os valores a serem inseridos
            (nome, cpf, turma, numero, email, idade, materia, horario, senha)
        )

        # Confirmando as operações realizadas
        conn.commit()

        return "Professor cadastrado com sucesso"

    except Error as e:
        # Tratando erros que podem ocorrer ao tentar conectar ou inserir dados
        return f"Erro ao conectar ao banco de dados: {e}"

    finally:
        # Fechando o cursor e a conexão com o banco de dados
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# Rota para deletar ou editar aluno/professor
@app.route('/deletar_editar', methods=['POST'])
def deletar_editar():
    alunos = alunos_cadastrados()
    return render_template("alterar.html", alunos=alunos)

# ALUNOS JA CADASTRADOS SERAO MOSTRADOS EM UMA TABELA
def alunos_cadastrados():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM ALUNO")
    alunos = cursor.fetchall()

    cursor.close()
    conn.close()

    return alunos

# Cadastro de aluno no banco de dados
@app.route("/cadastro_alun", methods=['POST', 'GET'])
def mostrar():
    conn = None
    cursor = None

    try:
        # Conectando ao banco de dados usando as configurações definidas anteriormente
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Coletando dados do formulário enviado via método POST
        nome = request.form.get('nome')                # Nome do aluno
        cpf = request.form.get('cpf')                  # CPF do aluno
        turma = request.form.get('turma')              # Turma em que o aluno está matriculado
        numero = request.form.get('numero')            # Número de telefone do aluno/responsável
        data_nascimento = request.form.get('data_d_nasc')  # Data de nascimento do aluno
        responsavel = request.form.get('responsavel')  # Nome do responsável
        ano = request.form.get('ano')                  # Ano da série do aluno
        email = request.form.get('email')              # Email do aluno ou responsável
        senha = request.form.get('senha')              # Senha de acesso do aluno

        # Validando que todos os campos foram preenchidos corretamente
        if not nome or not cpf or not turma or not numero or not data_nascimento or not responsavel or not ano or not email or not senha:
            return "Erro: Todos os campos devem ser preenchidos."

        # Verificando se o CPF tem 11 dígitos
        if len(cpf) != 11:
            return "Erro: O CPF deve conter 11 dígitos."

        # Verificando se o número do telefone é válido
        if len(numero) < 8 or len(numero) > 14:
            return "Erro: O número de telefone deve conter entre 8 e 14 dígitos."

        # Inserindo os dados na tabela ALUNO
        cursor.execute(
            "INSERT INTO ALUNO (nome, cpf, turma, numero, data_nascimento, responsavel, senha, email, ano_serie) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",  # Os placeholders indicam onde os valores coletados serão inseridos
            (nome, cpf, turma, numero, data_nascimento, responsavel, senha, email, ano)
        )

        # Definindo matérias padrões para o aluno
        materias = ["portugues", "matematica", "ingles", "fisica"]  # Lista de matérias padrão
        prova1 = 0  # Nota da primeira prova
        prova2 = 0  # Nota da segunda prova
        nota_final = 0  # Nota final (inicializada com zero)

        # Inserindo as matérias na tabela MATERIAS associadas ao aluno
        for materia in materias:
            cursor.execute(
                "INSERT INTO MATERIAS (ano, materia, PROVA1, PROVA2, NOTA_FINAL) "
                "VALUES (%s, %s, %s, %s, %s)",  # Placeholders para os valores das colunas
                (ano, materia, prova1, prova2, nota_final)
            )

        # Confirmando as operações realizadas (inserção dos dados)
        conn.commit()

        return "Aluno cadastrado com sucesso"

    except Error as e:
        # Em caso de erro, retorna uma mensagem explicando o que ocorreu
        return f"Erro ao conectar ao banco de dados: {e}"

    finally:
        # Fechando a conexão e o cursor para liberar os recursos
        if cursor:
            cursor.close()
        if conn:
            conn.close()
            
from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)

# Conectar ao banco de dados
def get_db_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='tabela_escola'
    )


@app.route('/resposta_aluno', methods=['POST'])
def resposta_aluno():
    termo_pesquisa = request.form['barraPesquisa']
    conn = get_db_connection()
    if conn is None:
        flash("Erro ao conectar ao banco de dados.")
        return redirect('/')

    cursor = conn.cursor()
    query = '''SELECT matricula, ano_serie, nome, cpf, turma, email 
               FROM ALUNO 
               WHERE matricula LIKE %s OR nome LIKE %s OR ano_serie LIKE %s'''
    termo_pesquisa_com_wildcard = f"%{termo_pesquisa}%"
    cursor.execute(query, (termo_pesquisa_com_wildcard, termo_pesquisa_com_wildcard, termo_pesquisa_com_wildcard))
    
    res_aluno = cursor.fetchall()
    cursor.close()
    conn.close()
    
    return render_template('diretor_tela1.html', res_aluno=res_aluno)


            

# Rota para pesquisar aluno
@app.route('/pesquisar_aluno', methods=['POST'])
def pesquisar_aluno():
    alunos = alunos_cadastrados()
    return render_template('diretor_tela1.html', alunos=alunos)

if __name__ == "__main__":
    app.run(debug=True)
