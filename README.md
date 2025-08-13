# LOG430 - TODO: Titre du labo

🎯 Objectifs d’apprentissage
- Comprendre et mettre en pratique le pattern CQRS (séparer les opérations de lecture/écriture).
- Intégrer une API Flask avec MySQL (write) et Redis (read cache).
- Écrire des tests de fumée et configurer une CI simple avec GitHub Actions.

⚙️ Setup
1. Copier le fichier `.env` et ajuster les variables (MySQL / Redis).
2. Démarrer les services:
   - `docker-compose up --build`
3. Installer les dépendances:
   - `pip install -r requirements.txt`
4. Initialiser la DB:
   - Exécuter le script SQL dans `db-init/init.sql` contre la base MySQL.

🧪 Activités pratiques
- Ajouter / supprimer / consulter des commandes (orders) via l'API.
- Étendre les modèles read/write et améliorer la logique de ranking.

📦 Livrables
- Projet source Python avec API Flask
- Scripts d'initialisation de la base de données
- Docker + docker-compose
- Tests unitaires de base et CI GitHub Actions
