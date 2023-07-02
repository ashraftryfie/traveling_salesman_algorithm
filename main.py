import sys
import timeit

import game
from state import State
from cell import Cell
from init_city import get_fixed_city, get_city_from_file

# ************************* Initialize City *************************
# 1. City from file
city, truck, packages = get_city_from_file("city.txt")

# 2. fixed City
# city, truck, packages, buildings = get_fixed_city()

# ************************* Initialize State *************************
startPosition = Cell(truck.position.x, truck.position.y)
start_state = State(city, truck, packages, None, 0, startPosition)

start_state.initial_state()

start_state.print_city()

g = game.Game(start_state)

# ************************* Start Algorithms *************************
# while True:
print('1. UCS')
print('2. A*')

choice = int(input('Choose an algorithm: '))
if choice == 1:
    start = timeit.default_timer()
    g.ucs(start_state)
    g.path(g.final_state)
    end = timeit.default_timer()
    print("|--> Execution Time : {:.3f} s".format((end - start)))
    print("-" * 40)
elif choice == 2:
    start = timeit.default_timer()
    g.a_star(start_state)
    g.path(g.final_state)
    end = timeit.default_timer()
    print("|--> Execution Time : {:.3f} s".format((end - start)))
    print("-" * 40)

else:
    print('Invalid choice')
    pass
