import random

min_distance = 5
max_distance = 50
num_of_vertices = 150
colony_life_span = 20
num_of_ants = 35
a = 2
b = 3
p = 0.4
l_min = 0


class Ant:
    def __init__(self, distances, pheromones, initial_position):
        self.distances = distances
        self.pheromones = pheromones
        self.visited_points = [initial_position]
        self.initial_position = initial_position

    def has_used_route(self, i, j):
        result = False

        for index, point in enumerate(self.visited_points):
            if index + 1 < len(self.visited_points) and point == i and self.visited_points[index + 1] == j:
                result = True
                break

        return result

    def has_visited(self, v):
        return v in self.visited_points

    def get_distance(self):
        result = 0

        for idx, point in enumerate(self.visited_points):
            if idx != 0:
                result = result + self.distances[self.visited_points[idx - 1]][point]

        return result

    def pick_next_point_random(self):
        result = None

        while result is None:
            v = random.randint(0, num_of_vertices - 1)
            if not self.has_visited(v):
                result = v

        return result

    def calculate_probability_section(self, p1, p2, t):
        return self.pheromones[t][p1][p2] ** a * (1 / self.distances[p1][p2]) ** b

    def pick_next_point_aco(self, t):
        result = None
        result_probability = None

        current_point = self.visited_points[-1]
        for point in range(num_of_vertices):
            if point != current_point and not self.has_visited(point):
                numerator = self.calculate_probability_section(current_point, point, t)
                denominator = 0
                for j in range(num_of_vertices):
                    if j != current_point and not self.has_visited(j):
                        denominator = denominator + self.calculate_probability_section(current_point, j, t)

                probability = numerator / denominator
                # print(f"probability is {probability}")
                if result is None:
                    result = point
                    result_probability = probability
                elif result_probability < probability:
                    result = point
                    result_probability = probability

        return result

    def pick_next_point_greedy(self):
        result = None

        if (len(self.visited_points)) == 0:
            result = random.randint(0, num_of_vertices - 1)
        else:
            while result is None:
                current_point = self.visited_points[-1]
                for point, distance in enumerate(self.distances[current_point]):
                    if point != current_point and not self.has_visited(point):
                        if result is None:
                            result = point
                        elif distance < self.distances[current_point][result]:
                            result = point

        return result

    def find_path(self):
        self.visited_points = [self.initial_position]
        while len(self.visited_points) < len(self.distances):
            self.visited_points.append(self.pick_next_point_random())

    def find_path_aco(self, t):
        self.visited_points = [self.initial_position]
        while len(self.visited_points) < len(self.distances):
            self.visited_points.append(self.pick_next_point_aco(t))

    def find_l_min(self) -> int:
        self.visited_points = [self.initial_position]
        while len(self.visited_points) < len(self.distances):
            self.visited_points.append(self.pick_next_point_greedy())

        return self.get_distance()


def calculate_delta_t(ants, i, j):
    result = 0
    for ant in ants:
        if ant.has_used_route(i, j):
            result = result + l_min / ant.get_distance()

    return result


def get_best_route_data(ants):
    best_route = None
    best_length = None

    for ant in ants:
        if best_length is None:
            best_route = ant.visited_points.copy()
            best_length = ant.get_distance()
        elif ant.get_distance() < best_length:
            best_route = ant.visited_points.copy()
            best_length = ant.get_distance()

    return best_route, best_length


def main():
    global l_min

    # 1. Init distances
    distances = []
    for r in range(num_of_vertices):
        r = []
        for c in range(num_of_vertices):
            r.append(0)

        distances.append(r)

    for r in range(num_of_vertices):
        for c in range(num_of_vertices):
            d = random.randint(min_distance, max_distance)
            if r != c:
                distances[r][c] = d
                distances[c][r] = d

    # plt.plot(list(map(lambda p: p.x, points)), list(map(lambda p: p.y, points)))
    # plt.show()
    course = Ant(distances, [], random.randint(0, num_of_vertices - 1))
    course.find_path()
    print(f"Random found path is {course.get_distance()} long")
    print(course.visited_points)

    # 2. Init variables
    # See top of the file
    # 3. Calculate Lmin using a greedy algorithm
    l_min = course.find_l_min()
    print(f"Lmin = {l_min}")
    # 4. Init edges and pheromones
    pheromones = []
    for t in range(colony_life_span):
        state = []

        for row in range(num_of_vertices):
            r = []
            for col in range(num_of_vertices):
                if row == col:
                    r.append(0)
                else:
                    r.append(1)

            state.append(r)

        pheromones.append(state)

    # 5. Create ants
    ants = []
    for v in range(num_of_ants):
        ants.append(Ant(distances, pheromones, random.randint(0, num_of_vertices - 1)))

    # 6. Loop
    best_length = None
    best_route = None
    for t in range(colony_life_span):
        # 7. For each ant
        for inx, ant in enumerate(ants):
            ant.find_path_aco(t)
            print(f"Found ant path is {ant.get_distance()} for ant {inx}")

        # update best route and length
        current_best_route, current_best_length = get_best_route_data(ants)
        if best_route is None:
            best_route = current_best_route
            best_length = current_best_length
        elif current_best_length < best_length:
            print("Updating best route!")
            best_route = current_best_route
            best_length = current_best_length

        # update pheromones
        if t + 1 < colony_life_span:
            for i in range(num_of_vertices):
                for j in range(num_of_vertices):
                    if i != j:
                        delta_t = calculate_delta_t(ants, i, j)
                        pheromones[t + 1][i][j] = (1 - p) * pheromones[t][i][j] + delta_t

    print(f"Done. found best route is {best_length} long. Path: {best_route}")


if __name__ == '__main__':
    main()
