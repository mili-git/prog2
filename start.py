from flask import Flask
from flask import render_template
app = Flask("Name App")

@app.route('/hello')
def hello_world():
    return render_template("test.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)