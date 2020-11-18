from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    jsonify,
    flash
)
class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1, username='Juan', password='password'))
users.append(User(id=2, username='Pedro', password='efefefefe'))
users.append(User(id=3, username='Carlos', password='qwerty'))
users.append(User(id=4, username='root', password='root'))

app = Flask(__name__)
app.secret_key = 'somesecretkeythatonlyishouldknow'

@app.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user
@app.route('/')
def main():
    return redirect('profile') if session else redirect('login')
@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect("login")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        print(username,password)
        if len(username.replace(" ", "") )+len(password.replace(" ", ""))==0:
            return render_template("login.html")
        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('profile'))

        
        #flash("Incorrect Password")
        flash(username)
        print("flash")
        return redirect(url_for('login'))

    return render_template("login.html")

@app.route('/profile')
def profile():
    if not g.user:
        return redirect(url_for('login'))

    return render_template('profile.html')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5050",debug=True)