from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import json
from datetime import datetime, timedelta

app = Flask("Name App")

rm_json_pfad = "./rm.json"
trainingseinheiten_json_pfad = "./traingseinheiten.json"
tracking_json_pfad = "./tracking.json"

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

def dictionary_von_string(text):
	# String in dictionary umwandeln: https://www.geeksforgeeks.org/python-convert-string-dictionary-to-dictionary/
	# Die Property namen müssen mit "" anstelle von '' umgeben sein.
	return json.loads(text.replace("'", '"'))

def berechne_trainings_werte(training):
	minimum_gewicht = 1
	maximum_gewicht = 1
	minimum_wiederholungen = 1
	maximum_wiederholungen = 1
	minimum_einheiten_pro_woche = 1
	maximum_einheiten_pro_woche = 1
	minimum_zu_erreichende_einheiten = 1
	maximum_zu_erreichende_einheiten = 1
	today = datetime.now()
	end_datum = today

	# Werte aus einer Tabelle von einer Kollegin
	if training["verbesserungsbereich"].lower() == "ausdauer":
		minimum_gewicht = round(0.5 * training["rm"]["resultat"], 2)
		maximum_gewicht = round(0.6 * training["rm"]["resultat"], 2)
		minimum_wiederholungen = 20
		maximum_wiederholungen = 40
		minimum_einheiten_pro_woche = 2
		maximum_einheiten_pro_woche = 3
		wochen = 4
		minimum_zu_erreichende_einheiten = wochen * minimum_einheiten_pro_woche
		maximum_zu_erreichende_einheiten = wochen * maximum_einheiten_pro_woche
		# https://pymotw.com/2/datetime/
		end_datum = today + timedelta(weeks=wochen)
	elif training["verbesserungsbereich"].lower() == "kraft":
		minimum_gewicht = round(0.9 * training["rm"]["resultat"], 2)
		maximum_gewicht = round(training["rm"]["resultat"], 2)
		minimum_wiederholungen = 1
		maximum_wiederholungen = 5
		minimum_einheiten_pro_woche = 2
		maximum_einheiten_pro_woche = 2
		wochen = 8
		minimum_zu_erreichende_einheiten = wochen * minimum_einheiten_pro_woche
		maximum_zu_erreichende_einheiten = wochen * maximum_einheiten_pro_woche
		# https://pymotw.com/2/datetime/
		end_datum = today + timedelta(weeks=wochen)
	else:
		# Muskelaufbau
		minimum_gewicht = round(0.6 * training["rm"]["resultat"], 2)
		maximum_gewicht = round(0.85 * training["rm"]["resultat"], 2)
		minimum_wiederholungen = 8
		maximum_wiederholungen = 12
		minimum_einheiten_pro_woche = 2
		maximum_einheiten_pro_woche = 3
		wochen = 12
		minimum_zu_erreichende_einheiten = round(wochen * minimum_einheiten_pro_woche, 2)
		maximum_zu_erreichende_einheiten = round(wochen * maximum_einheiten_pro_woche, 2)
		# https://pymotw.com/2/datetime/
		end_datum = today + timedelta(weeks=wochen)

	# Gleiches Format wie Date Picker
	# https://www.w3schools.com/python/python_datetime.asp
	end_datum = end_datum.strftime("%A, %d.%m.%Y") 

	training["minimum_gewicht"] = minimum_gewicht
	training["maximum_gewicht"] = maximum_gewicht
	training["minimum_wiederholungen"] = minimum_wiederholungen
	training["maximum_wiederholungen"] = maximum_wiederholungen
	training["minimum_einheiten_pro_woche"] = minimum_einheiten_pro_woche
	training["maximum_einheiten_pro_woche"] = maximum_einheiten_pro_woche
	training["minimum_zu_erreichende_einheiten"] = minimum_zu_erreichende_einheiten
	training["maximum_zu_erreichende_einheiten"] = maximum_zu_erreichende_einheiten
	training["end_datum"] = end_datum

	return training

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
		rm["resultat"]= round(ergebnis, 2) # Gerundet auf 2 Nachkommastellen 
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
		rm = dictionary_von_string(request.form["rm"])
		verbesserungsbereich = request.form["verbesserungsbereich"]
		startdatum = request.form["startdatum"]

		training = {
			"rm": rm,
			"verbesserungsbereich": verbesserungsbereich,
			"startdatum": startdatum,
		}
		
		if training in trainingseinheiten:
			return render_template("training.html", existiert_bereits = True, rms = rms)

		# Minimun Gewicht etc. berechnen
		training = berechne_trainings_werte(training)
		
		trainingseinheiten.append(training)
		schreibe_daten_in_json(trainingseinheiten_json_pfad, trainingseinheiten)
		return render_template("trainings_bestätigung.html", training = training)

	return render_template("training.html", rms = rms)

@app.route('/tracking', methods=["GET", "POST"])
def tracking():
	rms = lade_daten_aus_json(rm_json_pfad, [])
	if request.method == "POST":
		tracking = lade_daten_aus_json(tracking_json_pfad, [])

	#Extrahiere info aus dem request
		rm = dictionary_von_string(request.form["rm"])
		verbesserungsbereich = request.form["verbesserungsbereich"]
		startdatum = request.form["startdatum"]

		training = {
			"rm": rm,
			"verbesserungsbereich": verbesserungsbereich,
			"startdatum": startdatum,
		}
		
		if training in tracking:
			return render_template("tracking.html", existiert_bereits = True, rms = rms)
		
		tracking.append(training)
		schreibe_daten_in_json(tracking_json_pfad, tracking)
		return render_template("resultate.html", tracking = tracking)

	return render_template("tracking.html", rms = rms)

@app.route('/resultate')
def resultate():
    return render_template("resultate.html")    

if __name__ == "__main__":
    app.run(debug=True, port=5000)#