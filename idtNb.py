import os
import csv
import time
from PIL import Image, ImageFont, ImageDraw

def testDispersion(minX, maxX, minY, maxY) :
	return ((maxX - minX) <= dispersion and (maxY - minY) <= dispersion)

listNameParticipant = [2,3,5,7,9]
screenWidth, screenHeight = 1484.0, 1050.0
totalDispersion = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110]
totalDuration = [300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500]
circleLength = 6
# ************************ Main ************************
if __name__ == "__main__":
	for nameParticipant in listNameParticipant :
		
		nameDirectory = '../Participants/Participant ' + str(nameParticipant) + '/Colors'
		nameDirectoryRoot = '../Participants/Participant ' + str(nameParticipant) + '/'
		directory = os.listdir(nameDirectory)
		sortedFilesColors = sorted(directory, key=lambda x: int(x.split('_')[4]))
		
		for nameFiles in sortedFilesColors :

			# Fichier pour enregistrer temps ancrage
			nameFileNewLog = nameFiles.replace("LogsColor", "Ancrage")
			nameFileNewLog = nameFiles[:-4]
			resumeName = nameFileNewLog.split('_')
			file = open('../Participants/Participant ' + str(nameParticipant) + '/resumeFixation.csv', "w")
			file.write('Duration;Dispersion;NumberFixation\n')
			
			# Ouvrir le fichier log ecran
			cr = csv.reader(open(nameDirectory + "/" + nameFiles,"rt"), delimiter=';')	
			
			listofPoints = []
			# Range file csv in a array with coordinate and time
			for index, row in enumerate(cr): 
				if row[6] == 'Yellow' :
					coord = (int(row[10]), int(row[11]), int(row[5]))
					# check if coord is on the image
					if coord[0] > 0 and coord[1] > 0 and coord[0] < screenWidth and coord[1] < screenHeight :
						listofPoints.append(coord)
			
			for duration in totalDuration :			
				for dispersion in totalDispersion :
					cpt = 0
					indexStart = 0
					numberFixation = 1
					listPointFixation = []
					listFixationFound = []

					while (cpt + 1) < len(listofPoints) :
						currentPoint = listofPoints[cpt]
						startDuration = currentPoint[2]
						indexStart = cpt
						listPointFixation.append(currentPoint)
						
						cpt = cpt + 1
						nextPoint = listofPoints[cpt]
						
						# Initialize window over points to cover duration 
						while (startDuration + duration) > nextPoint[2] and (cpt + 1) < len(listofPoints) :
							listPointFixation.append(nextPoint)
							cpt = cpt + 1
							nextPoint = listofPoints[cpt]

						if (cpt + 1) < len(listofPoints) :
													
							# Initialization coordinate of window points
							coordWindowPoints = ((min(listPointFixation, key=lambda x: x[0]))[0], (min(listPointFixation, key=lambda x: x[1]))[1],
												 (max(listPointFixation, key=lambda x: x[0]))[0], (max(listPointFixation, key=lambda x: x[1]))[1])
							
							# If dispersion of window points <= threshold
							if testDispersion(coordWindowPoints[0], coordWindowPoints[2], coordWindowPoints[1], coordWindowPoints[3]) :
													
								# Add additional points to the window until dispersion > threshold
								while testDispersion(min(coordWindowPoints[0], nextPoint[0]), max(coordWindowPoints[2],nextPoint[0]), min(coordWindowPoints[1], nextPoint[1]), max(coordWindowPoints[3], nextPoint[1])) and (cpt + 1) < len(listofPoints) :
									listPointFixation.append(nextPoint)
									coordWindowPoints = (min(coordWindowPoints[0], nextPoint[0]), min(coordWindowPoints[1], nextPoint[1]),
												 	 	 max(coordWindowPoints[2], nextPoint[0]), max(coordWindowPoints[3], nextPoint[1]))
									cpt = cpt + 1
									nextPoint = listofPoints[cpt]
								
								if (cpt + 1) >= len(listofPoints) :
									# Test the last position
									if testDispersion(min(coordWindowPoints[0], nextPoint[0]), max(coordWindowPoints[2],nextPoint[0]), min(coordWindowPoints[1], nextPoint[1]), max(coordWindowPoints[3], nextPoint[1])) :
										listPointFixation.append(nextPoint)
										coordWindowPoints = (min(coordWindowPoints[0], nextPoint[0]), min(coordWindowPoints[1], nextPoint[1]),
												 	 		 max(coordWindowPoints[2], nextPoint[0]), max(coordWindowPoints[3], nextPoint[1]))											
									
								# Note a fixation at the centroid of the window points
								centerX = coordWindowPoints[0] + (coordWindowPoints[2] - coordWindowPoints[0]) / 2
								centerY = coordWindowPoints[1] + (coordWindowPoints[3] - coordWindowPoints[1]) / 2
								
								durationFixation = listPointFixation[-1][2] - listPointFixation[0][2]
								if durationFixation < duration : 
									# Remove window points from points
									cpt = indexStart + 1
									del listPointFixation[:]
								else :	
									numberFixation += 1
								
									# Remove window points from points
									cpt = indexStart + len(listPointFixation)
									del listPointFixation[:]

							# Remove first point to points	
							else :
								del listPointFixation[:]
								cpt = indexStart + 1	
					file.write(str(duration) + ';' + str(dispersion) + ';' + str(numberFixation) + '\n')
			file.close()