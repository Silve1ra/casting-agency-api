from flask import Flask, jsonify, render_template
from models import setup_db, Actor, Movie

app = Flask(__name__, static_url_path='/static')
setup_db(app)

@app.route('/')
def index():
    return jsonify({
        'service': 'Casting Agency API',
        'version': '1.1',
        'author': 'Felipe Silveira'
    })

@app.route('/docs')
def documentation():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(use_reloader=True)