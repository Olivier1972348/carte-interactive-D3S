# Prompt de reprise à transmettre au collègue

Copier-coller tout le bloc ci-dessous dans Codex après avoir ouvert/décompressé le projet. Le collègue peut remplacer les éléments entre crochets s'il dispose d'informations nouvelles.

---

Je reprends la maintenance du projet « Carte interactive D3S » transmis par un collègue. Le dossier complet du projet est ouvert dans mon workspace. Je veux que tu m'accompagnes comme mainteneur technique autonome, en préservant les données et le fonctionnement existants.

## Finalité du projet

Le projet publie une carte interactive des postes ouverts aux élèves directeurs d'établissement sanitaire, social et médico-social (D3S). Une personne non développeuse doit pouvoir mettre à jour un classeur Excel, générer la carte sur Mac puis la publier ou la transmettre.

## État de référence au 15 juillet 2026

- Source manuelle : `data/postes_d3s.xlsx`, onglet strictement nommé `Postes`.
- Le classeur contient 297 lignes historiques dans un tableau Excel de 16 colonnes.
- 10 lignes marquées `Actif ? = Non` sont conservées pour l'historique et exclues automatiquement.
- Après exclusion et dédoublonnage : 285 postes publiés, 0 sans coordonnées exploitables, 2 doublons supprimés.
- Parmi les postes publiés, 278 sont géocodés via FINESS et 7 utilisent des coordonnées manuelles de repli.
- Sortie publique : `output/index.html` ; copie de diffusion : `output/carte_d3s.html`.
- Déploiement : site statique Render décrit par `render.yaml`, normalement relié à la branche `main` du dépôt `https://github.com/m1k124/ED3S_Map_2026`.
- Python fixé par `.python-version` à 3.13.3 ; dépendances exactes dans `requirements.txt`.

Considère ces nombres comme une référence de non-régression pour le jeu de données transmis, pas comme des valeurs permanentes : ils changeront lorsque j'ajouterai ou retirerai des postes.

## Architecture à comprendre avant toute modification

Le flux est :

`data/postes_d3s.xlsx` + `data/referentiel_finess.csv` → `main.py` → chargement/configuration → nettoyage, statut, FINESS et dédoublonnage → CSV de contrôle → rendu Jinja/Leaflet → fichiers dans `output/`.

Fichiers principaux :

- `main.py` : orchestration et résumé des compteurs ;
- `config/settings.yaml` : chemins, textes de l'interface, couleurs et alias explicites des colonnes ;
- `src/config_loader.py` : chargement de la configuration ;
- `src/data_loader.py` : lecture stricte de l'onglet `Postes` ;
- `src/data_cleaner.py` : normalisation, exclusion des retraits, dérivation mois/année, enrichissement FINESS, inférence des types, validation des coordonnées, dédoublonnage et CSV ;
- `src/html_renderer.py` : sérialisation JSON sûre, rendu du template et copie des assets ;
- `templates/map_template.html` : page d'accueil, carte Leaflet, recherche, filtres et fiches ;
- `scripts/check_build_output.py` : contrôle minimal des sorties ;
- `scripts/simplify_excel.py` : convertisseur exceptionnel d'un ancien export à 36 colonnes ;
- `tests/test_pipeline.py` : tests métier et sécurité ;
- `1_GENERER_LA_CARTE.command` : parcours Mac de génération ;
- `build.sh` : build automatisé/Render.

## Contrat du fichier Excel

Ne renomme pas l'onglet `Postes` ni les en-têtes sans modifier explicitement la configuration et les tests.

Colonnes :

1. `Actif ?` — `Oui` publie, `Non` archive sans publier ; vide est actuellement traité comme actif.
2. `Poste` — intitulé affiché, obligatoire.
3. `Catégorie` — utiliser la liste déroulante.
4. `Établissement(s)` — obligatoire.
5. `Lieu(x) du poste`.
6. `Ville`.
7. `Département`.
8. `Région`.
9. `FINESS` — idéalement 9 chiffres, stocké comme texte.
10. `Date de parution` — vraie date Excel ; le programme calcule mois et année.
11. `Source` — URL de l'avis.
12. `Observations`.
13. `Latitude` — facultative si FINESS reconnu.
14. `Longitude` — facultative si FINESS reconnu.
15. `Type de structure` — correction manuelle facultative.
16. `Type d'établissement` — correction manuelle facultative.

