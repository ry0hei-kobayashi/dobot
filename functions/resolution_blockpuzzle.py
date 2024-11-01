import heapq

# initial_position = [
#     [4,3,7],
#     [0,6,2],
#     [5,1,8]
# ]

def resolution_blockpazzle(initial_position):
    # 目標状態
    goal_state = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]

    # 移動方向 (上、下、左、右)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # マンハッタン距離を計算
    def manhattan_distance(state):
        distance = 0
        for i in range(3):
            for j in range(3):
                if state[i][j] != 0:
                    goal_x, goal_y = divmod(state[i][j] - 1, 3)
                    distance += abs(goal_x - i) + abs(goal_y - j)
        return distance

    # パズルを解く関数
    def solve_puzzle(start_state):
        open_list = []
        heapq.heappush(open_list, (manhattan_distance(start_state), 0, start_state, []))
        visited = set()

        while open_list:
            _, cost, current_state, path = heapq.heappop(open_list)

            if current_state == goal_state:
                return path

            visited.add(tuple(map(tuple, current_state)))

            # 空白(0)の位置を探す
            empty_x, empty_y = next((i, j) for i in range(3) for j in range(3) if current_state[i][j] == 0)

            # 各方向に移動
            for dx, dy in directions:
                new_x, new_y = empty_x + dx, empty_y + dy

                if 0 <= new_x < 3 and 0 <= new_y < 3:
                    new_state = [row[:] for row in current_state]
                    new_state[empty_x][empty_y], new_state[new_x][new_y] = new_state[new_x][new_y], new_state[empty_x][empty_y]

                    if tuple(map(tuple, new_state)) not in visited:
                        new_cost = cost + 1
                        new_path = path + [[new_x, new_y]]
                        heapq.heappush(open_list, (new_cost + manhattan_distance(new_state), new_cost, new_state, new_path))

        return None  # 解が見つからない場合

    # パズルを解く
    solution_path = solve_puzzle(initial_position)
    return solution_path

r=resolution_blockpazzle(initial_position)
print(r)
