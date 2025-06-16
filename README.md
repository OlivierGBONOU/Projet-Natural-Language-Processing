# 🎵 Analyse des Sentiments des Chansons - Projet NLP

## 🧠 Description

Ce projet vise à effectuer une **analyse des sentiments** à partir des paroles des chansons d'un artiste donné.
Par défaut, le projet analyse les textes de **Charles Aznavour**, mais il est possible de modifier l’artiste et d’utiliser d'autres corpus de chansons.

Le projet utilise des techniques classiques de traitement du langage naturel (NLP) pour :

* Nettoyer et prétraiter les textes
* Appliquer une analyse lexicale des sentiments
* Générer des visualisations (nuages de mots, histogrammes, etc.)
* Permettre une exploration interactive via une interface utilisateur

---

## 📁 Arborescence du projet

```
Projet-Natural-Language-Processing-main/
├── 0_TP_1_Description.ipynb       # Introduction et description du projet
├── 1_python.py                    # Script de scraping
├── 2_nlp_tp_1.ipynb               # Analyse NLP détaillée (nettoyage, sentiment, TF-IDF, etc.)
├── 3_app.py                       # Application interactive (Streamlit ou Flask)
├── requirements.txt               # Dépendances du projet
```

---

## ⚙️ Installation

### Prérequis

* Python ≥ 3.8
* pip

### Installation des dépendances

```bash
pip install -r requirements.txt
```

---

## 🚀 **Logique d'exécution du projet**  

### 🔹 Étape 1 : Extraction des données  
📜 **Exécuter** : `1_python.py`  
- Saisir le **nom de l'artiste** 🎤  
- Indiquer le **lien vers la page** (⚠️ sans le dernier caractère du lien) 🔗  
- Définir le **nombre de pages à scraper** 📄  
🔽 **Résultat** : Génération d'une **base de données CSV** contenant les paroles des chansons et portant le nom de l'artiste.

### 🔹 Étape 2 : Traitement NLP et analyse des sentiments  
📜 **Exécuter** : `2_nlp_tp_1.ipynb`  
- Prétraitement des paroles de la base CSV 📝  
- Attribution d’un **score de sentiment** à chaque titre 📊 
🔽 **Résultat** : Génération d'une **base de données Excel** portant le nom de l'artiste + `sentiments`.

### 🔹 Étape 3 : Lancement de l’application Streamlit  
📜 **Exécuter** : `3_app.py`  
Lancer la commande suivante dans le terminal pour démarrer l'application :  

```bash
streamlit run 3_app.py
```

---

## ✍️ Modifier l’artiste

Vous pouvez remplacer les lignes suivantes dans `1_python.py` :
- artist = "Charles Aznavour"
- website = "https://paroles2chansons.lemonde.fr/paroles-charles-aznavour?page="
- nb_pages = 15

---

## 📊 Méthodes utilisées

* **Prétraitement du texte** : nettoyage, tokenisation, suppression des stopwords
* **Analyse de sentiments** : lexique (ex: TextBlob ou VADER)
* **TF-IDF** et fréquence des mots
* **Visualisations** : wordclouds, barplots

---

## 📚 Ressources

* Chansons : Charles Aznavour
* NLP : `nltk`, `sklearn`, `pandas`, `matplotlib`, `wordcloud`
* Interface : `streamlit` ou `flask`

---

## 👨‍💻 Auteurs

Projet réalisé dans le cadre du cours de traitement automatique du langage naturel.