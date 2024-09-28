from flask import Flask,render_template,redirect,request,flash,url_for,send_file, jsonify
import mysql.connector
from mysql.connector import Error
app= Flask(__name__)
app.config['SECRET_KET']= 'MAR'

@app.route('')
def criar_banco_de_dados():
    db_tabela = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': '',
    }
    
    cunn = None
    cursor = None
    
    try:
        cunn = mysql.connector.connect(**db_tabela)
        cursor = cunn.cursor()
        
        # Criar o banco de dados se não existir
        cursor.execute("CREATE DATABASE IF NOT EXISTS tabela_escola")
        cunn.commit()

        # Usar o banco de dados 'tabela_prod'
        cursor.execute("USE tabela_escola")

        # Criar tabela 'aluno' se não existir
        cursor.execute('''CREATE TABLE IF NOT EXISTS ALUNO(
                           id INT NOT NULL AUTO_INCREMENT,
                           matricula VARCHAR(12),
                           ano_serie VARCHAR(10),
                           cpf VARCHAR(11),
                           turma VARCHAR(20),
                           nome_responsavel(80),
                           email VARCHAR(30),
                           NUMERO VARCHAR(14),
                           idade VARCHAR(3),
                           nome VARCHAR(80),
                           materias INT(20),
                           senha VARCHAR(12)
                           
                           );''')
        # Criar tabela 'materias' se não existir
        cursor.execute('''CREATE TABLE IF NOT MATERIAS(
                           id INT NOT NULL AUTO_INCREMENT,
                           matricula VARCHAR(12),
                           ANO_SERIE,
                           materia VARCHAR(20),
                           PROVA1 INT(2),
                           PROVA2 INT(2),
                           NOTA_FINAL(2)
                           );''')
        # Criar tabela 'diretor' se não existir
        cursor.execute('''CREATE TABLE IF NOT DIRETOR(
                           id INT NOT NULL AUTO_INCREMENT,
                           nome VARCHAR(80),
                           senha varchar(12)
                           senha_mudanca VARCHAR(12)
                           );''')
         # Criar tabela 'PROFESSOR' se não existir
        cursor.execute('''CREATE TABLE IF NOT professor(
                           id INT NOT NULL AUTO_INCREMENT,
                           materia_professor(30),
                           nome VARCHAR(80),
                           materia VARCHAR(30),
                           horario VARCHAR(6),
                           senha VARCHAR(12)
                           );''')
         # Criar tabela 'RESPONSAVEL' se não existir
        cursor.execute('''CREATE TABLE IF NOT EXISTS RESPONSAVEL(
                           id INT NOT NULL AUTO_INCREMENT,
                           cpf VARCHAR(11),
                           nome_responsavel(80),
                           email VARCHAR(30),
                           NUMERO VARCHAR(14),
                           idade VARCHAR(3),
                           senha VARCHAR(12)
                           
                           );''')
        cunn.commit()
        
        print("Tabelas e banco de dados criados com sucesso")
        return "Tabelas e banco de dados criados com sucesso"
    
    except Error as e:
        print(f"Erro ao conectar ao MySQL: {e}")
        return f"Erro ao conectar ao MySQL: {e}"
    
    finally:
        if cursor is not None:
            cursor.close()
        if cunn is not None:
            cunn.close()

if __name__ == "__main__":
    app.run(debug=True)  