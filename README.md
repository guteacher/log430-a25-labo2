# Labo 02 – Architecture monolithique, ORM, DDD, CQRS, Persistance polyglotte
<img src="https://upload.wikimedia.org/wikipedia/commons/2/2a/Ets_quebec_logo.png" width="250">    
ÉTS - LOG430 - Architecture logicielle - Chargé de laboratoire: Gabriel C. Ullmann, Automne 2025.    

## 🎯 Objectifs d’apprentissage
- Comprendre ce qu’est une architecture monolithique à travers l’exemple d’une application de gestion de magasin.
- Comprendre et appliquer les patrons CQRS (Command Query Responsibility Segregation) pour séparer les opérations de lecture et écrite. 
- Comprendre et appliquer le CQRS avec une persistance polyglotte afin d’optimiser les opérations de lecture et d’écriture.
- Observer l'utilisation du DDD (Domain-Driven Design) pour bien nommer les entités et pour séparer la logique de l'application et de l'infrastructure dans cette application.
- Comprendre l’importance d’un ORM (Object-Relational Mapping) pour faciliter l’interaction avec les bases de données.

## ⚙️ Setup
Dans ce laboratoire, vous développerez une application de gestion de magasin similaire à celle du labo 01. Cependant, cette application sera plus complexe puisqu’elle permettra la gestion des commandes, des articles et des utilisateurs.

L’application est une API qui reçoit des requêtes d’un front-end, puis communique avec un serveur de base de données pour retourner les informations (architecture en trois couches).

### 1. Faites un fork et clonez le dépôt GitLab
```bash
git clone https://github.com/guteacher/log430-a25-labo2
cd log430-a25-labo2
```

### 2. Préparez l’environnement de développement
Suivez les mêmes étapes que dans le laboratoire 00.

### 3. Installez Postman
Installez Postman et importez la collection disponible dans /docs/collections.

## 🧪 Activités pratiques

### 1. Permettre l’accès à l’API

Ouvrez le port 5000 dans le fichier docker-compose.yml afin de permettre l’accès à l’API via Postman :
```yaml
store_manager:
  build: .
  volumes:
    - .:/app
  ports:
    - "5000:5000"
```

### 2. Insérer dans Redis
Dans `commands/write_order.py`, à chaque commande ajoutée dans MySQL, insérez-la également dans Redis. Cela permettra de générer des rapports statistiques sur les commandes sans avoir à lire directement dans MySQL. Pour une application à forte charge (grand nombre de requêtes), cela permet de réduire la pression sur MySQL.

> 💡 Question 1 : Quelles methodes avez-vous utilisées pour ajouter des données dans Redis ? Veuillez inclure le code pour illustrer votre réponse.

### 3. Test : ajouter une commande
Testez en utilisant la route `POST orders` à Postman.

> 💡 Question 2 : Quel résultat de requête avez-vous obtenu? Veuillez inclure la sortie à Postman pour illustrer votre réponse.

### 4. Supprimer dans Redis
Toujours dans `commands/write_order.py`, à chaque commande supprimée de MySQL, supprimez-la également de Redis afin de maintenir la consistance des données.

> 💡 Question 3 : Quelles methodes avez-vous utilisées pour supprimer des données dans Redis ? Veuillez inclure le code pour illustrer votre réponse.

### 5. Test : supprimer une commande
Testez en utilisant la route `DELETE orders` à Postman.

> 💡 Question 4 : Quel résultat de requête avez-vous obtenu? Veuillez inclure la sortie à Postman pour illustrer votre réponse.

### 6. Écrivez les « smoke tests »
Écrivez les tests unitaires qu'appelent les routes `POST orders` et  `DELETE orders` et vérifient si le résultat est consistent. Utilisez comme exemple le test qu'existe dèjá à `tests/test_store_manager.py`.

### 7. Créer un rapport : highest_spenders
Dans `queries/read_order.py`, créez une méthode qui obtient la liste des utilisateurs ayant le plus dépensé en commandes. Triez le résultat par total dépensé (ordre décroissant).

> 💡 Question 5 : Comment avez-vous testé cette route dans Postman ? Veuillez inclure votre collection Postman pour illustrer votre réponse.

### 8. Insérer les produits dans Redis
Dans `commands/write_order.py`, à chaque commande ajoutée dans MySQL, mettez également à jour dans Redis le nombre de fois que chaque article a été commandé. Si l’article existe déjà, incrémentez la valeur. Exemple :
```python
count = r.get("product:123")
r.set("product:123", int(count) + 1 if count else 1)
```

### 9. Créer un rapport : best_sellers
Dans `queries/read_order.py`, créez une méthode qui obtient la liste des articles les plus vendus. Triez le résultat par nombre de commandes (ordre décroissant).

> 💡 Question 6 : Pourrions-nous réaliser l’activité 6 sans avoir fait l’activité 5 au préalable ? Quels en seraient les impacts sur la performance ?

## 📦 Livrables
- Un fichier .zip contenant l’intégralité du code source du projet Labo 02.
- Un rapport en .pdf répondant aux 4 questions présentées dans ce document. Il est obligatoire d’illustrer vos réponses avec du code ou des captures de terminal.
