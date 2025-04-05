from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///voting.db'
db = SQLAlchemy(app)

# Database Model for Voters
class Voter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voter_id = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    has_voted = db.Column(db.Boolean, default=False)

# Database Model for Candidates
class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    votes = db.Column(db.Integer, default=0)

# Admin credentials
ADMIN_USERNAME = "muthiah"
ADMIN_PASSWORD = "mptc208"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        voter_id = request.form['voter_id']
        password = request.form['password']
        voter = Voter.query.filter_by(voter_id=voter_id, password=password).first()
        if voter and not voter.has_voted:
            session['voter_id'] = voter_id
            return redirect('/vote')
        return "Invalid Login or You Already Voted!"
    return render_template('login.html')

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    if 'voter_id' not in session:
        return redirect('/login')
    
    candidates = Candidate.query.all()
    
    if request.method == 'POST':
        selected_candidate_id = request.form['candidate']
        voter = Voter.query.filter_by(voter_id=session['voter_id']).first()
        candidate = Candidate.query.get(selected_candidate_id)

        if voter and candidate:
            candidate.votes += 1
            voter.has_voted = True
            db.session.commit()
            session.pop('voter_id', None)
            return "Voted Successfully!"

    return render_template('vote.html', candidates=candidates)

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin'] = True
            return redirect('/dashboard')
        return "Invalid Admin Credentials!"
    return render_template('admin_login.html')

@app.route('/dashboard')
def dashboard():
    if 'admin' not in session:
        return redirect('/admin')
    candidates = Candidate.query.all()
    voters = Voter.query.all()
    return render_template('dashboard.html', candidates=candidates, voters=voters)

@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/')

@app.route('/add_candidate', methods=['POST'])
def add_candidate():
    if 'admin' not in session:
        return redirect('/admin')
    name = request.form['name']
    new_candidate = Candidate(name=name)
    db.session.add(new_candidate)
    db.session.commit()
    return redirect('/dashboard')

@app.route('/delete_candidate/<int:id>')
def delete_candidate(id):
    if 'admin' not in session:
        return redirect('/admin')
    candidate = Candidate.query.get(id)
    if candidate:
        db.session.delete(candidate)
        db.session.commit()
    return redirect('/dashboard')

@app.route('/add_voter', methods=['POST'])
def add_voter():
    if 'admin' not in session:
        return redirect('/admin')
    voter_id = request.form['voter_id']
    password = request.form['password']
    new_voter = Voter(voter_id=voter_id, password=password)
    db.session.add(new_voter)
    db.session.commit()
    return redirect('/dashboard')

@app.route('/delete_voter/<int:id>')
def delete_voter(id):
    if 'admin' not in session:
        return redirect('/admin')
    voter = Voter.query.get(id)
    if voter:
        db.session.delete(voter)
        db.session.commit()
    return redirect('/dashboard')

@app.route('/view_results')
def view_results():
    candidates = Candidate.query.all()
    return render_template('results.html', candidates=candidates)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
