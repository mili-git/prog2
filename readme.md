# Projektidee Webapplikation
## Ausgangslage:
Sicherlich hast du schon ein Krafttraining Video angeschaut – vllt. mit Gewichten. Der Typ kann 20 Sätze machen und du bist nach 10 Wiederholungen schon ohne Kraft? Das liegt daran, dass ihr nicht die gleichen Kräfte haben oder dass er wahrscheinlich bereits trainiert hat und das Video seine ersten Trainings nicht gepostet hat ;) 
Deshalb wird sich diese Anwendung als nützlich erweisen. Diese benutzerdefinierte Anwendung wird das Maximum einer Wiederholung beim Krafttraining – 1RM (maximale Gewichtsmenge) berechnen. 

## Funktion/Projektidee: 
Diese Webapplikation wird für Menschen, die seine maximale Stärke kennenlernen wollen erstellt. Nicht jeder weiss, wie viel Gewicht er beim Training heben kann. Durch die Berechnung deiner Maximalkraft wirst du den Effekt deines Trainings verbessern und kannst das gewünschte Ziel in kurzer Zeit erreichen. Die App ist in der Lage, das Idealgewicht zu finden, um den Körper nicht zu viel belasten aber gleichzeitig keine Wiederholungen zu machen, ohne dass man Ergebnisse erzielt. Die Wiederholungsmaximum kann als Obergrenze verwendet werden, um die gewünschte Belastung für eine Übung zu bestimmen. 

## Workflow
Zu Beginn der Projektentwicklung wurde das Ablaufdiagramm erstellt.
![Ablaufdiagramm](./Mockups/workflow.png)

### Dateneingabe
Um deine maximale Stärke zu berechnen, musst du einige persönlichen Daten in die Anwendung eingeben, wie z.B das Gewicht, dass du gehoben hast und die entsprechenden Wiederholungen. Gib dein Ziel ein, das du erreichen möchtest. Da die App individuell angepasst ist, kannst du auch deine persönlichen Daten eingeben und für jeden Erfolg, den du erzielst, erhältst du einfache Benachrichtigung und du kannst auf die nächste Stufe fortsetzen. 

### Datenverarbeitung/Speicherung 

#### 1RM Calculator
```json
[
	{
		"gewicht": 25.5,
		"wiederholungen": 10
	},
	{
		"gewicht": 50,
		"wiederholungen": 5
	}
]
```

#### Training
```json
[
	{
		"1rm": {
			"gewicht": 25.5,
			"wiederholungen": 10
		},
		"bereich": "kraft",
		"anzahlTrainingsEinheiten": 5,
		"startDatum": "21.03.2020",
		"endDatum": "21.03.2020",
		"berechnung": {
			"gewicht": 20,
			"wiederholungen": 8
		},
		"fortschritt": ["22.03.2020", "23.03.2020", "25.03.2020"]
	},
	{
		"1rm": {
			"gewicht": 15,
			"wiederholungen": 20
		},
		"bereich": "ausdauer",
		"anzahlTrainingsEinheiten": 10,
		"startDatum": "21.03.2020",
		"endDatum": "21.03.2020",
		"berechnung": {
			"gewicht": 13,
			"wiederholungen": 15
		},
		"fortschritt": ["22.03.2020", "23.03.2020", "25.03.2020"]
		
	},
]
```

### Datenausgabe
Wenn du deine maximale Kraft berechnet hast, kannst du wissen, wie viel Gewicht und wie viele Wiederholungen du trainierst kannst, um deine gewünschtes Ziel zu erreichen. 

## Mockups
![Information](./Mockups/information.jpg)
![1RM](./Mockups/1rm_calculator.jpg)
![Training berechnen](./Mockups/training_berechnen.jpg)
![Tabelle Training](./Mockups/training_tabelle.jpg)
![Tracking auswählen](./Mockups/tracking_training_auswaehlen.jpg)
![Tracking](./Mockups/tracking.jpg)
![Resultate Cards](./Mockups/resultate_cards.jpg)
![Diagramm](./Mockups/diagramm.jpg)

## Optionale Erweiterungen
Es könnte noch ein Archievment Bereich ergänzt werden. Zum Beispiel könnte das Archievment "Buff Dude" freigeschalten werden wenn 5 Trainingseinheiten im Bereich Kraft erfolgreich absolviert wurden

## Installationsanleitung
Zuerst muss dieses Repository lokale auf dem PC vorhanden sein hierzu muss folgender Befehl ausgeführt werden:
```
git clone https://github.com/mili-git/prog2
```
Klont das Repository, das sich unter 'https://github.com/mili-git/prog2' befindet, auf die lokale Maschine. Das Original-Repo kann sich im lokalen Dateisystem oder auf einer Remote-Maschine befinden, die via HTTP zugänglich ist. 

Anschliessend muss sichergestellt sein, dass **Flask** und **Plotly** installiert sind.

> pip ist ein Werkzeug welches in Python3 vorinstalliert ist, es ermöglicht externe Pakete zu installieren und für meine Python Installation zu nutzen.

Um ein Paket zu installieren öffnet man die Konsole(Terminal) und gibt:
```
sudo pip3 install flask
sudo pip3 install plotly
```

Um nun die Webapplikation starten zu können, muss in den Ordner navigiert werden, welcher via dem **git clone** Befehl erzeugt wurde. Anschliessend kann die Webapplikation mit folgendem Befehl gestartet werden:
```
python start.py
```

## Validierung
- [x] Flussdiagramm
- [x]  1RM Calculator
  - [x] Es können nicht doppelte Einträge (gleiches Gewicht und  Wiederholungen vorhanden sein)
- [x] Training
  - [x] Es kann nicht das genau gleiche Training nochmals erfasst werden
  - [x] Berechnungsmethoden (Prozentsatz)
  - [x] Datumsformat für das Enddatum auf Deutsch 
- [x] Fortschritt rename auf Tracking 
  - [x] HTML umsetzen 
  - [x] Dropdown mit Daten befüllen 
  - [x] abspeichern
- [x] Resultate
  - [x] HTML umsetzen 
  - [x] Plotly implementieren 
  - [x] Sortiere die Trackingseinträge nach Datum (vom ältesten zum neusten)
  - [x] TODO löschen 
- [x] Layout
  - [x] Background hinzufügen
  - [x] App_Title setzen 






