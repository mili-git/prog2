from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import json

app = Flask("Name App")

rm_json_pfad = "./rm.json"
trainingseinheiten_json_pfad = "./traingseinheiten.json"

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

def berechne_rm(gewicht, wiederholungen):
	#https://en.wikipedia.org/wiki/One-repetition_maximum#Lombardi 
	resultat = gewicht*wiederholungen**0.10 
	return resultat

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/rm-calculator', methods=["GET", "POST"])
def rm_calculator():
	if request.method == "POST":
		# Lies alle informationen über unsere bestehenden RMs aus der Datei
		alle_rms = lade_daten_aus_json(rm_json_pfad, [])

		#Extrahiere information aus dem request 
		übungsname = str(request.form["übungsname"])
		gewicht = float(request.form["gewicht"])
		wiederholungen = int(request.form["wiederholungen"])

		rm = {
			"uebungsname": übungsname,
			"gewicht": gewicht,
			"wiederholungen": wiederholungen
		}

		if rm in alle_rms:
			return render_template("1rm.html", existiert_bereits = True)
		#Berechne 1 RM
		ergebnis = berechne_rm(gewicht, wiederholungen)
		rm["resultat"]= ergebnis
		alle_rms.append(rm)


		schreibe_daten_in_json(rm_json_pfad, alle_rms)
		return redirect(url_for("training"))
	return render_template("1rm.html", existiert_bereits = False)    

@app.route('/training', methods=["GET", "POST"])
def training():
	rms = lade_daten_aus_json(rm_json_pfad, [])
	if request.method == "POST":
		trainingseinheiten = lade_daten_aus_json(trainingseinheiten_json_pfad, [])


		#Extrahiere info aus dem request
		rm = request.form["rm"]
		verbesserungsbereich = request.form["verbesserungsbereich"]
		anzahltrainingseinheiten = int(request.form["trainingseinheiten"])
		startdatum = request.form["startdatum"]
		enddatum = request.form["enddatum"]

		training = {
			"rm": rm,
			"verbesserungsbereich": verbesserungsbereich,
			"anzahltrainingseinheiten": anzahltrainingseinheiten,
			"startdatum": startdatum,
			"enddatum": enddatum
		}
		
		if training in trainingseinheiten:
			return render_template("training.html", existiert_bereits = True)
		trainingseinheiten.append(training)
		schreibe_daten_in_json(trainingseinheiten_json_pfad, trainingseinheiten)
		return redirect(url_for("fortschritt"))


		
	return render_template("training.html", rms = rms)  

@app.route('/fortschritt')
def fortschritt():
    return render_template("fortschritt.html")  

@app.route('/resultate')
def resultate():
    return render_template("resultate.html")    

if __name__ == "__main__":
    app.run(debug=True, port=5000)#