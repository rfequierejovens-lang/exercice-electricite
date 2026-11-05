# Exercice complet : l'électricité dans 12 quartiers

**Lien de mon application :** [L'électricité dans 12 quartiers](https://data-exercice-electricite-rfequierejovens-lang-qb3mamlylbsyevo.streamlit.app/)

Une compagnie d'électricité (fictive) vous confie deux ans de relevés, de janvier 2024 à décembre 2025, pour 12 quartiers de Port-au-Prince, Delmas, Pétion-Ville et Cap-Haïtien. Le directeur veut savoir si la consommation suit la chaleur, ou les heures de courant.

| Fichier | Une ligne par | Colonnes |
|---|---|---|
| `donnees/consommation_brut.csv` | quartier et mois | `mois`, `quartier`, `kwh`, `heures_courant` |
| `donnees/quartiers.csv` | quartier | `quartier`, `commune`, `type`, `abonnes` |
| `donnees/meteo.csv` | commune et mois | `mois`, `commune`, `temperature_c`, `pluie_mm` |
| `donnees/consommation.csv` | quartier et mois | le fichier de référence, pour vérifier votre nettoyage (question 8) |

## Ce qu'il faut rendre

1. **`exploration.ipynb`** : toute votre démarche, dans le même plan que le projet final : diagnostic, nettoyage, jointures (qui écrivent `donnees/consommation_propre.csv`), une partie par question, conclusion. Exécutez-le du début à la fin (**Restart**, puis **Run All**) avant de pousser : les sorties et les graphiques doivent être visibles sur GitHub.
2. **`app.py`** : le tableau de bord Streamlit, **en ligne**, construit en six étapes (ci-dessous). Il lit `donnees/consommation_propre.csv` et ne refait pas le nettoyage.

On fait l'exercice ensemble, étape par étape : c'est exactement la démarche du projet final.

## Démarrer

```bash
cd cours-python
gh repo clone esih-classroom/data-exercice-electricite-VOTRE-IDENTIFIANT
cd data-exercice-electricite-VOTRE-IDENTIFIANT
uv sync
code .
```

Ouvrez `exploration.ipynb`, choisissez le noyau `.venv`, et répondez dans l'ordre.

## Lancer le tableau de bord sur votre machine

```bash
uv run streamlit run app.py
```

Le navigateur s'ouvre sur `http://localhost:8501`. Laissez la commande tourner : à chaque enregistrement de `app.py`, cliquez sur **Rerun** (ou choisissez **Always rerun**). `Ctrl+C` dans le terminal arrête l'application.

## Le tableau de bord, en six étapes

Après chaque étape : l'application tourne sur votre machine, puis `git add .`, `git commit`, `git push` et `git push perso main`. Le tableau de bord en ligne grandit avec vous.

| Étape | Ce qu'on ajoute | Attendu |
|---|---|---|
| 1 | L'`app.py` de départ, tel quel : titre et fichier brut. On le met **en ligne tout de suite** (section suivante) | un lien en `.streamlit.app` qui affiche 300 lignes |
| 2 | Lire `consommation_propre.csv` dans une fonction décorée par `@st.cache_data` ; deux phrases de contexte | l'application démarre sans erreur |
| 3 | Deux filtres dans la barre latérale : `st.sidebar.multiselect` des communes (toutes cochées), `st.sidebar.selectbox` de l'année | 2025 par défaut ; un message si aucune commune n'est choisie |
| 4 | Trois indicateurs côte à côte : `st.columns(3)` et `st.metric` | 2025, toutes communes : 37.35 millions de kWh, 222.2 kWh par abonné, 12.0 heures de courant |
| 5 | `st.tabs` : un onglet par question (parties 4 à 8 du notebook), chacun avec un graphique et une phrase chiffrée | corrélations 0.76 et -0.15 dans l'onglet « Chaleur ou courant ? » |
| 6 | La conclusion (`st.markdown`), puis les données filtrées dans un `st.expander` | la réponse de la partie 9 du notebook |

## Mettre l'application en ligne

Streamlit Community Cloud est gratuit, mais il ne déploie que depuis un dépôt dont vous êtes **administrateur** : le dépôt Classmoji ne convient pas. Chacun en fait une copie publique sur son propre compte GitHub, une seule fois, depuis le dossier du dépôt :

```bash
gh repo create exercice-electricite --public --source . --remote perso --push
```

Puis, sur [share.streamlit.io](https://share.streamlit.io) :

1. **Continue with GitHub**, et acceptez l'accès à vos dépôts.
2. **Create app**, puis **Deploy a public app from GitHub**.
3. Repository : `VOTRE-COMPTE/exercice-electricite` ; Branch : `main` ; Main file path : `app.py`.
4. App URL : un nom court et lisible, par exemple `exercice-electricite-votre-nom`.
5. **Advanced settings** : Python **3.14**, la version de votre machine. Puis **Deploy**.

L'application lit `donnees/consommation_propre.csv` : ce fichier doit être commité, sinon elle plante en ligne.

À chaque modification, on pousse vers les deux dépôts :

```bash
git add .
git commit -m "Ajoute la courbe de consommation"
git push
git push perso main
```

L'application en ligne se met à jour seule en une minute environ. Collez son lien en haut de ce README.

## Si ça coince

| Problème | Solution |
|---|---|
| `streamlit: command not found` | Lancez-la avec uv : `uv run streamlit run app.py` |
| `FileNotFoundError: ..._propre.csv` | Exécutez d'abord tout le notebook : c'est lui qui écrit le fichier propre |
| L'application en ligne affiche « Error running app » | **Manage app**, en bas à droite, montre l'erreur : souvent un fichier non commité ou une version de Python différente |
| L'application en ligne ne change pas | Vous avez oublié `git push perso main` |
| `rejected ... fetch first` au `git push` | Quelqu'un a poussé avant vous : `git pull`, puis `git push` |
| `ModuleNotFoundError: No module named 'pandas'` dans le notebook | Mauvais noyau : **Select Kernel**, puis `.venv` |

Bloqué ? Écrivez un commentaire dans l'issue, avec le message d'erreur en entier.
