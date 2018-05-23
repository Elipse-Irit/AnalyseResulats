import os
import csv
from PIL import Image, ImageDraw

def main() :
	nameParticipant = '2'
	nameDirectory = '../Participants/Participant ' + nameParticipant + '/'

	# Acceder dossier des fichiers du log camera
	nameDirectory = '../Participants/Participant ' + nameParticipant + '/Colors'
	directory = os.listdir(nameDirectory)
	sortedFilesColors = sorted(directory, key=lambda x: int(x.split('_')[4]))

	# Taille des points pour log camera
	eX, eY = 8, 8

	for nameFiles in sortedFilesColors :
		resumeName = nameFiles.split('_')
		print nameFiles
		# Ouvre le fichier de log camera
		fileColor = csv.reader(open(nameDirectory + "/" + nameFiles,"rb"), delimiter=';')

		# Ouvrir le fond de l'image 
		img = Image.open("../data/" + resumeName[5] + ".png")
		img = img.convert("RGBA")
		draw = ImageDraw.Draw(img)

		first = True
		last = (0,0)
		# Parcourir le fichier log camera
		for index, row in enumerate(fileColor) :
			if index > 0 :
				x = int(row[10])
				y = int(row[11])
				if (row[6] == 'Green') :
					bbox = (x - eX/2, y - eY/2, x + eX/2, y + eY/2)
					if not first:
						draw.line((last[0], last[1], x, y), fill = (0, 255, 0), width=4	)
					first = False
					last = (x,y)
		# Enregistre l'image
		if row[1] == 'ESC' :
				contexte = '1'
		elif row[1] == 'EAC' :
			contexte = '2'
		else :
			contexte = '3'
		img.save("../Participants/Participant " + str(nameParticipant) + "/TraceParcours/" + row[0] + '_' + row[4] + '_' + row[3] + '_' + row[1] + 'Majeur_Gauche.png')
if __name__ == "__main__":
    main()