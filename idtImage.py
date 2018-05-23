import os
import csv
import time
from PIL import Image, ImageFont, ImageDraw

def testDispersion(minX, maxX, minY, maxY) :
	return ((maxX - minX) <= dispersion and (maxY - minY) <= dispersion)

listNameParticipant = [2]
screenWidth, screenHeight = 1484.0, 1050.0
dispersion = 60
duration = 1000
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
			file = open('../Participants/Participant ' + str(nameParticipant) + '/Ancrage/' + resumeName[8] +'_' + resumeName[4] + '_' + resumeName[5] + '_' + resumeName[6] + '_d' + str(dispersion) + '_t' + str(duration) + '.csv', "w")
			file.write('Id;Finger;X;Y;Duree;Start;Stop\n')
			
			img = Image.open("../data/" + resumeName[5] + ".png")
			#img = Image.open("../data/lapin2.png")
			img = img.convert("RGBA")
			img2 = Image.open("../data/transparent.png")
			img2 = img2.convert('RGBA')
			draw = ImageDraw.Draw(img2)
			font = ImageFont.truetype("arial.ttf", 26)

			# Ouvrir le fichier log ecran
			cr = csv.reader(open(nameDirectory + "/" + nameFiles,"r"), delimiter=';')	
			
			listofPoints = []
			# Range file csv in a array with coordinate and time
			for index, row in enumerate(cr): 
				if row[6] == 'Yellow' :
					coord = (int(row[10]), int(row[11]), int(row[5]))
					# check if coord is on the image
					if coord[0] > 0 and coord[1] > 0 and coord[0] < screenWidth and coord[1] < screenHeight :
						listofPoints.append(coord)
			
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
							pointFixation = (centerX, centerY, durationFixation)
							listFixationFound.append(pointFixation)
							file.write(str(numberFixation) + ';IndexGauche;' + str(centerX) + ';' + str(centerY) + ';' +  str(durationFixation) + ';' + str(listPointFixation[0][2]) + ';' + str(listPointFixation[-1][2]) + '\n')
							bbox = (centerX - circleLength, centerY - circleLength, centerX + circleLength, centerY + circleLength)
							draw.ellipse(bbox, fill = (255, 255, 0))
							draw.text((centerX, centerY), str(numberFixation),(0,0,255), font=font)
							numberFixation += 1
						
							# Remove window points from points
							cpt = indexStart + len(listPointFixation)
							del listPointFixation[:]

					# Remove first point to points	
					else :
						del listPointFixation[:]
						cpt = indexStart + 1	

							
			file.close()
			img3 = Image.alpha_composite(img, img2)
			if row[1] == 'ESC' :
				contexte = '1'
			elif row[1] == 'EAC' :
				contexte = '2'
			else :
				contexte = '3'
			img3.save("../Participants/Participant " + str(nameParticipant) + "/Fixation/" + row[0] + '_' + row[4] + '_' + row[3] + '_' + row[1] + '_d' + str(dispersion) + '_t' + str(duration) + '.png')
			
