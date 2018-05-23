import os
import csv
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.ndimage.filters import gaussian_filter
from PIL import Image, ImageDraw


def myplot(histo, s):
    heatmap = gaussian_filter(histo, sigma=s) 
    return heatmap

nameParticipant = '2'

# Acceder dossier des fichiers du log camera
nameDirectory = '../Participants/Participant ' + nameParticipant + '/Colors'
directory = os.listdir(nameDirectory)
sortedFilesColors = sorted(directory, key=lambda x: int(x.split('_')[4]))


sigmas = [8, 16]

for nameFiles in sortedFilesColors :
	resumeName = nameFiles.split('_')
	
	fileColor = csv.reader(open(nameDirectory + "/" + nameFiles,"r"), delimiter=';')	

	histo = []
	for y in range(0, 1050) :
		temp = []
		for x in range(0, 1484) : 
			temp.append(0) 
		histo.append(temp)

	for index, row in enumerate(fileColor) :
		if index > 0 :
			x = int(row[10])
			y = int(row[11])
			if x > 0 and y > 0 and y < 1051 and x < 1485 :
				if (row[6] == 'Yellow') :
					histo[y][x] += 50000 
		
	for s in sigmas:
		img = myplot(histo, s)				
		plt.imsave("../Participants/Participant " + str(nameParticipant) + "/HeatMap/" + row[0] + '_' + row[4] + '_' + row[3] + '_' + row[1] + '_Gauche_v' + str(s) + '.png', img, origin='upper', cmap=cm.jet)

		# Ouvrir le fond de l'image 
		imgHeatMap = Image.open("../Participants/Participant " + str(nameParticipant) + "/HeatMap/" + row[0] + '_' + row[4] + '_' + row[3] + '_' + row[1] + '_Gauche_v' + str(s) + '.png')
		imgHeatMap = imgHeatMap.convert("RGB")

		#imgToDraw = Image.open("../data/lapin2.png")
		imgTrack = Image.open("../Participants/Participant " + str(nameParticipant) + "/TraceParcours/" + row[0] + '_' + row[4] + '_' + row[3] + '_' + row[1] + '_Gauche.png')
		imgTrack = imgTrack.convert("RGBA")

		imgHMWithTranparency = Image.new(imgTrack.mode, imgTrack.size)
		imgHMWithTranparency = imgHMWithTranparency.convert("RGBA")
		
		(l, h) = imgHeatMap.size
		for y in range(h):
			for x in range(l) : 
				r, g, b = imgHeatMap.getpixel((x, y))
				#if r == 0 and g == 0 and b > 230 :
				if (r, g, b) != (0, 0, 127) and (r, g, b) != (0, 0, 132) and (r, g, b) != (0, 0, 136) and (r, g, b) != (0, 0, 141) and (r, g, b) != (0, 0, 145) and (r, g, b) != (0, 0, 150) and (r, g, b) != (0, 0, 154) and (r, g, b) != (0, 0, 159) and (r, g, b) != (0, 0, 163) and (r, g, b) != (0, 0, 168) and (r, g, b) != (0, 0, 172) and (r, g, b) != (0, 0, 177) and (r, g, b) != (0, 0, 182) and (r, g, b) != (0, 0, 186) and (r, g, b) != (0, 0, 191) and (r, g, b) != (0, 0, 195) and (r, g, b) != (0, 0, 200) and (r, g, b) != (0, 0, 204) and (r, g, b) != (0, 0, 209) and (r, g, b) != (0, 0, 213) and (r, g, b) != (0, 0, 218) and (r, g, b) != (0, 0, 222)  and (r, g, b) != (0, 0, 227)  and (r, g, b) != (0, 0, 232)  and (r, g, b) != (0, 0, 236)  and (r, g, b) != (0, 0, 241) and (r, g, b) != (0, 0, 245) and (r, g, b) != (0, 0, 250) and (r, g, b) != (0, 0, 254) and (r, g, b) != (0, 0, 255) and (r, g, b) != (0, 4, 255) and (r, g, b) != (0, 8, 255) and (r, g, b) != (0, 12, 255) and (r, g, b) != (0, 16, 255) and (r, g, b) != (0, 20, 255) and (r, g, b) != (0, 24, 255) and (r, g, b) != (0, 28, 255) and (r, g, b) != (0, 32, 255) and (r, g, b) != (0, 36, 255) and (r, g, b) != (0, 40, 255) and (r, g, b) != (0, 44, 255) and (r, g, b) != (0, 48, 255) and (r, g, b) != (0, 52, 255) and (r, g, b) != (0, 56, 255) and (r, g, b) != (0, 60, 255) and (r, g, b) != (0, 64, 255) and (r, g, b) != (0, 68, 255) and (r, g, b) != (0, 72, 255) and (r, g, b) != (0, 76, 255) and (r, g, b) != (0, 80, 255):
					#print(r,g,b)
					#time.sleep(1)
					imgHMWithTranparency.putpixel((x,y), (r,g,b))
		img3 = Image.alpha_composite(imgTrack, imgHMWithTranparency)
		
		os.remove("../Participants/Participant " + str(nameParticipant) + "/HeatMap/" + row[0] + '_' + row[4] + '_' + row[3] + '_' + row[1] + '_Gauche_v' + str(s) + '.png')	
		img3.save("../Participants/Participant " + str(nameParticipant) + "/HeatMap/" + row[0] + '_' + row[4] + '_' + row[3] + '_' + row[1] + '_Gauche_v' + str(s) + '.png')
	del histo[:]

