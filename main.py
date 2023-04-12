from generator import Generator


def main():
    generator = Generator(nbr_names=30)
    generator.insert_trips(30)
    generator.show()


if __name__ == '__main__':
    main()

# Pour run:
# sudo docker run     --publish=7474:7474 --publish=7687:7687     --volume=$HOME/neo4j/data:/data     neo4j
# Disponible : http://localhost:7474/

# docker run --name postgre-trip   -e POSTGRES_PASSWORD=postgres   -e POSTGRES_DB=postgres   -e POSTGRES_USER=postgres   -v "/home/tom/tmp-postgre:/var/lib/postgresql/data"   -d -p 5432:5432 postgres
