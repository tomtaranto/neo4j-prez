# Liste de requetes


Les trajets qui sont allé vers Pau
```cypher
MATCH (t:TRIP)-[f:FROM]->(c1:CITY)-[to:TO]->(c2:CITY) WHERE t.trip_id=f.trip_id and t.trip_id=to.trip_id and c2.city_name="pau" RETURN t,c1,c2
```

Le nombre de trajet vers Pau par ville
```cypher
MATCH (c1:CITY)-->(c2:CITY) WHERE c2.city_name="pau" RETURN c1, COUNT(c1) order by c1.city_name
```

Les gens qui n'ont pas fait de trajets:
```cypher
MATCH (p:PERSON) WHERE NOT (p)-[:STARTED_TRIP]->() RETURN p
```