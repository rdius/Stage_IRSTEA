# -*- coding: utf-8 -*-
import os
import glob,json
from osgeo import gdal, gdalconst
from osgeo.gdalconst import * 
import numpy as np


#Pilote pour la gestion du format raster ici GeoTiff
driver = gdal.GetDriverByName('GTiff')
driver.Register()

# Chemin d'accès à l'image
dossier = ("/media/rodrigues/New Volume/")


# Acces aux couches d'extension .tif du dossier source
directory = glob.glob(r"/media/rodrigues/New Volume/SENTINEL-2-10m_multi_band_area_seg/*.tif")
D={}

# lecture et ouverture de l'image
for filename in directory:
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
	id=0
	# recuperation de la valeur du pixel en fonction des coordonnees de l'image et du segment auquel il appartient
	for xcoord  in range( nb_cols):
		for ycoord in range(nb_rows):
			data = band.ReadAsArray(xcoord,ycoord,1,1) 
			# obj_id  represente l'id unique de chaque segment. 
			obj_id = data[0,0] #
			#verifier que obj_id n'existe pas dans la liste des segments deja sauvegarde
			if not((obj_id,periode) in data_container):
				#recuperation de l'identifiant du pixel tout en tenant compte de sa date d'acquisition et l'objet auquel il appartient
				data_container[obj_id,periode]=set()
			data_container[obj_id,periode].add(id)
			#incrementation de la valeur de id   136, 'SENTINEL2A_20160804'
			id+=1
			print "========"
			print data_container

#RQ: a la sortie, l'id de chaque pixel est associe a deux cles que sont son temps d'acquisition et son segement
