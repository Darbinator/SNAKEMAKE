#!/usr/bin/env python

#############
#
#
# Calcul du RPKM de chaque gène à partir d'un fichier de comptage généré par featuresCounts
#
# RPKM (reads per kilobase of exon model per million mapped reads) accounts for both library size
# and gene length effects in within-sample comparisons
#
#
#############

import sys
import os
import re
import subprocess
import glob
from collections import defaultdict


featureCounts = open(sys.argv[1],"r")

# lignes récupère chaque ligne du fichier sous forme d'une liste
lignes = featureCounts.readlines()

# On initialise un dictionnaire qui récupère chaque échantillon (2ème ligne du fichier featureCounts"[1], 
# et à partir de la 7ème colonne "[6:]")

sample_to_total_reads = defaultdict(int)

[sample_to_total_reads[sample] for sample in range(len(lignes[1].rstrip().split()[6:]))]


# Pour calculer le nombre total de reads comptés dans chaque alignement
# A chaque ligne le compteur "sample" se déplace pour récuperer le nombre de reads
# pour un gène, et implémente la valeur dans le dictionnaire sample_to_total_reads

for ligne in lignes[2:]:
	for sample in range(len(ligne.rstrip().split()[6:])):

		sample_to_total_reads[sample] += int(ligne.rstrip().split()[6:][sample])
		

# Ouverture du fichier qui va générer la matrice avec les valeurs de RPKM

with open("RPKM.txt", "w") as RPKM:

	# Header dui fichier avec le nom des échantillons
	# On accède au nom des échantillons dans la 2ème ligne du fichier généré par featureCounts (lignes[1])
	RPKM.write("\t")
	for sample in lignes[1].rstrip().split()[6:]:
		RPKM.write(sample+"\t")
	RPKM.write("\n")



	# Pour chaque gène (à partir de lignes[2:]), on calcule le RPKM pour chaque échantillon et on ajoute la valeur dans le fichier et dans la bonne colonne
	#
	for ligne in lignes[2:]:
		RPKM.write(ligne.rstrip().split()[0]+"\t")
		for sample in range(len(ligne.rstrip().split()[6:])):

			#        RPKM = nombre de reads compté pour un échantillon    longueur du gène (6ème colonne du fichier) / 1000       nombre total de reads de l'échantillon / 1e6
			RPKM.write(str(int(ligne.rstrip().split()[6:][sample]) / ((int(ligne.rstrip().split()[5]) / 1000) * (int(sample_to_total_reads[sample])) / 1e6 ))+"\t")
		RPKM.write("\n")









