from flask import Flask, render_template, redirect, request, flash, url_for, send_file, jsonify
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.config['SECRET_KEY'] = 'MAR'  # Corrigido SECRET_KET para SECRET_KEY

@app.route('/')
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

        # Usar o banco de dados 'tabela_escola'
        cursor.execute("USE tabela_escola")

        # Criar tabela 'aluno' se não existir
        cursor.execute('''CREATE TABLE IF NOT EXISTS ALUNO (
                          matricula INT NOT NULL AUTO_INCREMENT,  -- Matricula será gerada automaticamente
                          ano_serie VARCHAR(10),                  
                          cpf VARCHAR(11),                        
                          turma VARCHAR(20),                      
                          email VARCHAR(30),                      
                          numero VARCHAR(14),                     
                          idade VARCHAR(3),                       
                          nome VARCHAR(80),                       
                          responsavel VARCHAR(80),  
                          cpf_respon VARCHAR(11),                                
                          senha VARCHAR(12),                      
                          PRIMARY KEY (matricula)
                          ) AUTO_INCREMENT=100000;''')
        
        # Criar tabela 'materias' se não existir
        cursor.execute('''CREATE TABLE IF NOT EXISTS MATERIAS(
                           id INT NOT NULL AUTO_INCREMENT,
                           matricula VARCHAR(12),
                           ano VARCHAR(10),
                           materia VARCHAR(20),
                           prova1 FLOAT(5,2),
                           prova2 FLOAT(5,2),
                           nota_final FLOAT(5,2),
                           PRIMARY KEY (id)
                           );''')

        # Criar tabela 'diretor' se não existir
        cursor.execute('''CREATE TABLE IF NOT EXISTS DIRETOR(
                           id INT NOT NULL AUTO_INCREMENT,
                           nome VARCHAR(80),
                           senha VARCHAR(12),
                           senha_mudanca VARCHAR(12),
                           PRIMARY KEY (id)
                           );''')
        
        # Criar tabela 'professor' se não existir
        cursor.execute('''CREATE TABLE IF NOT EXISTS PROFESSOR(
                           matricula INT NOT NULL AUTO_INCREMENT,
                           nome VARCHAR(80),
                           cpf VARCHAR(30),
                           numero VARCHAR(14),
                           email VARCHAR(30),
                           idade VARCHAR(3),
                           senha VARCHAR(12),
                           PRIMARY KEY (matricula)
                          ) AUTO_INCREMENT=100000;''')

        
        # Criar tabela 'materias' se não existir do professor
        cursor.execute('''CREATE TABLE IF NOT EXISTS MATERIAS_PROFESSOR(
                           matricula VARCHAR(12),
                           ano_serie VARCHAR(10),
                           horario VARCHAR(4),
                           materia VARCHAR(20),
                           PRIMARY KEY (matricula)
                           );''')
        cursor.execute('ALTER TABLE ALUNO ADD COLUMN data_nascimento DATE;')
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
