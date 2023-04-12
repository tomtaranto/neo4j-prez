from functools import partial

from generator import Generator
import timeit


def compare():
    generator = Generator(nbr_names=10, double=True)
    generator.insert_trips(5)
    pg_call = partial(compute_nbr_of_trip_from_pau, generator, "postgre")
    neo4j_call = partial(compute_nbr_of_trip_from_pau, generator, "neo4j")
    n = 50
    result = timeit.timeit(pg_call, globals=globals(), number=n)
    print(f"Execution time for PostGres is {result / n} seconds")

    result = timeit.timeit(neo4j_call, globals=globals(), number=n)
    print(f"Execution time for Neo4j is {result / n} seconds")


def compute_nbr_of_trip_from_pau(generator, bdd="neo4j"):
    if bdd == "neo4j":
        query = "MATCH ()-[:TO]->(c:CITY {city_name:'pau'}) RETURN COUNT(*)"
        generator.conn.execute_query(query)
    elif bdd == "postgre":
        query = "select COUNT(*) FROM trip t JOIN city c ON t.from_city = c.id WHERE c.city_name LIKE 'pau'"
        generator.execute_pg_query(query)


def main():
    compare()


if __name__ == '__main__':
    main()
