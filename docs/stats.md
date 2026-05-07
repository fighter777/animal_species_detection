# Statistiques Possibles

Ce document recense des pistes de statistiques exploitables pour le projet
`animal_species_detection`.

L'idee n'est pas de tout produire tout de suite, mais de garder une base large
de metriques potentielles a partir d'un pipeline:

- camera
- detection
- classification
- horodatage
- export des resultats

## Prerequis de journalisation

Pour pouvoir calculer beaucoup de statistiques ensuite, il est utile de stocker
au minimum:

- timestamp
- source video ou camera
- index de frame
- index de detection
- bounding box
- score detecteur
- label detecteur
- espece predite
- score de classification
- top-k complet si possible
- chemin de capture sauvegardee

## Volume global

- nombre total de frames lues
- nombre total de frames analysees
- nombre total de detections
- nombre total de classifications retenues
- nombre total de captures sauvegardees
- ratio `frames actives / frames analysees`
- ratio `detections / frames analysees`
- ratio `captures / detections`

## Detection

- score moyen du detecteur
- score median du detecteur
- score minimum du detecteur
- score maximum du detecteur
- distribution des scores detecteur
- nombre moyen de detections par frame
- nombre maximal de detections sur une frame
- nombre de frames avec plusieurs detections
- taux de detections sous seuil
- taille moyenne des bounding boxes
- surface moyenne des bounding boxes
- ratio surface box / surface image
- largeur moyenne des boxes
- hauteur moyenne des boxes
- distribution des tailles de boxes
- position moyenne des boxes dans le cadre
- heatmap des detections
- zones de l'image les plus frequentees
- stabilite des positions detectees dans le temps

## Classification

- espece top-1 la plus frequente
- top `N` especes observees
- nombre total de classes differentes detectees
- repartition des predictions par espece
- score moyen de classification par espece
- score median de classification par espece
- score min et max par espece
- variance des scores par espece
- distribution des top-1
- distribution des top-3
- distribution des top-5
- marge moyenne entre top-1 et top-2
- nombre de predictions ambiguës
- nombre de predictions a faible confiance
- nombre de predictions a forte confiance
- classes les plus instables
- classes les plus rarement observees

## Temps

- detections par heure
- detections par jour
- detections par semaine
- detections par mois
- activite par tranche de 5 minutes
- activite par tranche de 15 minutes
- activite par tranche de 30 minutes
- activite par tranche d'une heure
- heure moyenne de premiere detection
- heure moyenne de derniere detection
- pic quotidien d'activite
- pic hebdomadaire d'activite
- temps moyen entre deux detections
- temps median entre deux detections
- temps maximum sans detection

## Evenements et visites

Une visite peut etre estimee en regroupant plusieurs detections proches dans le
temps.

- nombre estime de visites
- nombre moyen de detections par visite
- duree moyenne d'une visite
- duree mediane d'une visite
- duree maximale d'une visite
- duree minimale d'une visite
- repartition des durees de visite
- espece majoritaire par visite
- nombre de visites par espece
- temps moyen entre deux visites d'une meme espece
- visites tres courtes
- visites longues
- jours avec le plus de visites

## Spatial et comportement apparent

- cote de l'image le plus frequente
- centre de gravite moyen des detections
- trajectoire approximative entre frames
- vitesse apparente moyenne d'un animal detecte
- oscillation des positions
- frequence d'entree par la gauche
- frequence d'entree par la droite
- frequence de sortie par la gauche
- frequence de sortie par la droite
- hauteur moyenne d'apparition dans l'image
- distance moyenne au centre du cadre
- occupation relative du cadre
- zones preferees selon l'espece

## Multi-animaux

- nombre de frames avec plusieurs animaux
- nombre moyen d'animaux par frame active
- maximum d'animaux observes sur une meme frame
- frequence des cooccurrences
- paires d'especes les plus observees ensemble
- espece la plus souvent observee seule
- espece la plus souvent observee avec d'autres
- chevauchement moyen des bounding boxes
- evenements de concurrence supposee

## Confiance et qualite

- distribution globale des scores de classification
- distribution globale des scores de detection
- proportion de detections robustes
- proportion de classifications robustes
- taux de predictions faibles
- taux de predictions moyennes
- taux de predictions fortes
- moments de la journee ou la confiance baisse
- impact de la taille de box sur la confiance
- impact du nombre d'animaux sur la confiance
- images les plus ambiguës
- jours avec la plus faible confiance moyenne

## Long terme

- evolution de la frequentation par semaine
- evolution de la frequentation par mois
- evolution de la diversite d'especes
- apparition de nouvelles especes
- disparition temporaire d'especes
- variation saisonniere des passages
- variation des horaires de passage
- tendance haussiere ou baissiere de certaines especes
- jours atypiques
- semaines atypiques

## Metriques techniques

- temps moyen de traitement par frame
- temps moyen de detection
- temps moyen de classification
- FPS moyen traite
- nombre de frames sautees
- temps moyen d'ecriture des resultats
- volume disque genere
- nombre moyen de captures par jour
- poids moyen des captures
- croissance du stockage dans le temps

## Metriques experimentales

- indice de diversite locale
- score de regularite par espece
- score de rarete relative
- indice d'agitation
- score d'activite journalier
- score d'intensite par plage horaire
- score de competition a la mangeoire
- score de surprise d'une observation
- similarite entre journees
- clustering de journees selon activite

## Remarques pratiques

- une detection n'est pas forcement une visite
- une visite n'est pas forcement un individu unique
- une espece predite n'est pas une verite terrain
- les statistiques doivent idealement distinguer:
  - les donnees brutes
  - les donnees filtrees
  - les evenements regroupes

## Recommandation de mise en oeuvre

Ordre raisonnable:

1. stocker large
2. produire un CSV brut propre
3. calculer les stats simples
4. ajouter la logique de regroupement en visites
5. seulement ensuite, produire des metriques plus expertes
