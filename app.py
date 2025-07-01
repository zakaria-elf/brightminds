from flask import Flask, render_template, flash, redirect, url_for,request, jsonify
import requests
import mysql.connector
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql

app = Flask(__name__)




app = Flask(__name__)
app.config['SECRET_KEY'] = 'aed3d5504454b7a080dc5ce245e27d76c1e64887bb9bfbdc69757994cb6b7b61'

# Connexion à MySQL
def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="",   
        database="bd"  
    )

@app.route("/Home", methods=["POST"])
def Home():
    email = request.form.get('email')
    password = request.form.get('password')

    conn = get_db_connection()
    cursor = conn.cursor()

    # chercher l'utilisateur 
    cursor.execute("SELECT mot_de_passe FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()  

    cursor.close()
    conn.close()

    if user:
        password_db = user[0]  
        if password == password_db:
            return render_template("interface.html")  
        else:
            flash("Mot de passe incorrect", "error")
            return redirect(url_for('login'))
    else:
        flash("Email incorrect", "error")
        return redirect(url_for('login'))


user_inf ={
    "email": "zakariaelfadili00@gmail.com",
    "password": "hckhkjaheedaddfc"
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///brightminds.db'

app.config['SECRET_KEY'] = 'aed3d5504454b7a080dc5ce245e27d76c1e64887bb9bfbdc69757994cb6b7b61'
db = SQLAlchemy(app)


@app.route("/")
def login(): 
    return render_template('project.html', error="username or password is incorrect")

@app.route("/home", methods=["POST"])
def home():
    email=request.form.get('email')
    password=request.form.get('password')
    if email==user_inf["email"] and password== user_inf["password"]:
        return render_template("interface.html")
    else:
        """return render_template('login.html', error="try again please")"""
        flash("try again please", "error")
        return redirect(url_for('login'))

@app.route("/interface")
def interface ():
    return render_template('interface.html')
 
@app.route("/about")
def about ():
    return render_template('about.html')

@app.route("/blog")
def blog ():
    return render_template('blog.html')

@app.route("/contact")
def contact ():
    return render_template('contact.html')

@app.route("/courses")
def courses ():
    return render_template('courses.html')
@app.route("/dut1")
def dut1 ():
    return render_template('dut1.html')
@app.route("/dut2")
def dut2 ():
    return render_template('dut2.html')
@app.route("/license")
def license ():
    return render_template('license.html')

# Route principale
@app.route('/ginie')
def ginie():
    return render_template('ginie.html')  # ta page d'accueil

@app.route('/modele')
def modele():
    return render_template('modele.html')  # ta page d'accueil

# Route pour accéder aux cours
@app.route('/cours/<filename>')
def cours(filename):
    return send_from_directory('cours', filename)

#chatbot

API_KEY = "AIzaSyA6aycVnRxonCiV-7os0NBndLhQC4NZ8_M"
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-002:generateContent"

def envoyer_requete(prompt):
    """Envoie une requête à l'API Gemini et retourne la réponse uniquement."""
    sParam = {
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "generationConfig": {
            "temperature": 0.7,
            "topK": 40,
            "topP": 0.95,
            "maxOutputTokens": 1500
        }
    }

    headers = {"Content-Type": "application/json"}
    params = {"key": API_KEY}

    try:
        response = requests.post(API_URL, headers=headers, params=params, json=sParam)
        response.raise_for_status()
        data = response.json()

        
        bot_response = data.get("candidates", [{}])[0].get("content", {}).get("parts", [{}])[0].get("text", "Aucune réponse trouvée.")

        return bot_response
    except requests.exceptions.RequestException as e:
        return f"Erreur lors de la communication avec l'API: {e}"

@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")

@app.route("/ask", methods=["POST"])
def ask():
    user_input = request.json.get("prompt", "")
    response = envoyer_requete(user_input)
    return jsonify({"response": response})
#notes///

# Connexion à ta base de données
db = mysql.connector.connect(
    host="localhost",
    port=3306,          
    user="root",     
    password="",        
    database="bd"  
)

@app.route('/notes')
def afficher_notes():
    cursor = db.cursor(dictionary=True)
    
# récupérer les notes des étudiants
    cursor.execute("""
        SELECT 
            etudiants.nom,
            etudiants.prenom,
            modules.nom_module,
            notes.note
        FROM notes
        JOIN etudiants ON notes.etudiant_id = etudiants.id
        JOIN modules ON notes.module_id = modules.id
        ORDER BY etudiants.nom ASC, modules.nom_module ASC
    """)
    
    resultats = cursor.fetchall()  
    cursor.close()  
    
    return render_template('notes.html', notes=resultats)
#quiz

questions = [
    {"question": "Quelle est la définition correcte du cycle de vie du développement logiciel ?", "choices": [
        "C'est un processus qui consiste uniquement à écrire du code sans planification ni tests.",
        "C'est une méthode utilisée pour tester les logiciels après leur déploiement afin de corriger les erreurs éventuelles.",
        "C'est un ensemble d'étapes permettant de concevoir, développer, tester, déployer et maintenir un logiciel.",
        "C'est une approche où seuls les tests automatisés sont pris en compte pour garantir la qualité du logiciel."
    ], "answer": "C'est un ensemble d'étapes permettant de concevoir, développer, tester, déployer et maintenir un logiciel."},

    {"question": "Quelle est la définition correcte du modèle Code-And-Fix ?", "choices": [
        "C'est un modèle structuré qui suit une planification détaillée avant le codage et inclut une phase de conception approfondie.",
        "C'est une approche qui repose sur l'automatisation complète du développement logiciel à partir de règles et de modèles prédéfinis.",
        "C'est une méthode où les développeurs commencent immédiatement à coder sans planification préalable, en corrigeant les erreurs et en ajoutant des fonctionnalités au fur et à mesure.",
        "C'est un processus basé sur des cycles de développement itératifs avec des phases bien définies comme l'analyse, la conception, l'implémentation et la maintenance."
    ], "answer": "C'est une méthode où les développeurs commencent immédiatement à coder sans planification préalable, en corrigeant les erreurs et en ajoutant des fonctionnalités au fur et à mesure."},

    {"question": "Quel est le principe du modèle en cascade ?", "choices": [
        "Les phases du projet s’exécutent en parallèle",
        "Chaque phase commence uniquement après la fin de la précédente",
        "Il est basé sur une approche itérative et flexible",
        "Il n’inclut pas de phase de test"
    ], "answer": "Chaque phase commence uniquement après la fin de la précédente"},

    {"question": "Quelle est la première phase du modèle en cascade ?", "choices": [
        "Conception",
        "Développement",
        "Analyse des besoins",
        "Tests"
    ], "answer": "Analyse des besoins"},

    {"question": "Quels sont les inconvénients du modèle Code-And-Fix ?", "choices": [
        "Manque de planification, ce qui peut entraîner un code difficile à maintenir.",
        "Facilité de modification du code à tout moment sans contraintes.",
        "Accumulation d’erreurs et de bugs en raison de l’absence de structure claire.",
        "Risque élevé de coûts et de délais imprévisibles à long terme.",
        "Processus structuré et bien organisé dès le départ."
    ], "answer": "Manque de planification, ce qui peut entraîner un code difficile à maintenir."},

    {"question": "Pour utiliser le modèle incrémental, il faut d’abord avoir une idée claire et bien définie", "choices": [
        "Vrai", "Faux"
    ], "answer": "Vrai"},

    {"question": "Pour utiliser le modèle par prototypage, il faut d’abord avoir une idée claire et bien définie", "choices": [
        "Vrai", "Faux"
    ], "answer": "Faux"},

    {"question": "Quelle est une étape clé du modèle en spirale ?", "choices": [
        "Tests unitaires",
        "Analyse des risques",
        "Livraison du produit final dès la première itération",
        "Développement en une seule phase"
    ], "answer": "Analyse des risques"},

    {"question": "Quelle est la principale caractéristique du modèle en V ?", "choices": [
        "Il est identique au modèle en cascade",
        "Chaque phase de développement a une phase de test associée",
        "Il permet des itérations rapides entre les phases",
        "Il ne nécessite pas de documentation"
    ], "answer": "Chaque phase de développement a une phase de test associée"},

    {"question": "Le modèle qui vise à diviser le projet en petites parties et fonctionnalités est :", "choices": [
        "Le modèle en spirale",
        "Le modèle code-and-fix",
        "Le modèle en cascade",
        "Le modèle par spirale"
    ], "answer": "Le modèle par spirale"}
]



@app.route('/test')
def test():
    return redirect(url_for('quiz', q=0, score=0))

@app.route('/quiz')
def quiz():
    q = int(request.args.get("q", 0))
    score = int(request.args.get("score", 0))
    feedback = request.args.get("feedback", "")
    if q >= len(questions):
        return render_template("result.html", score=score, total=len(questions))
    return render_template("quiz.html", question=questions[q], q=q, score=score, feedback=feedback)

@app.route('/answer', methods=["POST"])
def answer():
    q = int(request.form["q"])
    score = int(request.form["score"])
    selected = request.form["choice"]
    correct = questions[q]["answer"]
    feedback = "✅ Correct!" if selected == correct else f"❌ Wrong! Correct answer: {correct}"
    if selected == correct:
        score += 1
    return redirect(url_for('quiz', q=q+1, score=score, feedback=feedback))
if __name__ == "__main__":
    app.run(debug=True)