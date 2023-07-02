from cell import Cell
from truck import Truck
from package import Package

city_file = []
truck = None
packages = []
buildings = []


def get_fixed_city():
    # City size
    m = 6  # width
    n = 4  # height

    # Initialize city
    city = [['.'] * m for i in range(n)]

    # Make buildings in the city
    buildings.append(Cell(1, 1))
    buildings.append(Cell(1, 2))
    buildings.append(Cell(2, 2))
    buildings.append(Cell(2, 3))

    for b in buildings:
        city[b.x][b.y] = '#'

    # Initialize packages positions
    pack1 = Package(0, Cell(3, 0), Cell(0, 0))
    pack2 = Package(1, Cell(1, 3), Cell(3, 5))
    packages.append(pack1)
    packages.append(pack2)

    # Initialize Truck Position
    truck = Truck(Cell(0, 5), 1)

    return city, truck, packages, buildings


def get_package_by_id(d_id):
    for p in packages:
        if p.id == d_id:
            return p, True
    return None, False


def get_city_from_file(file_name):
    with open(file_name, 'r') as file:
        tmp = []
        for line in file:
            tmp.append(''.join(line.split()))

        is_num = False

        for r_i, r in enumerate(tmp):

            city_file.append([])

            n_items = 0

            for i in range(len(r)):

                if r[i] != '.':
                    if r[i] == 'T':
                        truck = Truck(Cell(r_i, n_items), 1)

                    elif r[i] == 'P':
                        d, condition = get_package_by_id(r[i + 1])
                        if condition:
                            d.source = Cell(r_i, n_items)
                        else:
                            pack = Package(r[i + 1], Cell(r_i, n_items), None)
                            packages.append(pack)
                        n_items -= 1

                    elif r[i] == 'D':
                        p, condition = get_package_by_id(r[i + 1])
                        if condition:
                            p.destination = Cell(r_i, n_items)
                        else:
                            pack = Package(r[i + 1], None, Cell(r_i, n_items))
                            packages.append(pack)
                        n_items -= 1

                n_items += 1

                if r[i] in ['D', 'P']:
                    city_file[r_i].append(
                        r[i] + r[i + 1]
                    )
                    is_num = True
                elif is_num:
                    is_num = False
                    continue
                else:
                    city_file[r_i].append(
                        r[i]
                    )

    return city_file, truck, packages
