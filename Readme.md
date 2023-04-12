# Hands On: Neo4j

## Quick start

Cloner le projet

```bash
git clone https://github.com/tomtaranto/neo4j-prez.git
```

#### Création de l'environnement python


Lien d'installation de [Poetry](https://python-poetry.org/docs/)

```bash
poetry install
```

#### Lancement de Neo4j

Lien d'installation de [Docker](https://docs.docker.com/engine/install/)

```bash
docker run --name neo4j-trip --publish=7474:7474 --publish=7687:7687 --volume=$HOME/neo4j/data:/data neo4j
```

#### Changement du mot de passe Neo4J (requis).

Aller sur l'URL [http://localhost:7474/browser](http://localhost:7474/browser).

Dans la première cellule executer la commande :
```cypher
:server connect
```

Puis dans le formulaire se connecter en renseignant :

- username: `neo4j`
- password: `neo4j`

Et valider en appuyant sur `connect`. 

Un formulaire de changement de mot de passe va apparaitre, renseigner comme nouveau mot de passe: `neo4jneo4j`


#### Génération de données:
```bash
poetry run python main.py
```

## Comparaison avec Postgre

Lancer l'image Docker :

```bash
docker run --name postgre-trip -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=postgres -e POSTGRES_USER=postgres -v "$HOME/tmp/postgre:/var/lib/postgresql/data" -d -p 5432:5432 postgres
```

Pour analyser une requête:

```bash
poetry run python compare.py
```


## Pour aller plus loin

Ne pas hésiter à modifier les paramètres de la classe `Generator` lors de son instanciation. 

On peut jouer avec le nombre de villes, le nombre d'utilisateurs ou le nombre de trajets insérés.

On peut aussi modifier les requêtes dans le fichier `compare.py` pour mieux mettre en valeur les différences entre les deux formats.

Pour une introduction plus complète à Neo4j, on peut dans l'interface WEB taper `:play movie-graph` et suivre ce tutoriel.