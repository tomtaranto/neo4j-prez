# Hands On: Neo4j

## Quick start

Cloner le projet

```bash
git clone #TODO
```

#### Création de l'environnement python

```bash
poetry install
```

#### Lancement de Neo4j

```bash
docker run --publish=7474:7474 --publish=7687:7687 --volume=$HOME/neo4j/data:/data neo4j
```

#### Changement du mot de passe Neo4J (requis).

Aller sur l'URL `http://localhost:7474/browser/`, puis dans le formulaire renseigner :

- username: `neo4j`
- password: `neo4j`

Et valider en appuyant sur `connect`. 

Un formulaire de changement de mot de passe va apparaitre, renseigner comme mot de passe: `neo4jneo4j`


#### Génération de données:
```bash
poetry run python main.py
```

## Comparaison avec Postgre

Lancer l'image Docker :

```bash
docker run --name postgre-trip2 -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=postgres -e POSTGRES_USER=postgres -v "$HOME/tmp/postgre:/var/lib/postgresql/data" -d -p 5432:5432 postgres
```

Pour analyser une requete:

```bash
poetry run python compare.py
```


## Pour aller plus loin

Ne pas hésiter à modifier les paramètres de la classe `Generator` lors de son instanciation. 

On peut jouer avec le nombre de villes, le nombre d'utilisateurs ou le nombre de trajets insérés.

On peut aussi modifier les requêtes dans le fichier `compare.py` pour mieux mettre en valeur les différences entre les deux formats.

Pour une introduction plus complète à Neo4j, on peut dans l'interface WEB taper `:play movie-graph` et suivre ce tutoriel.