from flask import Flask, render_template, request, redirect, jsonify
from flask_httpauth import HTTPDigestAuth
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
auth = HTTPDigestAuth()

# 認証情報
users = {"admin": "password"}

@auth.get_password
def get_pw(username):
    return users.get(username)

def get_db_connection():
    conn = sqlite3.connect('blog.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    posts = conn.execute('SELECT * FROM posts ORDER BY created_at DESC').fetchall()
    conn.close()
    return render_template('index.html', posts=posts)

@app.route('/post', methods=['GET', 'POST'])
@auth.login_required
def post():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn = get_db_connection()
        conn.execute('INSERT INTO posts (title, content) VALUES (?, ?)', (title, content))
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('post.html')

@app.route('/api/post/<int:post_id>')
def get_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?', (post_id,)).fetchone()
    conn.close()
    return jsonify(title=post['title'], content=post['content']) if post else ('', 404)

if __name__ == '__main__':
    app.run(debug=True)
