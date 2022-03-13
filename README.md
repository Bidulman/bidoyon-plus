# Bidoyon+
Une application Web pour gérer l'événement "Jus de Pomme" sans trop se casser la tête !

---

## Présentation

### L'événement
Le projet a été créé pour faciliter la gestion de l'événement "Jus de Pomme". Lors de cet événement dans le village, un grand pressoir est installé. Chacun participe à l'achat d'une certaine partie des pommes, ces participants sont appelés les **investisseurs**, simplement car ils placent des pommes pour recevoir plus tard une dose de jus de pomme proportionnelle à ce qu'ils ont apporté comme pommes. L'événement est découpé en plusieurs **pressées** : on remplit le pressoir d'une certaine dose de pommes, on presse, et on récupère le jus produit. Chaque pressée peut donc avoir une **quantité différente de pommes** (comptée en Kg), et donc une **quantité différente de jus** produit (comptée en L). On calcule ensuite le nombre de **jus contenu dans les pommes** (compté en L/Kg). En moyenne, les pommes utilisées produisent environ 0.6 L/Kg. Ces valeurs sont évidemment approximatives !

### Le but du projet
Cet événement implique donc plusieurs calculs. Les investisseurs doivent recevoir une part de jus de pomme proportionnelle à la quantité de pommes qu'ils ont apporté. Pour obtenir le nombre de jus qu'ils récupèreront, on effectue le calcul **I÷T×P**, où I est le nombre de pommes amené par l'investisseur (Kg), T est le nombre total de pommes apporté par les investisseurs (Kg), et P est la quantité de jus produite sur tout l'événement (L). On obtient alors la quantité de jus de pomme que doit recevoir l'investisseur (L). De plus, nous devons garder un œil sur la quantité de jus produite, les pommes utilisées, les pommes restantes ainsi que la quantité de jus dans les pommes, **dans chaque pressée et au total** !

Le projet est donc là pour faciliter la gestion de l'événement. Il doit être capable de fournir une interface utilisateur (sous forme de site Web) facile d'accès, avec un système de comptes et d'authentification, de plusieurs rôles (ils seront détaillés plus bas) et donc de permissions. Il doit effectuer les calculs automatiquement à partir des valeurs qu'on y rentre, et les afficher de différentes façons en fonction du rôle de l'utilisateur. De plus, un client sous forme de console doit être à disposition de l'administrateur pour gérer plus simplement certaines tâches !

**Bidoyon** ici veut dire "ce qui sort du pressoir". Le projet prend donc ce nom pour un peu plus d'originalité que "Jus de Pomme", tout simplement.

---

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

### Outils développés

#### L'Application
L'application s'utilise depuis le navigateur. Elle correspond à ce qui sera plutôt apparent, ce que verront les utilisateurs. Elle n'utilise pas l'API puisqu'elle est directement connectée à la base de données.

#### L'API
L'API est comme collée à l'application, mais n'est pas indispensable. Par contre, elle est indispensable si on veut utiliser le client ou utiliser des requêtes HTTP pour communiquer avec la base de données.

#### Le Client
Le client est détaché de l'application et de l'API. Il peut-être n'importe où, sur un autre ordinateur, du moment qu'il a accès à l'API. Pour l'utiliser, il suffit de copier le package "client" dans le dépôt de code de Bidoyon+. Dans ce package, on peut trouver différentes choses.
- Le Raw Client : Une aide basée sur Request pour mémoriser le jeton d'authentification et l'adresse de l'API, tout en acceptant d'envoyer n'importe quelle requête.
- Le Client : Basé sur le Raw Client, il possède des requêtes prêtes à l'utilisation et accessibles par l'intermédiaire de méthodes, telles que méthodes telles que "get_users()" par exemple.
- La Console : Basée elle-même sur le Client, elle est utilisable pour utiliser le Client comme une ligne de commandes. Voyez sa partie dédiée ci-dessous.

#### La Console
Comme dit ci-dessus, la console est une façon d'utiliser le Client par l'intermédiaire de lignes de commandes.

###### Activer la console
Importez la console et instanciez-la comme ce qui suit :
```python
from client import Console

if __name__ == "__main__":
    Console()
```
Démarrez ensuite le script créé et entrez l'adresse (si vous ne mettez rien, elle sera par défaut à http://localhost:8080). Puis entrez un token d'authentification (préférez le token ayant le plus de permissions possible). Ensuite, vous pouvez utiliser les commandes comme sur une console classique.

###### Liste des commandes
La liste des commandes est disponible dans le code du fichier `client/console.py`, mais voici la liste des commandes :

- `getusers` (abrégé en `gus`) : Récupère la liste des utilisateurs
- `getuser <id>` (abrégé en `gu`) : Récupère les informations d'un utilisateur en particulier
- `adduser <name> <permission> <password>` (abrégé en `au`) : Crée un utilisateur
- `removeuser <id>` (abrégé en `ru`) : Supprime un utilisateur
- `updateusername` (abrégé en `uun`) : Change le nom d'un utilisateur
- `updateuserpassword` (abrégé en `uupa`) : Change le mot de passe d'un utilisateur
- `updateuserpermission` (abrégé en `uupe`) : Change la permission d'un utilisateur

Cette liste n'est pas exhaustive et sera complétée plus tard. Consultez `client/console.py` pour connaître la liste complète.

---

## Installation et mise à jour
Des outils ont été développés pour faciliter la gestion des versions du projet. Pour utiliser ces outils, vous devez posséder Git sur votre ordinateur. Git est téléchargeable [ici](https://git-scm.com/).
### Installation
#### Clonage
Pour installer de zéro l'application sur votre ordinateur, il faut utiliser directement Git. C'est normalement la seule fois où vous aurez à le faire.
```
git clone https://github.com/Bidulman/bidoyon-plus
```
#### Initialisation
Ensuite, il est préférable d'initialiser les scripts de mise à jour (vous pouvez le faire à n'importe quel moment).
Depuis un terminal, placez-vous dans le dossier parent du dépôt de code :
```
dossier-parent/
| <--- VOUS ÊTES ICI
|-- bidoyon-plus/
|   |-- fichiers
```
Puis exécutez les actions en fonction de votre système d'exploitation.
###### Sous Windows
```
call bidoyon-plus\scripts\setscripts.bat
```
###### Sous Linux
```
./bidoyon-plus/scripts/setscripts.sh
```
Superbe ! Vous avez maintenant des scripts prêts à l'utilisation.

### Mise à jour
Si vous avez bien mis en place les scripts pendant l'installation, la mise à jour sans perte de données sera un jeu d'enfant.
Il vous suffit d'activer le script `updater.bat` ou `updater.sh` (en fonction de votre système d'exploitation) préalablement installé. Automatiquement, les fichiers de données seront sauvegardés et replacés dans l'application, et les scripts seront mis à jour.

Si l'option est activée dans la configuration, l'application peut vérifier elle-même si elle est à jour et vous prévenir.

---
