from generator import Generator


def main():
    generator = Generator(nbr_names=30)
    generator.insert_trips(30)
    generator.show()


if __name__ == '__main__':
    main()
