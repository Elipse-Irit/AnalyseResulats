import os
import csv

def main() :
	listExpert = [2,3]
	listNonExpert = [5,7,9]
	numberParticipant = 1

	# Ouvre le fichier lateralite resume
	nameDirectory = '../Results/Lateralite/lateraliteResume.csv'
	file = csv.reader(open(nameDirectory,"rt"), delimiter=';')

	# Cree les fichiers resumer expert, contexte, diagrammes
	fileResumeExpert = open('../Results/Lateralite/lateralite_resume_expert.csv', "w")
	fileResumeContext = open('../Results/Lateralite/lateralite_resume_context.csv', "w")
	fileResumeDiagrams = open('../Results/Lateralite/lateralite_resume_diagram.csv', "w")

	meanExpertL = 0
	meanExpertR = 0
	meanNonExpertL = 0
	meanNonExpertR = 0

	meanESCL = 0
	meanESCR = 0
	meanEACL = 0
	meanEACR = 0
	meanEACQL = 0
	meanEACQR = 0

	meanDrawingL = 0
	meanDrawingR = 0
	meanPerspectiveDrawingL = 0
	meanPerspectiveDrawingR = 0
	meanGraphL = 0
	meanGraphR = 0
	meanGMapL = 0
	meanGMapR = 0
	meanNMapL = 0
	meanNMapR = 0

	for index, row in enumerate(file):
		if index > 0 :
			# 1) Compare suivant l'expertise
			if row[0] in listExpert :
				meanExpertL = meanExpertL + float(row[6])
				meanExpertR = meanExpertR + float(row[7])
			else : 
				meanNonExpertL = meanNonExpertL + float(row[6])
				meanNonExpertR = meanNonExpertR + float(row[7])

			# 2) Compare suivant le contexte
			if row[1] == 'ESC' :
				meanESCL = meanESCL + float(row[6])
				meanESCR = meanESCR + float(row[7])
			elif row[1] == 'EAC' :
				meanEACL = meanEACL + float(row[6])
				meanEACR = meanEACR + float(row[7])
			else :
				meanEACQL = meanEACQL + float(row[6])
				meanEACQR = meanEACQR + float(row[7])

			# 3) Compare suivant les diagrammes
			if row[2] == 'dessins' :
				meanDrawingL = meanDrawingL + float(row[6])
				meanDrawingR = meanDrawingR + float(row[7])
			elif row[2] == 'dessins en perspective' :
				meanPerspectiveDrawingL = meanPerspectiveDrawingL + float(row[6])
				meanPerspectiveDrawingR = meanPerspectiveDrawingR + float(row[7])
			elif row[2] == 'graphes' :
				meanGraphL = meanGraphL + float(row[6])
				meanGraphR = meanGraphR + float(row[7])
			elif row[2] == 'cartes' :
				meanGMapL = meanGMapL + float(row[6])
				meanGMapR = meanGMapR + float(row[7])
			else :
				meanNMapL = meanNMapL + float(row[6])
				meanNMapR = meanNMapR + float(row[7])

	fileResumeExpert.write('Expertise;Left;Right\n')
	fileResumeContext.write('Context;Left;Right\n')
	fileResumeDiagrams.write('Diagrams;Left;Right\n')

	meanExpertL = meanExpertL / (30 * len(listExpert))
	meanExpertR = meanExpertR / (30 * len(listExpert))
	meanNonExpertL = meanNonExpertL / (30 * len(listNonExpert))
	meanNonExpertR = meanNonExpertR / (30 * len(listNonExpert))

	meanESCL = meanESCL / (6 * numberParticipant)
	meanESCR = meanESCR / (6 * numberParticipant)
	meanEACL = meanEACL / (6 * numberParticipant)
	meanEACR = meanEACR / (6 * numberParticipant)
	meanEACQL = meanEACQL / (6 * numberParticipant)
	meanEACQR = meanEACQR / (6 * numberParticipant)

	meanDrawingL = meanDrawingL / (10 * numberParticipant)
	meanDrawingR = meanDrawingR / (10 * numberParticipant)
	meanPerspectiveDrawingL = meanPerspectiveDrawingL / (10 * numberParticipant)
	meanPerspectiveDrawingR = meanPerspectiveDrawingR / (10 * numberParticipant)
	meanGraphL = meanGraphL / (10 * numberParticipant)
	meanGraphR = meanGraphR / (10 * numberParticipant)
	meanGMapL = meanGMapL / (10 * numberParticipant)
	meanGMapR = meanGMapR / (10 * numberParticipant)
	meanNMapL = meanNMapL / (10 * numberParticipant)
	meanNMapR = meanNMapR / (10 * numberParticipant)

	fileResumeExpert.write('Expert' + ';' + str(format(meanExpertL, '.2f')) + ';' + str(format(meanExpertL, '.2f')) +'\n')
	fileResumeExpert.write('Non-Expert' + ';' + str(format(meanNonExpertL, '.2f')) + ';' + str(format(meanNonExpertR, '.2f')) +'\n')

	fileResumeContext.write('ESC' + ';' + str(format(meanESCL, '.2f')) + ';' + str(format(meanESCR, '.2f')) +'\n')
	fileResumeContext.write('EAC' + ';' + str(format(meanEACL, '.2f')) + ';' + str(format(meanEACR, '.2f')) +'\n')
	fileResumeContext.write('EACQ' + ';' + str(format(meanEACQL, '.2f')) + ';' + str(format(meanEACQR, '.2f')) +'\n')

	fileResumeDiagrams.write('Dessins' + ';' + str(format(meanDrawingL, '.2f')) + ';' + str(format(meanDrawingR, '.2f')) +'\n')
	fileResumeDiagrams.write('Dessins en perspective' + ';' + str(format(meanPerspectiveDrawingL, '.2f')) + ';' + str(format(meanPerspectiveDrawingR, '.2f')) +'\n')
	fileResumeDiagrams.write('Graphes' + ';' + str(format(meanGraphL, '.2f')) + ';' + str(format(meanGraphR, '.2f')) +'\n')
	fileResumeDiagrams.write('Cartes' + ';' + str(format(meanGMapL, '.2f')) + ';' + str(format(meanGMapR, '.2f')) +'\n')
	fileResumeDiagrams.write('Plans' + ';' + str(format(meanNMapL, '.2f')) + ';' + str(format(meanNMapR, '.2f')) +'\n')

	fileResumeExpert.close()
	fileResumeContext.close()
	fileResumeDiagrams.close()

if __name__ == "__main__":
    main()