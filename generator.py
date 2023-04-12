import json

import numpy as np
import psycopg2
from neo4j import GraphDatabase, ExperimentalWarning
from tqdm import tqdm
import warnings

warnings.filterwarnings('ignore', category=ExperimentalWarning)

TRANSPORTATION_MODES = {"CAR": "CAR", "FOOT": "FOOT", "BUS": "BUS", "TRAIN": "TRAIN", "BIKE": "BIKE"}


class Generator:
    def __init__(self, nbr_names=4945, nbr_cities=75, double=False):
        self.names = open('data/names.txt', 'r').read().split('\n')
        self.cities = open('data/cities.txt', 'r').read().split('\n')
        self.names = np.random.choice(self.names, size=nbr_names, replace=False)
        self.cities = np.random.choice(self.cities, size=nbr_cities, replace=False)
        self.conf = json.load(open('connection.conf', "r"))
        self.double = double
        self.conn = self.start_conn()
        if self.double:
            self.pg_conn = self.start_pg_conn()
            self.init_pg()
        self.clean()
        self.insert_people()
        self.insert_cities()
        self.insert_transportation_modes()
        self.trip_count = 0

    def start_conn(self):
        host, user, password = self.conf["neo4j"]["host"], self.conf["neo4j"]["username"], self.conf["neo4j"][
            "password"]
        return GraphDatabase.driver(host, auth=(user, password))

    def start_pg_conn(self):
        host, user, password = self.conf["postgre"]["host"], self.conf["postgre"]["username"], self.conf["postgre"][
            "password"]
        conn = psycopg2.connect(
            user=user,
            password=password,
            database="postgres",
            port=5432,
            host="localhost"
        )
        conn.autocommit = True
        return conn

    def close(self):
        self.clean()
        self.conn.close()

    def clean(self):
        self.conn.execute_query('MATCH (n) DETACH DELETE n')
        if self.double:
            self.execute_pg_query("DELETE FROM trip")
            self.execute_pg_query("DELETE FROM person")
            self.execute_pg_query("DELETE FROM transportation_mode")
            self.execute_pg_query("DELETE FROM city")

    def init_pg(self):
        if self.double:
            create_table_person = """create table if not exists public."person"(
                "id" SERIAL primary key,
                "name" VARCHAR(20)
            )
            """
            create_table_transportation_mode = """create table if not exists public."transportation_mode"(
                        "id" SERIAL primary key,
                        "mode" VARCHAR(20)
                        )
                        """
            create_table_city = """create table if not exists public."city"(
                                    "id" SERIAL primary key,
                                    "city_name" VARCHAR(20)
                                    )
                                    """
            create_table_trip = """create table if not exists public."trip"(
                                                "trip_id" SERIAL primary key,
                                                "from_city" INT NOT NULL,
                                                "to_city" INT NOT NULL,
                                                "departure_time" TIMESTAMP,
                                                "arrival_time" TIMESTAMP,
                                                "transportation_mode"  INT NOT NULL,
                                                "person_id" INT NOT NULL,
                                                "distance" REAL,
                                                FOREIGN KEY (from_city) REFERENCES city (id),
                                                FOREIGN KEY (to_city) REFERENCES city (id),
                                                FOREIGN KEY (transportation_mode) REFERENCES transportation_mode (id),
                                                FOREIGN KEY (person_id) REFERENCES person (id)
                                                )
                                                """
            self.execute_pg_query(create_table_person)
            self.execute_pg_query(create_table_transportation_mode)
            self.execute_pg_query(create_table_city)
            self.execute_pg_query(create_table_trip)

    def execute_pg_query(self, query: str):
        cursor = self.pg_conn.cursor()
        cursor.execute(query)
        if cursor.pgresult_ptr is not None:
            return cursor.fetchall()

    def show(self):
        records, summary, keys = self.conn.execute_query('MATCH (n) RETURN *')
        print(summary.query)
        for record in records:
            print(record)
        self.show_summary_info(summary)

    @staticmethod
    def show_summary_info(summary):
        print(summary.__dict__)

    def insert_people(self):
        print("Inserting people")
        for name in self.names:
            self.conn.execute_query(f'CREATE (:PERSON {{ name:"{name}" }})')
            if self.double:
                query = f"""
                INSERT INTO public.person
                ("name")
                VALUES('{name}');
                """
                self.execute_pg_query(query)

    def insert_cities(self):
        print("Inserting cities")
        for city in self.cities:
            self.conn.execute_query(f'CREATE (:CITY {{ city_name:"{city}" }})')
            if self.double:
                query = f"""
                    INSERT INTO public.city
                    (city_name)
                    VALUES('{city}');
                    """
                self.execute_pg_query(query)

    def insert_transportation_modes(self):
        print("Inserting transportation modes")
        for mode in TRANSPORTATION_MODES:
            self.conn.execute_query(f'CREATE (:TRANSPORTATION_MODE {{ mode:"{TRANSPORTATION_MODES[mode]}" }})')
            if self.double:
                query = f"""
                    INSERT INTO public.transportation_mode
                    ("mode")
                    VALUES('{TRANSPORTATION_MODES[mode]}');
                """
                self.execute_pg_query(query)

    def insert_trips(self, number_of_trips):
        print("Inserting trips")
        for _ in tqdm(range(number_of_trips)):
            source = np.random.choice(self.cities)
            destination = np.random.choice(self.cities)
            person = np.random.choice(self.names)
            start_date = np.random.randint(0, 1000)
            end_date = np.random.randint(start_date, 1200)
            transportation_mode = np.random.choice(list(TRANSPORTATION_MODES.keys()))
            distance = np.random.uniform(0, 1000)
            trip_id = self.trip_count
            self.trip_count += 1
            insert_trip_query = f'MATCH (p:PERSON), ' \
                                f'(c1:CITY), ' \
                                f'(c2:CITY), ' \
                                f'(tm:TRANSPORTATION_MODE) ' \
                                f'WHERE p.name="{person}" ' \
                                f'AND c1.city_name="{source}" ' \
                                f'AND c2.city_name="{destination}" ' \
                                f'AND tm.mode="{transportation_mode}" ' \
                                f'MERGE (p)-[:STARTED_TRIP {{ date:"{start_date}", trip_id:{trip_id} }}]->' \
                                f'(t:TRIP {{ distance:{distance}, trip_id:{trip_id} }})-[:FROM {{ departure_time:{start_date}, trip_id:{trip_id} }}]' \
                                f'->(c1)-[:TO {{ arrival_time:{end_date}, trip_id:{trip_id} }}]->(c2) ' \
                                f'CREATE (t)-[:USING]->(tm) ' \
                                f'RETURN *'
            self.conn.execute_query(insert_trip_query)
            if self.double:
                query = f"""
                    INSERT INTO public.trip
                    (from_city, to_city, departure_time, arrival_time, transportation_mode, person_id, distance)
                    VALUES((SELECT id FROM city WHERE city_name LIKE '{source}'), (SELECT id FROM city WHERE city_name LIKE '{destination}'), to_timestamp('{start_date}'), to_timestamp('{end_date}'), (SELECT id FROM transportation_mode WHERE mode LIKE '{transportation_mode}'), (SELECT id FROM person WHERE name LIKE '{person}'), {distance});
                    """
                self.execute_pg_query(query)
