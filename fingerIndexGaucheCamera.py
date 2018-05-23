import os
import csv
from PIL import Image, ImageDraw

def main() :
	#nameParticipant = '2'
	#nameDirectory = '../Participants/Participant ' + nameParticipant + '/'

	# Acceder dossier des fichiers du log camera
	#nameDirectory = '../Participants/Participant ' + nameParticipant + '/Colors'
	#directory = os.listdir(nameDirectory)
	#sortedFilesColors = sorted(directory, key=lambda x: int(x.split('_')[4]))

	# Taille des points pour log camera
	eX, eY = 14, 14

	#for nameFiles in sortedFilesColors :
	#resumeName = nameFiles.split('_')
	#print (nameFiles)
	# Ouvre le fichier de log camera
	fileColor = csv.reader(open("logs.csv","rt"), delimiter=',')

	# Ouvrir le fond de l'image 
	#img = Image.open("../data/" + resumeName[5] + ".png")
	img = Image.open("../data/dromadaire.png")
	img = img.convert("RGBA")
	draw = ImageDraw.Draw(img)

	first = True
	last = (0,0)
	# Parcourir le fichier log camera
	for index, row in enumerate(fileColor) :
		if index > 0 :
			x = int(row[8])
			y = int(row[9])
			if (row[6] == 'Yellow') :
				bbox = (x - eX, y - eY, x + eX, y + eY)
				if not first:
					draw.line((last[0], last[1], x, y), fill = (255, 255, 0), width=14)
				first = False
				last = (x,y)
	# Enregistre l'image
	if row[1] == 'ESC' :
			contexte = '1'
	elif row[1] == 'EAC' :
		contexte = '2'
	else :
		contexte = '3'
	#img.save("../Participants/Participant " + str(nameParticipant) + "/TraceParcours/" + row[0] + '_' + row[4] + '_' + row[3] + '_' + row[1] + '_Gauche.png')
	img.save('test.png')
if __name__ == "__main__":
    main()