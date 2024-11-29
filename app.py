from flask import Flask, render_template, request, redirect, url_for
import json
import os
import difflib

app = Flask(__name__)

# Função para carregar o banco de dados
def load_database():
    if os.path.exists('database.json'):
        with open('database.json', 'r') as f:
            return json.load(f)
    else:
        return {}

# Função para salvar no banco de dados
def save_database(db):
    with open('database.json', 'w') as f:
        json.dump(db, f, indent=4)

@app.route('/', methods=['GET', 'POST'])
def index():
    db = load_database()
    if request.method == 'POST':
        question = request.form['question'].strip().lower()
        # Verificar similaridade com perguntas existentes
        similar_questions = difflib.get_close_matches(question, db.keys(), n=1, cutoff=0.3)

        if similar_questions:
            # Pega a pergunta mais parecida
            matched_question = similar_questions[0]
            answer = db[matched_question]
            return render_template('index.html', question=question, matched_question=matched_question, answer=answer)
        else:
            return render_template('index.html', question=question, not_found=True)
    added = request.args.get('added')
    return render_template('index.html', added=added)


@app.route('/learn', methods=['POST'])
def learn():
    question = request.form['question'].strip().lower()
    answer = request.form['answer'].strip()
    db = load_database()
    db[question] = answer
    save_database(db)
    return render_template('index.html', learned=True)

@app.route('/adjust', methods=['POST'])
def adjust():
    # Use a pergunta feita pelo usuário (não a similar)
    question = request.form['original_question']
    return render_template('index.html', adjust=True, question=question)

@app.route('/update', methods=['POST'])
def update():
    question = request.form['question'].strip().lower()
    new_answer = request.form['new_answer'].strip()
    db = load_database()
    
    # Adiciona a nova pergunta com sua resposta ao banco de dados
    db[question] = new_answer
    save_database(db)
    
    return redirect(url_for('index', added=True))


if __name__ == '__main__':
    app.run(debug=True)
