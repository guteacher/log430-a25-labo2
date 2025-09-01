# Labo 02 – Architecture monolithique, ORM, CQRS, Persistance polyglotte
<img src="https://upload.wikimedia.org/wikipedia/commons/2/2a/Ets_quebec_logo.png" width="250">    
ÉTS - LOG430 - Architecture logicielle - Chargé de laboratoire: Gabriel C. Ullmann, Automne 2025.    

## 🎯 Objectifs d’apprentissage
- Comprendre ce qu’est une architecture monolithique à travers l’exemple d’une application de gestion de magasin.
- Comprendre et appliquer les patrons CQRS (Command Query Responsibility Segregation) pour séparer les opérations de lecture et écrite. 
- Comprendre et appliquer le CQRS avec une persistance polyglotte afin d’optimiser les opérations de lecture et d’écriture.
- Comprendre l’importance d’un ORM (Object-Relational Mapping) pour faciliter l’interaction avec les bases de données.

## ⚙️ Setup
Dans ce laboratoire, vous développerez une application de gestion de magasin similaire à celle du labo 01. Cependant, cette application sera plus complexe puisqu’elle permettra la gestion des commandes, des articles et des utilisateurs dans une interface Web. Veuillez utiliser les diagrammes UML disponibles dans le dossier `docs/views` comme référence pour l’implémentation.

### 1. Faites un fork et clonez le dépôt GitLab
```bash
git clone https://github.com/guteacher/log430-a25-labo2
cd log430-a25-labo2
```

### 2. Préparez l’environnement de développement
Suivez les mêmes étapes que dans le laboratoire 00. Créez un fichier .env.

## 🧪 Activités pratiques
TODO: why use polyglot

### 1. Population initiale de Redis au démarrage
Créez une fonction qui charge toutes les commandes depuis MySQL vers Redis au démarrage

**Exemple de code**:
```python
pass
```

### 2. Insérer dans Redis
Dans `commands/write_order.py`, à chaque commande ajoutée dans MySQL, insérez-la également dans Redis. Cela permettra de générer des rapports statistiques sur les commandes sans avoir à lire directement dans MySQL. Pour une application à forte charge (grand nombre de requêtes), cela permet de réduire la pression sur MySQL.

> 💡 Question 1 : Quelles methodes avez-vous utilisées pour ajouter des données dans Redis ? Veuillez inclure le code pour illustrer votre réponse.

### 3. Supprimer dans Redis
Toujours dans `commands/write_order.py`, à chaque commande supprimée de MySQL, supprimez-la également de Redis afin de maintenir la consistance des données.

> 💡 Question 2 : Quelles methodes avez-vous utilisées pour supprimer des données dans Redis ? Veuillez inclure le code pour illustrer votre réponse.

### 4. Créer un rapport : best_selling_products
Dans `queries/read_order.py`, créez une méthode qui obtient la liste des articles les plus vendus. Triez le résultat par nombre de commandes (ordre décroissant).

> 💡 Question 3 : TODO

### ✅ Correction des activités

Des tests unitaires sont inclus dans le dépôt. Pour les exécuter :

```bash
python3 -m pytest
```

Si tous les tests passent ✅, vos implémentations sont correctes.

## 📦 Livrables
- Un fichier .zip contenant l’intégralité du code source du projet Labo 02.
- Un rapport en .pdf répondant aux 4 questions présentées dans ce document. Il est obligatoire d’illustrer vos réponses avec du code ou des captures de terminal.
