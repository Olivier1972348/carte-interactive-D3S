# Carte interactive D3S

Ce projet transforme un fichier Excel maintenu manuellement en une carte web des postes ouverts aux élèves D3S. Le fonctionnement courant ne nécessite ni VS Code ni modification du code : il suffit de mettre à jour le tableau Excel puis de régénérer la carte.

## Mise à jour la plus simple sur Mac

1. Ouvrir `data/postes_d3s.xlsx`, onglet `Postes`.
2. Ajouter ou corriger les lignes du tableau sans renommer les colonnes ni l'onglet.
3. Enregistrer puis fermer Excel.
4. Double-cliquer sur `1_GENERER_LA_CARTE.command`.
5. Contrôler le résumé affiché et la carte ouverte dans le navigateur.

Lors de la première utilisation, le script crée `.venv` et installe Python localement pour le projet. Une connexion Internet est alors nécessaire. Python 3.11 ou plus récent est requis ; la version de référence est indiquée dans `.python-version`.

## Classeur de saisie

Le classeur a volontairement un seul onglet et 16 colonnes :

- indispensables : `Actif ?`, `Poste`, `Catégorie`, `Établissement(s)` ;
- localisation : `Lieu(x) du poste`, `Ville`, `Département`, `Région` ;
- géocodage : `FINESS`, `Latitude`, `Longitude` ;
- publication : `Date de parution`, `Source`, `Observations` ;
- corrections facultatives : `Type de structure`, `Type d'établissement`.

Règles importantes :

- `Actif ? = Non` conserve la ligne dans Excel mais l'exclut de la carte ; une cellule vide est considérée active ;
- le FINESS doit idéalement contenir 9 chiffres et suffit généralement à trouver les coordonnées ;
- latitude et longitude peuvent rester vides si le FINESS est reconnu ;
- sans FINESS reconnu, saisir latitude et longitude ;
- la date de parution alimente automatiquement les filtres mois/année ;
- les listes déroulantes du classeur évitent les variantes de catégories.

Le script `scripts/simplify_excel.py` sert uniquement à convertir un ancien export technique à 36 colonnes vers ce format. Il n'est pas nécessaire pour les mises à jour ordinaires.

## Contrôles après génération

Le résumé doit notamment afficher :

- les lignes lues ;
- les postes inactifs ou retirés exclus ;
- les postes valides avec coordonnées ;
- les postes sans coordonnées exploitables ;
- les doublons supprimés.

Consulter ensuite `output/postes_sans_coordonnees.csv`. Toute ligne présente doit être corrigée dans Excel avec un FINESS valable ou des coordonnées manuelles.

Dans la carte, tester la recherche, les filtres, les compteurs et l'ouverture d'une fiche poste.

## Fichiers produits et diffusion

La génération crée :

- `output/carte_d3s.html` et `output/index.html` : deux copies identiques de la carte ;
- `output/postes_valides.csv` : données réellement affichées ;
- `output/postes_sans_coordonnees.csv` : lignes à corriger ;
- les assets nécessaires, notamment le logo et la plaquette.

Pour une diffusion hors Render, transmettre le dossier `output` complet dans un ZIP. Ne pas envoyer seulement le fichier HTML : le logo et la plaquette sont des fichiers séparés. La carte nécessite aussi Internet pour charger Leaflet et le fond de carte.

Pour préparer le ZIP complet destiné au collègue, double-cliquer sur `3_CREER_ZIP_TRANSFERT.command`. L'archive créée à la racine exclut `.git`, `.venv`, les caches et les fichiers locaux inutiles.

## Utilisation en ligne de commande

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m unittest discover -v
python main.py
python scripts/check_build_output.py
```

Le build Render utilise simplement :

```bash
./build.sh
```

## Dépannage

- `Onglet 'Postes' introuvable` : ne pas renommer l'onglet Excel.
- `Aucun poste avec coordonnées exploitables` : renseigner un FINESS reconnu ou latitude/longitude.
- carte à zéro poste : vérifier `Actif ?`, les coordonnées et `output/postes_sans_coordonnees.csv`.
- script Mac bloqué par macOS : clic droit sur le fichier `.command`, puis `Ouvrir`.

La documentation de reprise complète est dans `docs/PROMPT_REPRISE_CODEX.md` et la procédure détaillée dans `docs/MISE_A_JOUR_DONNEES.md`.
