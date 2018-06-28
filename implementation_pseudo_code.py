# -*- coding: utf-8 -*-
import os
import glob
from osgeo import gdal, gdalconst
from osgeo.gdalconst import * 
import numpy as np

#fonction de recuperation de tous les segments de lensemble des images
def allSegment(filename):
	current_image = gdal.Open(filename, GA_ReadOnly)	
	# recuperation de la 1re bande
	band = current_image.GetRasterBand(1)	
	# nombre de lignes et colonnes
	nb_cols= current_image.RasterXSize
	nb_rows = current_image.RasterYSize
	#filename_array=current_image.ReadAsArray()
	#affichage du nombre de ligne et de colonne
	print nb_cols, nb_rows
	#affichage de la taille de l'image
	current_image_size=  nb_cols*nb_rows
	# recuperation du nom de fichier
	chemin, filenam = os.path.split(filename)	
	# recuperation du nom du fichier sans extension
	filenam = filenam.split('.tif')[0]	
	#recuperation de la partie du nom du fichier representant sa periode d'acquisition
	periode=filenam.split("-")[0]	
	#structure de donnees dans laquelle sera stockee et les dates d'acquisiton, et les ids des segments et les ids des pixels qui s'y trouvent	
	data_container={}
	# recuperation des ids de chaque pixel de limage
	id=0 
	# recuperation de la valeur du pixel en fonction des coordonnees de l'image et du segment auquel il appartient
	for xcoord  in range( nb_cols):
		for ycoord in range(nb_rows):
			data = band.ReadAsArray(xcoord,ycoord,1,1) 
			# obj_id  represente l'id unique de chaque segment.identique aux valeurs obtenues avec np.unique(filename.ReadAsArray())
			obj_id = data[0,0] 
			#verifier que obj_id n'existe pas dans la liste des segments deja sauvegarde
			if not((obj_id,periode) in data_container):
				#recuperation de l'identifiant du pixel tout en tenant compte de sa date d'acquisition et l'objet auquel il appartient
				data_container[obj_id,periode]=set()
			#ajout de chaque nouveau id
			data_container[obj_id,periode].add(id)
			#incrementation de la valeur de id   
			id+=1	
	# retourner le contenu de data_container, c-a-d le dictionnaire contenant les ids des pixels avec le segment et l'image auxquels ils appartiennent 
	return data_container


# fonction de selection objets prenant en entree l'ensemble des objets et la valeur de alpha
def  SelectionObjet (Obj,a): # 
	Obj= Obj #structure contenant tous les objets des differentes periodes
	PAC= set() # pac ou pixels deja selectionnes, regroupes les pixels des objets deja selectionnes	
	allSelectedObj= {} # structure contenant tous les objets candidats
	# tant que la liste est pas vide, on repete l'instruction sur les conditions de selection
	while len(Obj) >0 :
		# represente le poids de l'objet selectionne a chaque iterration
		max_weight=0 
		
		#Objet de reference ou objet candidat init
		objsref=None 		
		#Obj2 represente une copy de Obj,
		Obj2=Obj.copy()  
		#parcours de tous les objets 
		for (obj_id,periode) in Obj:				
			#print type(Obj[(obj_id,periode)])
			#print "pac", len(PAC)
			# evaluation de l'intersection de l'objet courant par rapport aux objets deja selectionnes ou pac
			intersect= Obj[(obj_id,periode)].intersection(PAC) 
			# verifier sil y a intersection entre les pixels de l'objet courant avec ceux deja sauvegardes dans pac
			if  len(intersect)==0:
				# si pas d'intersection, alors on stock le poids de cet objet
				weight= len(Obj[(obj_id,periode)])
			# s'il y a intersection, alors on calcule le poids de l'insection
			else:
				weight = (len(Obj[(obj_id,periode)]) - len(PAC))/len(Obj[(obj_id,periode)])
				#print "weight" , weight
			# si le poids obtenu est inferieur a la valeur seuil 'a' fixee, alors l'objet correspondant est suprime de la liste
			if weight <= a:
				del Obj2[(obj_id,periode)]
			#print weight
			# si le poids de l'objet courant est superieur a tous les poids obtenu usque la, alors poids on met a jour la valeur de poids max
			if weight > max_weight : #
				max_weight = weight #
				# on recupere la cle de lobjet ayant le plus grand poids 
				objsref= (obj_id,periode)
				#objsref= PAC
		#mise a jour de lensemble Obj pour itteration suivante
		Obj=Obj2.copy() 
		
		#verification du contenu de la liste qui recupere les objets candidats
		if objsref !=None:			
			#Sprint Obj[(objsref)]
			# recuperation de l'objet candidat dans allSelectedObj
			allSelectedObj[objsref]=Obj[(objsref)]	 			
			# ajout de l'objet selectionne dans la liste pac
			PAC=PAC.union(Obj[objsref])
			
			#suprimer l'objet qu'il ai ete retenu comme objet candidat
			del Obj[objsref]
			#candidate_segment=candidate_segment.union(objs)
	print "PCA value", len(PAC)
	# renvoi de tous les objets candidats
	return allSelectedObj
	
# fonction main	
if __name__ == '__main__':	
	#directory = glob.glob(r"/media/rodrigues/New Volume/SENTINEL-2-10m_multi_band_area_seg/*tif")
	#lecture des images 
	directory = glob.glob(r"/media/rodrique/DATA/test_data/*.tif")
	allSegmentObject={}
	# parcours de chaque image 
	for i in directory:
		#appel de la fonction allSegment et execution pour chaque image
		allSegments=allSegment(i)
		#ajout et mise a jour de la structure contenant l'ensemble des objets
		allSegmentObject.update(allSegments)
		#print allSegments
	# appel de la fonction de selection des objets canditats avec le parametre alpha
	selected_region = SelectionObjet(allSegmentObject, 0.8)
	# affichage du nombre d'objets candidats obtenus 
	print "nombre de region ", len(selected_region)

