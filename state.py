import copy
from termcolor import colored


class State:

    def __init__(self, city, truck, packages, parent, cost, start):
        self.city = city
        self.truck = truck
        self.packages = packages
        self.parent = parent
        self.cost = cost
        self.start = start
        self.city_width = len(city[0])  # width (m)
        self.city_height = len(city)  # height (n)

    # ************************** Goal **************************
    def goal(self):
        for p in self.packages:
            if not p.done:
                return False
        if self.truck.position == self.start:
            print("Job done successfully!")
            return True
        return False

    def __eq__(self, other):
        if hasattr(self, 'city'):
            if hasattr(other, 'city'):
                return self.city == other.city
            return False
        return True

    # ************************** Initialize Problem **************************
    def initial_state(self):
        self.city[self.truck.position.x][self.truck.position.y] = "T"

        for p in self.packages:
            sn = ''
            dn = ''
            s = '.'
            d = '.'
            if not p.taken:
                if self.city[p.source.x][p.source.y] == "T":
                    sn = ",T"
                s = 'P' + str(p.id)
            else:
                if self.city[p.source.x][p.source.y] == "T":
                    sn = "T"
                    s = ''
            self.city[p.source.x][p.source.y] = s + sn

            if not p.done:
                if self.city[p.destination.x][p.destination.y] == "T":
                    dn = ",T"
                d = 'D' + str(p.id)
            else:
                if self.city[p.destination.x][p.destination.y] == "T":
                    dn = "T"
                    d = ''
            self.city[p.destination.x][p.destination.y] = d + dn

    # ************************** Move **************************
    def can_move(self, truck, direction):
        tx = truck.position.x
        ty = truck.position.y

        if direction == 'U':
            return tx - 1 >= 0 and self.city[tx - 1][ty] != '#'

        if direction == 'D':
            return tx + 1 < self.city_height and self.city[tx + 1][ty] != '#'

        if direction == 'R':
            return ty + 1 < self.city_width and self.city[tx][ty + 1] != '#'

        if direction == 'L':
            return ty - 1 >= 0 and self.city[tx][ty - 1] != '#'
        return False

    def move(self, truck, d):
        self.city[truck.position.x][truck.position.y] = '.'
        if d == 'R':
            truck.position.y += 1
        elif d == 'L':
            truck.position.y -= 1
        elif d == 'U':
            truck.position.x -= 1
        elif d == 'D':
            truck.position.x += 1
        self.initial_state()

    # ************************** Helper for next_states() **************************
    def has_source_package(self, cell):
        for i, pn in enumerate(self.packages):
            if (pn.source.x == cell.x) and (pn.source.y == cell.y):
                return pn, i
        return False, None

    def has_destination_package(self, cell):
        for i, dn in enumerate(self.packages):
            if (dn.destination.x == cell.x) and (dn.destination.y == cell.y):
                return dn, i
        return False, None

    def num_packages(self):
        c = 0
        for i in self.packages:
            if i.taken and not i.done:
                c = c + 1
        return c

    # ************************** Next states **************************
    def next_states(self):
        l = []
        pack, pack_index = False, None

        # North
        if self.can_move(self.truck, 'U'):
            new_state = copy.deepcopy(self)
            new_state.move(new_state.truck, 'U')
            new_state.parent = self
            new_state.cost = self.cost + 1 + new_state.num_packages()
            l.append(new_state)

        # South
        if self.can_move(self.truck, 'D'):
            new_state = copy.deepcopy(self)
            new_state.move(new_state.truck, 'D')
            new_state.parent = self
            new_state.cost = self.cost + 1 + new_state.num_packages()
            l.append(new_state)

        # East
        if self.can_move(self.truck, 'R'):
            new_state = copy.deepcopy(self)
            new_state.move(new_state.truck, 'R')
            new_state.parent = self
            new_state.cost = self.cost + 1 + new_state.num_packages()
            l.append(new_state)

        # West
        if self.can_move(self.truck, 'L'):
            new_state = copy.deepcopy(self)
            new_state.move(new_state.truck, 'L')
            new_state.parent = self
            new_state.cost = self.cost + 1 + new_state.num_packages()
            l.append(new_state)

        # Receive
        pack, pack_index = self.has_source_package(self.truck.position)
        if pack:
            new_state = copy.deepcopy(self)
            # new_state.has_source_package(new_state.truck.position).taken = True
            new_state.packages[pack_index].taken = True
            new_state.move(new_state.truck, 'no')
            new_state.parent = self
            # new_state.cost = self.cost + new_state.num_packages()
            l.append(new_state)

        # Delivery
        pack, pack_index = self.has_destination_package(self.truck.position)
        if pack:
            if pack.taken:
                new_state = copy.deepcopy(self)
                # new_state.has_destination_package(new_state.truck.position).done = True
                new_state.packages[pack_index].done = True
                new_state.move(new_state.truck, 'no')
                new_state.parent = self
                # new_state.cost = self.cost + new_state.num_packages()
                l.append(new_state)
        return l

    # ************************** Display city **************************
    def print_city(self):
        width = self.city_width * 5 + 6
        print(colored('=' * width, 'white'), end="")
        for n, i in enumerate(self.city):
            print('')
            print(colored("{:<3}".format("||"), 'white'), end='')
            for j in i:
                if j == 'T':
                    print(colored("{:^5}".format(j), 'blue'), end='')

                elif j == '#':
                    print(colored("{:^5}".format(j), 'red'), end='')

                elif 'P' in j:
                    print(colored("{:^5}".format(j), 'yellow'), end='')

                elif 'D' in j:
                    print(colored("{:^5}".format(j), 'green'), end='')

                else:
                    print("{:^5}".format(j), end='')
            else:
                print(colored("{:>3}".format("||"), 'white'), end='')

        print()
        print(colored('=' * width, 'white'))

    # ************************** Old Next states **************************
    # def next_old_states(self):
    #     l = []
    #
    #     if self.can_move(self.truck, 'L'):
    #         new_state = copy.deepcopy(self)
    #         new_state.move(new_state.truck, 'L')
    #         new_state.parent = self
    #         new_state.cost = self.cost + 1 + new_state.num_packages()
    #         l.append(new_state)
    #         if self.has_source_package(self.truck.position):
    #             new_state = copy.deepcopy(self)
    #             new_state.has_source_package(new_state.truck.position).taken = True
    #             new_state.move(new_state.truck, 'L')
    #             new_state.parent = self
    #             new_state.cost = self.cost + 1 + new_state.num_packages()
    #             l.append(new_state)
    #         if self.has_destination_package(self.truck.position):
    #             if self.has_destination_package(self.truck.position).taken:
    #                 new_state = copy.deepcopy(self)
    #                 new_state.has_destination_package(new_state.truck.position).done = True
    #                 new_state.parent = self
    #                 new_state.cost = self.cost + 1 + new_state.num_packages()
    #                 new_state.move(new_state.truck, 'L')
    #                 l.append(new_state)
    #
    #     if self.can_move(self.truck, 'R'):
    #         new_state = copy.deepcopy(self)
    #         new_state.move(new_state.truck, 'R')
    #         new_state.parent = self
    #         new_state.cost = self.cost + 1 + new_state.num_packages()
    #         l.append(new_state)
    #         if self.has_source_package(self.truck.position):
    #             new_state = copy.deepcopy(self)
    #             new_state.has_source_package(new_state.truck.position).taken = True
    #             new_state.move(new_state.truck, 'R')
    #             new_state.parent = self
    #             new_state.cost = self.cost + 1 + new_state.num_packages()
    #             l.append(new_state)
    #         if self.has_destination_package(self.truck.position):
    #             if self.has_destination_package(self.truck.position).taken:
    #                 new_state = copy.deepcopy(self)
    #                 new_state.has_destination_package(new_state.truck.position).done = True
    #                 new_state.move(new_state.truck, 'R')
    #                 new_state.parent = self
    #                 new_state.cost = self.cost + 1 + new_state.num_packages()
    #                 l.append(new_state)
    #     if self.can_move(self.truck, 'U'):
    #         new_state = copy.deepcopy(self)
    #         new_state.move(new_state.truck, 'U')
    #         new_state.parent = self
    #         new_state.cost = self.cost + 1 + new_state.num_packages()
    #         # new_state.car.clear()
    #         l.append(new_state)
    #         if self.has_source_package(self.truck.position):
    #             new_state = copy.deepcopy(self)
    #             new_state.has_source_package(new_state.truck.position).taken = True
    #             new_state.move(new_state.truck, 'U')
    #             new_state.parent = self
    #             new_state.cost = self.cost + 1 + new_state.num_packages()
    #             l.append(new_state)
    #         if self.has_destination_package(self.truck.position):
    #             if self.has_destination_package(self.truck.position).taken:
    #                 new_state = copy.deepcopy(self)
    #                 new_state.has_destination_package(new_state.truck.position).done = True
    #                 new_state.move(new_state.truck, 'U')
    #                 new_state.parent = self
    #                 new_state.cost = self.cost + 1 + new_state.num_packages()
    #                 l.append(new_state)
    #     if self.can_move(self.truck, 'D'):
    #         new_state = copy.deepcopy(self)
    #         new_state.move(new_state.truck, 'D')
    #         new_state.parent = self
    #         new_state.cost = self.cost + 1 + new_state.num_packages()
    #         l.append(new_state)
    #         if self.has_source_package(self.truck.position):
    #             new_state = copy.deepcopy(self)
    #             new_state.has_source_package(new_state.truck.position).taken = True
    #             new_state.move(new_state.truck, 'D')
    #             new_state.parent = self
    #             new_state.cost = self.cost + 1 + new_state.num_packages()
    #             l.append(new_state)
    #         if self.has_destination_package(self.truck.position):
    #             if self.has_destination_package(self.truck.position).taken:
    #                 new_state = copy.deepcopy(self)
    #                 new_state.has_destination_package(new_state.truck.position).done = True
    #                 new_state.parent = self
    #                 new_state.cost = self.cost + 1 + new_state.num_packages()
    #                 new_state.move(new_state.truck, 'D')
    #                 l.append(new_state)
    #     return l
