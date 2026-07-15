# Mise à jour et publication des données D3S

## Mise à jour manuelle

1. Ouvrir `data/postes_d3s.xlsx`, onglet `Postes`.
2. Ajouter les nouveaux avis ou modifier les lignes existantes.
3. Pour retirer un poste sans perdre son historique, saisir `Non` dans `Actif ?`.
4. Renseigner le FINESS lorsque possible. Sinon, ajouter latitude et longitude.
5. Enregistrer et fermer Excel avant la génération.

Les quatre champs métier à toujours renseigner sont `Actif ?`, `Poste`, `Catégorie` et `Établissement(s)`. La date, la source et la localisation sont vivement recommandées.

## Génération et tests

Sur Mac, double-cliquer sur `1_GENERER_LA_CARTE.command`. En ligne de commande :

```bash
source .venv/bin/activate
python -m unittest discover -v
python main.py
python scripts/check_build_output.py
```

À la date de passation, le jeu fourni donne la référence suivante : 297 lignes lues, 10 retraits exclus, 285 postes valides, 0 sans coordonnées, 2 doublons supprimés.

Vérifier systématiquement :

- `output/postes_sans_coordonnees.csv` ;
- les compteurs et filtres de la carte ;
- quelques fiches au hasard, notamment les nouvelles ;
- que `output/index.html` et `output/carte_d3s.html` sont identiques.

## Publication Render

Le dépôt est configuré par `render.yaml` comme site statique. `./build.sh` installe les versions Python fixées, lance les tests, régénère les sorties et exécute le contrôle final. Un push sur `main` déclenche normalement le redéploiement automatique.

```bash
git status
git diff --check
git add data output
git commit -m "Update D3S map data"
git push origin main
```

Ne publier qu'après contrôle manuel. Vérifier au préalable que le dépôt et les données peuvent être publics.

## Diffusion directe

Compresser et transmettre le dossier `output` complet. Le HTML seul ne contient ni le logo ni la plaquette. Une connexion Internet reste nécessaire pour les bibliothèques Leaflet et les tuiles cartographiques.

## Ancien classeur technique

Pour convertir une ancienne version contenant `Postes_enrichis`, `FINESS_retrouves`, `A_controler`, etc. :

```bash
python scripts/simplify_excel.py --input ancien.xlsx --output nouveau.xlsx
```

Contrôler le nouveau fichier avant de remplacer `data/postes_d3s.xlsx`.

## Points restant à traiter

- remplacer `output/plaquette-promo.pdf` par la plaquette officielle si le fichier fourni est encore le PDF provisoire ;
- documenter la date, la source et la licence de chaque mise à jour du référentiel FINESS ;
- si un fonctionnement totalement hors ligne devient nécessaire, héberger localement Leaflet, MarkerCluster et un fond cartographique adapté.
