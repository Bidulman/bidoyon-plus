# Bidoyon+
Une application Web pour gérer l'événement "Jus de Pomme" sans trop se casser la tête !

## Présentation

### L'événement
Le projet a été créé pour faciliter la gestion de l'événement "Jus de Pomme". Lors de cet événement dans le village, un grand pressoir est installé. Chacun participe à l'achat d'une certaine partie des pommes, ces participants sont appelés les **investisseurs**, simplement car ils placent des pommes pour recevoir plus tard une dose de jus de pomme proportionnelle à ce qu'ils ont apporté comme pommes. L'événement est découpé en plusieurs **pressées** : on remplit le pressoir d'une certaine dose de pommes, on presse, et on récupère le jus produit. Chaque pressée peut donc avoir une **quantité différente de pommes** (comptée en Kg), et donc une **quantité différente de jus** produit (comptée en L). On calcule ensuite le nombre de **jus contenu dans les pommes** (compté en L/Kg). En moyenne, les pommes utilisées produisent environ 0.6 L/Kg. Ces valeurs sont évidemment approximatives !

### Le but du projet
Cet événement implique donc plusieurs calculs. Les investisseurs doivent recevoir une part de jus de pomme proportionnelle à la quantité de pommes qu'ils ont apporté. Pour obtenir le nombre de jus qu'ils récupèreront, on effectue le calcul **I÷T×P**, où I est le nombre de pommes amené par l'investisseur (Kg), T est le nombre total de pommes apporté par les investisseurs (Kg), et P est la quantité de jus produite sur tout l'événement (L). On obtient alors la quantité de jus de pomme que doit recevoir l'investisseur (L). De plus, nous devons garder un œil sur la quantité de jus produite, les pommes utilisées, les pommes restantes ainsi que la quantité de jus dans les pommes, **dans chaque pressée et au total** !

Le projet est donc là pour faciliter la gestion de l'événement. Il doit être capable de fournir une interface utilisateur (sous forme de site Web) facile d'accès, avec un système de comptes et d'authentification, de plusieurs rôles (ils seront détaillés plus bas) et donc de permissions. Il doit effectuer les calculs automatiquement à partir des valeurs qu'on y rentre, et les afficher de différentes façons en fonction du rôle de l'utilisateur. De plus, un client sous forme de console doit être à disposition de l'administrateur pour gérer plus simplement certaines tâches !

**Bidoyon** ici veut dire "ce qui sort du pressoir". Le projet prend donc ce nom pour un peu plus d'originalité que "Jus de Pomme", tout simplement.

## Le projet

### Organisation
Contraîrement à la dernière version du projet, l'application sera 3 en 1 : l'application Web ainsi que l'API et même un petit nouveau, le CDN (Content Delivery Network, qui sert à stocker plusieurs médias importants) font partie de la même application.

### Outils utilisés
Pour fonctionner, le projet se base sur un langage et des libraires.
- Python est le langage utilisé pour l'entièreté du code
- SQL est celui qui sert pour toutes les requêtes avec la base de données
- YML est utile pour les fichiers de configuration
- HTML est utilisé pour la structuration des pages (accompagné de CSS)
- JavaScript est très peu utilisé mais a le mérite d'être là...
- FastAPI est la librairie Web utilisée pour le projet
- Sqlite3 s'occupe de stocker les données du projet
- Requests permet aux services de communiquer entre eux
- Uvicorn est utilisée pour démarrer FastAPI

D'autres librairies préinstallées dans l'installation basique de Python sont utilisées certaines fois, mais je juge inutile d'en parler ici, puisqu'elles sont utilisées dans pratiquement tous les projets.

## Suite...
La suite viendra avec le développement du projet.