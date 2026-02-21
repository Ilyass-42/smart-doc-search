# Smart Doc Search

## Présentation
Smart Doc Search est un moteur de recherche intelligent pour documents texte et PDF, avec le choix d’utiliser **TF-IDF** ou une **recherche sémantique** pour retrouver rapidement des informations pertinentes dans de grands documents.

## Fonctionnalités principales
- Upload de fichiers **TXT** et **PDF**  
- Choix du moteur de recherche : **TF-IDF** ou **sémantique**  
- Résultats affichés avec **score** et **contenu du chunk**  
- Gestion des **doublons** via hash + nom du fichier  
- Interface **Streamlit** simple et intuitive  

## Architecture / stack
- **Back-end :** FastAPI  
- **Front-end :** Streamlit  
- **Embeddings :** SentenceTransformer  
- Gestion des doublons avec **hash + nom** pour éviter les répétitions  

## Problèmes résolus et à venir
- Duplication de chunks **résolue**  
- **Optimisation** en cours pour accélérer les recherches volumineuses  
- Support PDF complet et amélioration UI à venir  

## Installation & usage

### Étape 1 : Installer les dépendances
```bash
pip install -r requirements.txt

# Smart Doc Search

## Présentation
Smart Doc Search est un moteur de recherche intelligent pour documents texte et PDF, avec le choix d’utiliser **TF-IDF** ou une **recherche sémantique** pour retrouver rapidement des informations pertinentes dans de grands documents.

## Fonctionnalités principales
- Upload de fichiers **TXT** et **PDF**  
- Choix du moteur de recherche : **TF-IDF** ou **sémantique**  
- Résultats affichés avec **score** et **contenu du chunk**  
- Gestion des **doublons** via hash + nom du fichier  
- Interface **Streamlit** simple et intuitive  

## Architecture / stack
- **Back-end :** FastAPI  
- **Front-end :** Streamlit  
- **Embeddings :** SentenceTransformer  
- Gestion des doublons avec **hash + nom** pour éviter les répétitions  

## Problèmes résolus et à venir
- Duplication de chunks **résolue**  
- **Optimisation** en cours pour accélérer les recherches volumineuses  
- Support PDF complet et amélioration UI à venir  

## Installation & usage

### Étape 1 : Installer les dépendances
```bash
pip install -r requirements.txt
# Smart Doc Search

## Présentation
Smart Doc Search est un moteur de recherche intelligent pour documents texte et PDF, avec le choix d’utiliser **TF-IDF** ou une **recherche sémantique** pour retrouver rapidement des informations pertinentes dans de grands documents.

## Fonctionnalités principales
- Upload de fichiers **TXT** et **PDF**  
- Choix du moteur de recherche : **TF-IDF** ou **sémantique**  
- Résultats affichés avec **score** et **contenu du chunk**  
- Gestion des **doublons** via hash + nom du fichier  
- Interface **Streamlit** simple et intuitive  

## Architecture / stack
- **Back-end :** FastAPI  
- **Front-end :** Streamlit  
- **Embeddings :** SentenceTransformer  
- Gestion des doublons avec **hash + nom** pour éviter les répétitions  

## Problèmes résolus et à venir
- Duplication de chunks **résolue**  
- **Optimisation** en cours pour accélérer les recherches volumineuses  
- Support PDF complet et amélioration UI à venir  

## Installation & usage

### Étape 1 : Installer les dépendances
```bash
pip install -r requirements.txt
# Smart Doc Search

## Présentation
Smart Doc Search est un moteur de recherche intelligent pour documents texte et PDF, avec le choix d’utiliser **TF-IDF** ou une **recherche sémantique** pour retrouver rapidement des informations pertinentes dans de grands documents.

## Fonctionnalités principales
- Upload de fichiers **TXT** et **PDF**  
- Choix du moteur de recherche : **TF-IDF** ou **sémantique**  
- Résultats affichés avec **score** et **contenu du chunk**  
- Gestion des **doublons** via hash + nom du fichier  
- Interface **Streamlit** simple et intuitive  

## Architecture / stack
- **Back-end :** FastAPI  
- **Front-end :** Streamlit  
- **Embeddings :** SentenceTransformer  
- Gestion des doublons avec **hash + nom** pour éviter les répétitions  

## Problèmes résolus et à venir
- Duplication de chunks **résolue**  
- **Optimisation** en cours pour accélérer les recherches volumineuses  
- Support PDF complet et amélioration UI à venir  

## Installation & usage

### Étape 1 : Installer les dépendances
```bash
pip install -r requirements.txt

### Étape 2 : Lancer l'API FastAPI

uvicorn main:app --reload

### Étape 3 : Lancer l'interface Streamlit

streamlit run app.py

