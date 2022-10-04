from collections import deque
import heapq

directions = [[1, 0], [0, 1], [-1, 0], [0, -1]]


def is_in(n, row, col):
    return 0 <= row < n and 0 <= col < n


def bfs(taxi_pos, board, n):
    t_row, t_col = taxi_pos
    visited = [[False]*n for _ in range(n)]

    table = [[float('inf')]*n for _ in range(n)]
    table[t_row][t_col] = 0
    queue = deque()
    queue.append((t_row, t_col))
    visited[t_row][t_col] = True

    while queue:
        row, col = queue.popleft()

        for i in range(4):
            nrow, ncol = row + directions[i][0], col + directions[i][1]

            if is_in(n, nrow, ncol) and not visited[nrow][ncol] and board[nrow][ncol] != 1:
                visited[nrow][ncol] = True
                queue.append((nrow, ncol))
                table[nrow][ncol] = table[row][col]+1
    return table


def find_nearest(n, m, fuel, board, taxi_pos, picked, sources):
    table = bfs(taxi_pos, board, n)

    candidates = []
    for i in range(m):
        if picked[i]:
            continue
        row, col = sources[i][0], sources[i][1]
        dist = table[row][col]
        if dist <= fuel:
            # 거리, row,col, 승객 번호
            heapq.heappush(candidates, (dist, row, col, i))
    if not candidates:
        return -1, -1, -1, -1
    candidate = heapq.heappop(candidates)
    return candidate


def get_dist(n, board,  source, dest, fuel):
    table = bfs(source, board, n)
    row, col = dest[0], dest[1]
    distance = table[row][col]
    if distance > fuel:
        return -1
    return distance


N, M, fuel = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(N)]
ty, tx = map(int, input().split())

taxi_pos = [ty - 1, tx - 1]

passenger_start = []  # 손님들의 출발지를 저장할 리스트
passenger_end = []  # 손님들의 도착지를 저장할 리스트
picked = [False for _ in range(M)]

for _ in range(M):
    sy, sx, ey, ex = map(int, input().split())
    passenger_start.append([sy - 1, sx - 1])
    passenger_end.append([ey - 1, ex - 1])

count = M
while count:
    dist_to_passenger, row, col, passenger = find_nearest(
        N, M, fuel, board, taxi_pos, picked, passenger_start)
    if dist_to_passenger == -1:
        fuel = -1
        break
    fuel -= dist_to_passenger
    picked[passenger] = True
    taxi_pos = passenger_start[passenger]
    dist = get_dist(N, board, taxi_pos, passenger_end[passenger], fuel)
    if dist == -1:
        fuel = -1
        break
    fuel += dist
    taxi_pos = passenger_end[passenger]
    count -= 1

print(fuel)
