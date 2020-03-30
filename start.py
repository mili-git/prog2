from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import json 

app = Flask("Name App")

rm_json_pfad = "./rm.json"

def lade_daten_aus_json (pfad, standard_wert = []):
	#https://www.programiz.com/python-programming/json
	try:
		with open(pfad, 'r') as datei:
			return json.load(datei)
	except Exception:
		return standard_wert

def schreibe_daten_in_json(pfad, daten):
	#https://stackoverflow.com/questions/17043860/how-to-dump-a-dict-to-a-json-file
	with open(pfad, 'w') as datei:
		json.dump(daten, datei)



@app.route('/')
def index():
    return render_template("index.html")

@app.route('/rm-calculator', methods=["GET", "POST"])
def rm_calculator():
	if request.method == "POST":
		# Lies alle informationen über unsere bestehenden RMs aus der Datei
		alle_rms = lade_daten_aus_json(rm_json_pfad, [])

		#Extrahiere information aus dem request 
		gewicht = float(request.form["gewicht"])
		wiederholungen = int(request.form["wiederholungen"])

		rm = {
			"gewicht": gewicht,
			"wiederholungen": wiederholungen
		}

		if rm in alle_rms:
			return render_template("1rm.html", existiert_bereits = True)

		alle_rms.append(rm)

		schreibe_daten_in_json(rm_json_pfad, alle_rms)
		return redirect(url_for("training"))

    return render_template("1rm.html", existiert_bereits = False)    

@app.route('/training')
def training():
    return render_template("training.html")    

@app.route('/fortschritt')
def fort_schritt():
    return render_template("fortschritt.html")  

@app.route('/resultate')
def resultate():
    return render_template("resultate.html")    

if __name__ == "__main__":
    app.run(debug=True, port=5000)#