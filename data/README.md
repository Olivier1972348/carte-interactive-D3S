# Données source

## `postes_d3s.xlsx`

Source manuelle de la carte. Mettre à jour uniquement l'onglet `Postes` et conserver le nom du fichier, de l'onglet et des colonnes.

Les colonnes `Latitude` et `Longitude` sont facultatives si le `FINESS` est reconnu. Une ligne marquée `Actif ? = Non` reste archivée dans Excel mais n'est pas publiée.

## `referentiel_finess.csv`

Référentiel utilisé automatiquement pour transformer un numéro FINESS en coordonnées. Ne pas le modifier pendant une mise à jour ordinaire. Son remplacement doit conserver au minimum les colonnes `numero_finess_et`, `coord`, `sourcecoordet` et `raison_sociale`.
