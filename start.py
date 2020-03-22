from flask import Flask
from flask import render_template
app = Flask("Name App")

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/rm-calculator')
def rm_calculator():
    return render_template("1RM.html")    

if __name__ == "__main__":
    app.run(debug=True, port=5000)