Le référentiel FINESS doit conserver au minimum `numero_finess_et`, `coord`, `sourcecoordet` et `raison_sociale`. Ne le remplace pas sans vérifier provenance, date, licence, séparateur et taux de géocodage.

## Procédure obligatoire au début de chaque intervention

1. Lire `README.md`, `docs/MISE_A_JOUR_DONNEES.md`, `config/settings.yaml` et les fichiers concernés.
2. Exécuter `git status --short` et préserver toute modification qui ne vient pas de toi.
3. Activer `.venv` ou le créer si nécessaire.
4. Lancer :

```bash
python -m unittest discover -v
python main.py
python scripts/check_build_output.py
```

5. Lire les compteurs et `output/postes_sans_coordonnees.csv`.
6. Pour toute modification de code, ajouter ou adapter un test proportionné au risque.

## Règles de maintenance

- Ne réintroduis jamais les postes marqués `Non` dans la carte.
- Exclure les retraits avant le dédoublonnage.
- Ne remets pas de rapprochement flou silencieux des noms de colonnes : les alias de `settings.yaml` doivent être explicites.
- Les colonnes latitude/longitude doivent rester facultatives lorsque le FINESS fournit les coordonnées.
- Conserver le repli manuel pour les postes sans FINESS.
- Ne jamais injecter directement dans `<script>` une valeur Excel non échappée ; le test du payload `</script>` doit continuer à passer.
- Conserver `output/index.html` et `output/carte_d3s.html` identiques.
- Ne publier, pousser, déployer, supprimer des données ou remplacer le référentiel qu'après mon autorisation explicite.
- Avant un commit de données, comparer les compteurs à la mise à jour précédente et expliquer tout écart.
- Pour diffuser localement, fournir tout le dossier `output` en ZIP, pas le seul HTML.

## Mise à jour ordinaire des postes

Quand je te donne un nouveau poste ou un nouveau fichier :

1. valider les champs métier et le statut ;
2. préserver les lignes historiques ;
3. utiliser `Actif ? = Non` pour un retrait ;
4. privilégier un FINESS vérifié ;
5. ne saisir latitude/longitude qu'en repli ou correction justifiée ;
6. régénérer et tester ;
7. me rendre un bilan avec lignes lues, retraits exclus, valides, sans coordonnées, doublons, catégories et fichiers modifiés.

N'utilise `scripts/simplify_excel.py` que pour importer un ancien classeur technique. Ne l'exécute pas sur le fichier courant sans copie de sécurité et comparaison préalable.

## Publication

Le build attendu est :

```bash
./build.sh
```

Avant toute proposition de push : vérifier tests, contrôle HTML, diff, statut Git, présence du logo et de la vraie plaquette. Le push sur `main` peut déclencher Render automatiquement : demande donc mon accord avant de le faire. Après déploiement, vérifier l'URL publique, les assets, la recherche, les filtres et quelques fiches.

## Points connus à surveiller

- `output/plaquette-promo.pdf` était un PDF provisoire lors de la passation : vérifier qu'il a été remplacé par la plaquette officielle.
- La carte n'est pas totalement hors ligne : Leaflet, MarkerCluster et les tuiles sont chargés depuis Internet.
- Le référentiel FINESS est volumineux et sa procédure de rafraîchissement reste à documenter précisément.
- Le dédoublonnage repose sur une clé métier ; examiner les collisions avant de la modifier.
- Le contrôle HTML est un smoke test, pas un test visuel de navigateur.
- Vérifier la publiabilité des données si le dépôt GitHub est public.

## Ce que j'attends de toi maintenant

Commence par auditer l'état réellement présent dans le workspace et compare-le à cette passation. Signale toute divergence sans l'écraser. Puis donne-moi un bilan bref : état Git, résultats des tests, compteurs actuels, éventuelles lignes sans coordonnées, présence/validité des assets et prochaines actions recommandées. Ne publie rien et ne modifie rien tant que ce contrôle initial n'a pas révélé un correctif nécessaire et que je ne t'ai pas demandé de l'appliquer.

---

## Notes pour le cédant

Avant d'envoyer le ZIP, remplacer si nécessaire la plaquette provisoire, supprimer les fichiers locaux inutiles non suivis, puis lancer une dernière fois les tests et le build. Ne pas inclure `.venv` dans le ZIP : elle est spécifique à la machine et sera recréée.
