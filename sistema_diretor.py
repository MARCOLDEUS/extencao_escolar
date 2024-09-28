from flask import Flask, render_template, redirect, request, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.config['SECRET_KEY'] = 'EXTENCAO'

#configuracao do banco de dados mysql
db_config={
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'tabela_escola',
}

# TELA DE LOGIN DIRETOR
@app.route('/')
def login():
    return render_template("AcessoDiretor.html")

# ROTA PARA PROCESSAR O LOGIN DO DIRETOR
@app.route('/login_diretor', methods=['POST'])
def login_diretor():
    usuario = request.form.get('usuario')
    senha = request.form.get('senha')
    
    if usuario == 'diretor' and senha == '123':
        return render_template('diretor_tela1.html')
    else:
        flash('Usuário ou senha inválido, por favor tente novamente.')
        return redirect('/')

# ROTA PARA ADICIONAR ALUNO
@app.route('/adicionar_aluno', methods=['POST'])
def adicionar_aluno():
    return render_template("adicionar_pfs_aln.html")

# ROTA PARA ADICIONAR PROFESSOR
@app.route('/adicionar_professor', methods=['POST'])
def adicionar_professor():
    return render_template("cadastro_professor.html")

# ROTA PARA DELETAR OU EDITAR ALUNO/PROFESSOR
@app.route('/deletar/editar', methods=['POST'])
def deletar_editar():
    return render_template("alterar.html")


@app.route("/cadastro_alun", methods=['POST','GET'])
def mostar():
 
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()
    categoria = request.form.get('p')
   
    nome =request.form.get('nome')
    cpf = request.form.get('cpf')
    matricula = request.form.get('matricula')
    turma = request.form.get('turma')
    numero = int(request.form.get('numero'))
    data = request.form.get('data_d_nasc')
    responcavel = request.form.get('responcavel')
    senha = request.form.get('senha')
    
 

 
 #sistema de inpementacao de produtos no estoque
    if request.method == "POST":
     selected_option = request.form['p']
    if selected_option=='1_medio':
       categoria= "1_medio"
       cursor.execute(f"INSERT INTO ALUNO (nome,cpf,matrucula,turma,numero,data,responcavel,senha) VALUES ('{nome}','{cpf}','{matricula}','{numero}','{data}','{turma}','{responcavel}','{senha}')")
       conn.commit()
          
       return "produto cadastrado com sucesso"
          
    elif selected_option== '2_medio':
      categoria= "2_medio"
      cursor.execute(f"INSERT INTO ALUNO (nome,cpf,matrucula,turma,numero,data,responcavel,senha) VALUES ('{nome}','{cpf}','{matricula}','{numero}','{data}','{turma}','{responcavel}','{senha}')")
      conn.commit()
          
      return "produto cadastrado com sucesso"
    
if __name__ == "__main__":
    app.run(debug=True)
