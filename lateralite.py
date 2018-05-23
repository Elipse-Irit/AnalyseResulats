import os
import csv
from PIL import Image, ImageDraw

def main() :
	nameParticipant = '9'
	nameDirectory = '../Participants/Participant ' + nameParticipant + '/'
	screenWidth, screenHeight = 1484, 1050

	# Acceder dossier des fichiers du log camera
	nameDirectory = '../Participants/Participant ' + nameParticipant + '/Colors'
	directory = os.listdir(nameDirectory)
	sortedFilesColors = sorted(directory, key=lambda x: int(x.split('_')[4]))

	fileResume = open('../Participants/Participant ' + str(nameParticipant) + '/lateraliteResume.csv', "w")
	fileResume.write('Participant;Bloc;Categorie;NomTrial;NumTrial;Finger;PourcentageLeft;PourcentageRight\n')

	for nameFiles in sortedFilesColors :
		nameFileNewLog = nameFiles[:-4]
		resumeName = nameFileNewLog.split('_')
		print (nameFiles)

		# Ouvrir le fichier de log camera
		cr = csv.reader(open(nameDirectory + "/" + nameFiles,"rt"), delimiter=';')	
		file = open('../Participants/Participant ' + str(nameParticipant) + '/Ancrage/' + resumeName[8] +'_' + resumeName[4] + '_' + resumeName[5] + '_' + resumeName[6] + '_lateralite.csv', "w")
		file.write('Finger;Cote;Duree;Start;Stop\n')
		listofPoints = []
		
		# Range file csv in a array with coordinate and time
		for row in cr: 
			if row[6] == 'Yellow' :
				coord = (int(row[10]), int(row[11]), int(row[5]))
				# check if coord is on the image
				if coord[0] > 0 and coord[1] > 0 and coord[0] < screenWidth and coord[1] < screenHeight :
					listofPoints.append(coord)
	
		# Time spend in each part of diagram
		cpt = 0
		listTimeSpend = []
		startDurationLeft = 0
		startDurationRight = 0

		while (cpt + 1) < len(listofPoints) :
			x = listofPoints[cpt][0]
			if x < (screenWidth / 2) :
				startDurationLeft = listofPoints[cpt][2]
			else :
				startDurationRight = listofPoints[cpt][2]
			cpt = cpt + 1
			x = listofPoints[cpt][0]	
			
			while x < (screenWidth / 2) and (cpt + 1) < len(listofPoints):
				cpt = cpt + 1
				x = listofPoints[cpt][0]
			
			if startDurationLeft != 0 :
				if (cpt + 1) >= len(listofPoints) : 
					lastDurationLeft = listofPoints[cpt][2]
				else :
					lastDurationLeft = listofPoints[cpt - 1][2]
					startDurationRight = listofPoints[cpt][2]
				timeSpend = ('Left', (lastDurationLeft - startDurationLeft), startDurationLeft, lastDurationLeft)
				listTimeSpend.append(timeSpend)
				startDurationLeft = 0

			while x >= (screenWidth / 2) and (cpt + 1) < len(listofPoints):
				cpt = cpt + 1
				x = listofPoints[cpt][0]
				
			if startDurationRight != 0 :
				if (cpt + 1) >= len(listofPoints) : 
					lastDurationRight = listofPoints[cpt][2]
				else :
					lastDurationRight = listofPoints[cpt - 1][2]
				timeSpend = ('Right', (lastDurationRight - startDurationRight), startDurationRight, lastDurationRight)
				listTimeSpend.append(timeSpend)
				startDurationRight = 0
		
		cptTimeTotalLeft = 0
		cptTimeTotalRight = 0		
		for listT in listTimeSpend :
			if (listT[0] == 'Right') :
				cptTimeTotalRight = cptTimeTotalRight + listT[1]
			else :
				cptTimeTotalLeft = cptTimeTotalLeft + listT[1]
			file.write('IndexLeft' + ';' + str(listT[0]) + ';' + str(listT[1]) + ';' + str(listT[2]) + ';' + str(listT[3]) +'\n')		
		file.close()

		cptTimeTotalLeft = cptTimeTotalLeft / (listofPoints[-1][2] - listofPoints[0][2]) * 100
		cptTimeTotalRight = cptTimeTotalRight / (listofPoints[-1][2] - listofPoints[0][2]) * 100
		fileResume.write(row[0] + ';' + row[1] + ';' + row[2] + ';' + row[3] + ';' + row[4] + ';' + 'IndexLeft' + ';' + str(format(cptTimeTotalLeft, '.2f')) + ';' + str(format(cptTimeTotalRight, '.2f')) +'\n')

		del listTimeSpend[:]
		del listofPoints[:]

		
	fileResume.close()
if __name__ == "__main__":
    main()