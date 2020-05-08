from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
import json
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import plotly


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
		beschreibung = str(request.form["beschreibung"])
		gewicht = float(request.form["gewicht"])
		wiederholungen = int(request.form["wiederholungen"])

		rm = {
			"beschreibung": beschreibung,
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
		titel = request.form["titel"]
		verbesserungsbereich = request.form["verbesserungsbereich"]
		startdatum = request.form["startdatum"]

		training = {
			"rm": rm,
			"verbesserungsbereich": verbesserungsbereich,
			"startdatum": startdatum,
			"titel": titel
		}

		#Prüfe ob das Training mit dem Titel bereits vorhanden 
		for element in trainingseinheiten:
			if element["titel"] == titel:
				return render_template("training.html", existiert_bereits = True, rms = rms)
		
		# Minimun Gewicht etc. berechnen
		training = berechne_trainings_werte(training)
		
		trainingseinheiten.append(training)
		schreibe_daten_in_json(trainingseinheiten_json_pfad, trainingseinheiten)
		return render_template("trainings_bestaetigung.html", training = training)

	return render_template("training.html", rms = rms)

@app.route('/tracking', methods=["GET", "POST"])
def tracking():
	trainingseinheiten = lade_daten_aus_json(trainingseinheiten_json_pfad, [])
	if request.method == "POST":
		trainings_titel = request.form["trainings_auswahl"]
		return redirect(url_for("tracking_details", trainings_titel = trainings_titel))

	return render_template("tracking.html", trainingseinheiten = trainingseinheiten)

@app.route('/tracking_details/<trainings_titel>', methods = ["GET", "POST"])
def tracking_details(trainings_titel):
	#Finde das Training mit diesem Trainingstitel
	trainingseinheiten = lade_daten_aus_json(trainingseinheiten_json_pfad, [])
	training = None
	for element in trainingseinheiten:
		if element["titel"] == trainings_titel:
			training = element
		if request.method == "POST":
			gewicht = float(request.form["gewicht"])
			wiederholungen = int(request.form["wiederholungen"])
			startdatum = request.form["startdatum"]

			tracking_eintrag = {
				"gewicht": gewicht,
				"wiederholungen": wiederholungen,
				"startdatum": startdatum
			}

			#Wir müssen hier nicht mehr überprüfen ob das Training vorhanden ist. Da der Benutzer sonst die Eingaben nicht hätte machen
			tracking = training.get("tracking", [])
			tracking.append(tracking_eintrag)
			training["tracking"] = tracking 
			schreibe_daten_in_json(trainingseinheiten_json_pfad, trainingseinheiten)
			return redirect(url_for("resultate"))
		return render_template("tracking_details.html", training = training)


@app.route('/resultate')
def resultate():
	trainingseinheiten = lade_daten_aus_json(trainingseinheiten_json_pfad, [])
	return render_template("resultate.html", trainingseinheiten = trainingseinheiten)    

@app.route('/details/<trainings_titel>')
def details(trainings_titel):
	trainingseinheiten = lade_daten_aus_json(trainingseinheiten_json_pfad, [])
	# Finde das entsprechende Training
	resultat = None
	for training in trainingseinheiten:
		if training["titel"] == trainings_titel:
			resultat = training

	# Sortiere die Trackingseinträge nach Datum (vom ältesten zum neusten)
	# TODO
	# resultat["tracking"] = resultat["tracking"].sort(key=lambda tup: datetime.strptime(tup[3], '%d.%m.%Y'))
	# Hole Daten für Chart
	fig = go.Figure()
	x = []
	y = []
	for einheit in resultat["tracking"]:
		x.append(einheit["startdatum"])
		y.append(einheit["gewicht"])

	fig.add_trace(go.Scatter(x = x, y = y, line=dict(color='royalblue', width=4)))
	#Edit the layout
	fig.update_layout(title='Average',
		xaxis_title='Startdatum',
		yaxis_title='Gewicht')
	div = plotly.offline.plot(fig, output_type="div")
	return render_template("details.html", chart=div, training=resultat) 

if __name__ == "__main__":
    app.run(debug=True, port=5000)#