# Labo 02 – Architecture monolithique, ORM, CQRS, Persistance polyglotte
<img src="https://upload.wikimedia.org/wikipedia/commons/2/2a/Ets_quebec_logo.png" width="250">    
ÉTS - LOG430 - Architecture logicielle - Chargé de laboratoire: Gabriel C. Ullmann, Automne 2025.    

## 🎯 Objectifs d’apprentissage
- Comprendre ce qu’est une architecture monolithique à travers l’exemple d’une application de gestion de magasin.
- Comprendre et appliquer les patrons CQRS (Command Query Responsibility Segregation) pour séparer les opérations de lecture et écrite. 
- Comprendre et appliquer le CQRS avec une persistance polyglotte afin d’optimiser les opérations de lecture et d’écriture.
- Comprendre l’importance d’un ORM (Object-Relational Mapping) pour faciliter l’interaction avec les bases de données.

## ⚙️ Setup
Dans ce laboratoire, nous continuerons à développer l'application de gestion de magasin que nous avons commencée dans le laboratoire 01. Maintenant l'application deviendra plus complexe puisqu’elle permettra la gestion des commandes, des articles et des utilisateurs dans une interface Web. 

Nous voulons préparer cette application à une charge de lecture et d'écriture élevée. Pour ce faire, nous utiliserons la persistance polyglotte avec Redis et MySQL. Tout au long des activités, vous découvrirez une stratégie pour y parvenir.

Veuillez utiliser les diagrammes UML disponibles dans le dossier `docs/views` comme référence pour l’implémentation.

### 1. Faites un fork et clonez le dépôt GitLab
```bash
git clone https://github.com/guteacher/log430-a25-labo2
cd log430-a25-labo2
```

### 2. Préparez l’environnement de développement
Suivez les mêmes étapes que dans le laboratoire 00. Créez un fichier .env.

## 🧪 Activités pratiques

### 1. Population initiale de Redis au démarrage
Dans `commands/write_order.py`, la méthode `sync_all_orders_to_redis` charge toutes les commandes depuis MySQL vers Redis au démarrage de l'application. Veuillez terminer l'implémentation et assurez-vous qu'elle ne s'exécute qu'une seule fois au démarrage de l'application. Cette opération prendra plus de temps et de ressources à mesure que notre base de données se développe, nous voulons donc la faire uniquement lorsque cela est strictement nécessaire.

> 💡 **Question 1** : Lorsque l'application démarre, la synchronisation entre Redis et MySQL est-elle initialement déclenchée par quelle méthode ? Veuillez inclure le code pour illustrer votre réponse.

### 2. Modifier la View de commandes pour utiliser uniquement Redis
Dans `views/order_view.py`, remplacez l'appel à `list_orders` pour un appel à une autre méthode qui lit les commandes à partir de Redis. Veuillez terminer la méthode  `get_orders_from_redis` qu'existe déjà dans `queries/read_order.py`.

> 💡 **Question 2** : Quelles methodes avez-vous utilisées pour lire des données à partir de Redis ? Veuillez inclure le code pour illustrer votre réponse.

### 2. Insérer dans Redis
Dans `commands/write_order.py`, à chaque commande ajoutée dans MySQL, insérez-la également dans Redis. Même si cela peut paraître redondant, cela nous permettra de générer des rapports statistiques sur les commandes sans lire directement dans MySQL. Pour une application à forte charge (grand nombre de requêtes), cela permet de réduire la pression sur MySQL.

> 💡 **Question 3** : Quelles methodes avez-vous utilisées pour ajouter des données dans Redis ? Veuillez inclure le code pour illustrer votre réponse.

### 3. Supprimer dans Redis
Toujours dans `commands/write_order.py`, à chaque commande supprimée de MySQL, supprimez-la également de Redis afin de maintenir la consistance des données.

> 💡 **Question 4** : Quelles methodes avez-vous utilisées pour supprimer des données dans Redis ? Veuillez inclure le code pour illustrer votre réponse.

### 4. Créer un rapport : les plus grands acheteurs
Dans `queries/read_order.py`, créez une méthode qui obtient la liste le top 10 des utilisateurs ayant le plus dépensé en commandes. Triez le résultat par total dépensé (ordre décroissant).

> 💡 **Question 5** : Si nous souhaitions créer un rapport similaire, mais présentant les produits les plus vendus, les informations dont nous disposons actuellement dans Redis sont-elles suffisantes, ou devrions-nous checher dans le tables sur MySQL ? Si nécessaire, quelles informations devrions-nous ajouter à Redis ? Veuillez inclure le code pour illustrer votre réponse.

### ✅ Correction des activités

Des tests unitaires sont inclus dans le dépôt. Pour les exécuter :

```bash
python3 -m pytest
```

Si tous les tests passent ✅, vos implémentations sont correctes.

## 📦 Livrables
- Un fichier .zip contenant l’intégralité du code source du projet Labo 02.
- Un rapport en .pdf répondant aux 5 questions présentées dans ce document. Il est obligatoire d’illustrer vos réponses avec du code ou des captures de terminal.
