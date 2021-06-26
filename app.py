from flask import Flask, jsonify, render_template

app = Flask(__name__, static_url_path='/static')

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