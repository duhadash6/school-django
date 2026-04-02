# School Management System

**Université Abdelmalek Essaadi — Faculté des Sciences et Techniques de Tanger**  
**Licence IDAI | Développement Web | 2025–2026**

## Description
Plateforme web développée sous **Django** pour la gestion centralisée, administrative et académique d'un établissement scolaire. Elle intègre un système d'authentification robuste (RBAC) avec des espaces sécurisés et sur-mesure répondant aux besoins quotidiens des **étudiants**, des **professeurs** et de l'**administration**.

## Fonctionnalités
| Fonctionnalité | Description |
|----------------|-------------|
| **Catalogue des utilisateurs** | Ajout, édition, et supervision en temps réel des élèves et du corps enseignant |
| **Multi-rôles sécurisé** | Étudiant, Professeur, Administrateur (RBAC structuré via `@role_required`) |
| **Gestion académique** | Inscription aux cours, attribution des matières aux enseignants |
| **Portail d'évaluation (Grading)**| Interface métier permettant la saisie dynamique des notes par les professeurs |
| **Tableaux de bord (Dashboards)**| Espaces analytiques dédiés par profil (statistiques, suivi de l'apprentissage) |
| **Emploi du temps visuel** | Calendrier interactif propulsé par FullCalendar pour structurer la grille horaire |
| **Authentification renforcée** | Login, prévention des accès externes directs (URL forcées), sessions sécurisées |
| **Design Adaptatif** | Mode responsive soigné pour la fluidité d'affichage (Vanilla JS / Bootstrap) |

## Stack technique
- **Backend :** Django (Python) orienté MVT (Modèle-Vue-Template)
- **Frontend :** Templates Django (.html), CSS Vanilla, JavaScript, Bootstrap
- **Base de données :** SQLite (Développement natif Django)
- **Librairies clés :**
  - **FullCalendar** — Emplois du temps hebdomadaires récurrents
  - **ApexCharts** — Composants graphiques métier
  - **jQuery** — Manipulation du DOM (Sidebar, validations)

## Installation

```bash
# 1. Cloner le projet
git clone https://github.com/duhadash6/school-django.git
cd school-django/school

# 2. Créer un environnement virtuel (Fortement recommandé)
python -m venv venv
# Windows: venv\Scripts\activate
# Linux/macOS: source venv/bin/activate

# 3. Installer les dépendances Python
pip install -r requirements.txt

# 4. Effectuer les migrations système
python manage.py makemigrations
python manage.py migrate

# 5. Déployer la base de données (Fixtures ou Seeder Automatique)
# Option A : Via le fichier Fixtures officiel
python manage.py loaddata test_data_fixtures.json
# Option B : Via notre puissant script de peuplement aléatoire
python populate_fake_data.py

# 6. Lancer le serveur Django
python manage.py runserver
```
*(Accédez au projet sur http://127.0.0.1:8000/)*


## Structure du projet (Architécture MVT)

```text
school-django/school/
│
├── home_auth/                      <- Authentification, CustomUser, Décorateurs (RBAC)
├── student/                        <- Modèles (Student, Parent), Vues Étudiants
├── faculty/                        <- Modèles (Teacher, Department), Tableaux de bord Admin/Prof
├── subjects/                       <- Modèles métier (Subject, Exam, Enrollment, Timetable)
├── holidays/                       <- Composants calendriers et événements
│
├── templates/                      <- Couche présentation (Vues HTML dynamiques - DTL)
│   ├── Home/                       <- Héritage maître (base.html, layout, authentification)
│   ├── students/                   <- Dashboards analytiques et espaces élèves
│   ├── teachers/                   <- Interfaces de saisie de notes
│   ├── subjects/                   <- Rendu des emplois du temps
│   └── departments/
│
├── static/                         <- Assets du Front-End (Serveur unifié)
│   ├── assets/css/                 <- Stylesheets Bootstrap & personnalisées
│   ├── assets/js/                  <- Logique Sidebar et modules d'interaction
│   └── assets/plugins/             <- Librairies analytiques (Apex, Simple-Calendar)
│
├── school/                         <- Cœur du configurateur Django (settings.py, urls.py racine)
├── database/                       <- Instance SQLite (db.sqlite3)
│
├── populate_fake_data.py           <- Générateur massif de données métier automatisé
├── test_data_fixtures.json         <- Instance instantanée de déploiement (Fixtures)
├── requirements.txt                <- Manifeste des librairies Python (pip freeze)
├── manage.py                       <- CLI Administration Django
└── README.md                       <- Documentation technique de déploiement
```

## Contribution
Les contributions visant à améliorer le parcours scolaire éducatif sont les bienvenues.  
Pour proposer une amélioration :
1. **Forkez** le dépôt
2. Créez votre branche : `git checkout -b feature/NouvelleVue`
3. Commitez vos ajustements : `git commit -m "Ajout: Implémentation Nouvelle Vue"`
4. Pushez vers la branche : `git push origin feature/NouvelleVue`
5. Ouvrez une **Pull Request** en vue d'une révision.

## Auteurs
**Projet réalisé par :**
- **Ziouani Doha**
- **Chentouf Ayoub**

*Encadré par Prof. Sara Ahsain*

**Université Abdelmalek Essaadi — Faculté des Sciences et Techniques de Tanger — 2025/2026**
