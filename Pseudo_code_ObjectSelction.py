
##########################################
# Dans cette partie, je decris en premier lieu le pseudo code 
#	pour la selection automatique des objets 
#
#######################################

#Initialisation
Soit Obj la liste contenant les segments
Soit  α le seuil dacceptation de chevauchement entre deux objets 
Soit obj designant tout objet element de Objects
#Definition d'une fonction a deux parametres pour la generation automatique des segments

Function SelectionObjet (Obj,α)
	EnsembleSegments= Obj # recuperation des segments en entree
	PCA= ∅ #initialisation de pca (pixel already covered) comme ensemble vide
	weight= 0 #le poids pour recevoir le poids du current obj 
	WHILE  Obj > 0 DO #Tant que la liste des segments n'est pas vide, on execute l'action
		maxWeight #
		FOR obj IN Obj  DO #pour tout objet dans la liste des objets, faire
			novelty(obj) = |poids(obj) - poids(PCA))|/poids(obj) # calcul du poids de nouveaute pour chaque objet
			IF novelty(obj) = 1 THEN  #si la nouveaute est egal a 1, 
			 	weight =  poids(obj) # alors le poids de l'objet a prendre = poids de l'objet courant
			ELSE IF α <= novelty(obj) < 1# si la nouveaute de l'objet courant est comprise entre α et 1
				weight = novelty(obj) # alors le poids de l'objet a prendre = poids de l'objet dont les elements sont nouveaux 
			END IF #
			IF  novelty(obj) < α # si la nouveaute de l'objet courant  < α, 
				Obj = Obj - obj #alors, on suprime l'objet courant de la liste des objets
			ELSE IF #
				weight > maxWeight THEN #si le poids de l'ensemble des objets deja selectionne est plus grand que que celui du poids max
				maxWeight = weight #alors, poids max prend la valeur du poids actuel
			END IF #
		END FOR	
		PCA= maxWeight # la liste des pixels deja couverts recoit le poids max , c-a-d le nombre total des objets admissibles
	END WHILE

	RETURN PCA #retourne le pca qui represente l'ensemble final des objets
#END FUNCTION

			

