import sys
from math import sqrt

sys.setrecursionlimit(4000)


class Game:
    visited_states = []
    queue = []
    final_state = None
    name = ''

    def __init__(self, begain_state):
        self.begain_state = begain_state
        self.count = 0

    # **************************** UCS *******************************
    def ucs(self, state):
        self.name = 'UCS'
        print('\n********* UCS *********')
        self.visited_states.append(state)
        self.queue.append(state)
        self.count += 1
        # queue
        while len(self.queue) > 0:
            node = self.pop()
            self.count += 1
            # node.print_city()
            print(self.count)
            # print(node.cost)
            if node.goal():
                # node.print_city()
                self.final_state = node
                # print(self.count)
                # print(node.cost)
                break
            next_state = node.next_states()
            for ch_state in next_state:
                if ch_state not in self.visited_states:
                    self.visited_states.append(ch_state)
                    self.queue.append(ch_state)

    # **************************** A* *******************************
    def a_star(self, state):
        self.name = 'A star'

        print('\n********* A_star *********')
        self.visited_states.append(state)
        self.queue.append(state)
        self.count += 1
        # queue
        while len(self.queue) > 0:

            node = self.pop_star()
            self.count += 1
            print(self.count)

            if node.goal():
                self.final_state = node
                # node.print_city()
                # print(self.count)
                # print(node.cost)
                break

            next_state = node.next_states()

            for ch_state in next_state:
                if ch_state not in self.visited_states:
                    self.visited_states.append(ch_state)
                    self.queue.append(ch_state)

    # **************************** Printing Path *******************************
    def path(self, state):
        c = 0
        path_list = []
        cost = state.cost
        print('\n\n***************** Solution Path *****************')
        while state.parent:
            path_list.append(state)
            state = state.parent
            c += 1

        for i in range(len(path_list)):
            # print(f"\n# State-{i + 1}")
            s = path_list.pop()
            print(f"\n# State({i + 1}) cost: {s.cost}")
            s.print_city()


        print("\n", end="")
        print(f'\n-----------------(example)----------------')

        self.begain_state.print_city()
        print(f'\n-----------------({self.name})----------------')
        # print("-" * 40)
        print(f"|--> Cost of path : {c}")
        print(f"|--> Cost of solution : {cost}")
        print(f"|--> Number of generated nodes: {self.count}")

    # **************************** Get Less Cost *******************************
    def pop(self):
        min_cost = self.queue[0]
        state_index = 0
        for i, state in enumerate(self.queue):
            if min_cost.cost > state.cost:
                min_cost = state
                state_index = i
        return self.queue.pop(state_index)

    # **************************** Heuristic [Manhattan Distance] *******************************
    def manhattan_distance(self, state):  # abs(x_cur - x_goal) + abs(y_cur - y_goal)
        return abs(state.truck.position.x - state.start.x) + abs(state.truck.position.y - state.start.y)

    # **************************** Heuristic (1) *******************************
    def h_f1(self, state):  # sqrt( (x_end - x_start)**2 + (x_end - x_start)**2 )
        return sqrt(
            pow(state.truck.position.x - state.start.x, 2)
            + pow(state.truck.position.y - state.start.y, 2)
        )

    # **************************** Heuristic (2) *******************************
    def h_f2(self, state, p):
        if not p.taken:
            return sqrt(  # between (truck & package)
                pow(state.truck.position.x - p.source.x, 2)
                + pow(state.truck.position.y - p.source.y, 2)
            ) + sqrt(  # between (source.package & dist.package)
                pow(p.destination.x - p.source.x, 2)
                + pow(p.destination.y - p.source.y, 2)
            )
        else:
            return sqrt(
                pow(state.truck.position.x - p.destination.x, 2)
                + pow(state.truck.position.y - p.destination.y, 2)
            )

    def max_cost(self, state):
        max_pack = state.packages[0]
        for p in state.packages:
            if self.h_f2(state, max_pack) < self.h_f2(state, p):
                max_pack = p
        return self.h_f2(state, max_pack)

    # **************************** Heuristic (3) *******************************
    def h_f3(self, state):
        # if state.package.taken!=True:
        return self.max_cost(state)

    def pop_star(self):
        c = self.queue[0]
        state_index = 0
        for i, state in enumerate(self.queue):
            if c.cost + self.h_f2(c, state.packages[0]) > state.cost + self.h_f2(state,state.packages[0]):
                c = state
                state_index = i
        return self.queue.pop(state_index)

    # **************************** Old Functions *******************************
    # def old_pop(self):
    #     c = 0
    #     r = 0
    #     for n, i in enumerate(self.queue):
    #         if c == 0:
    #             c = i
    #             r = n
    #         elif c.cost > i.cost:
    #             c = i
    #             r = n
    #     return self.queue.pop(r)

    # def old_pop_star(self):
    #     c = 0
    #     r = 0
    #     for n, i in enumerate(self.queue):
    #         if c == 0:
    #             c = i
    #             r = n
    #         elif c.cost + self.max_cost(c) > i.cost + self.max_cost(i):
    #             c = i
    #             r = n
    #     return self.queue.pop(r)
