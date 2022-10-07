# start : 14:00
# end : 16:13
from collections import deque


INF = float('inf')
WALL = '-'
ACTIVE_VIRUS = 0
INACTIVE_VIRUS = '*'

dx = [1, -1, 0, 0]
dy = [0, 0, 1, -1]


def is_in(n, row, col):
    return 0 <= row < n and 0 <= col < n


def bfs(lab, n, virus):
    queue = deque(virus)
    visited = [[-1 for _ in range(n)] for _ in range(n)]

    for row, col in virus:
        visited[row][col] = 0

    max_time = 0
    while queue:
        row, col = queue.popleft()

        for i in range(4):
            nrow = row+dx[i]
            ncol = col+dy[i]
            if is_in(n, nrow, ncol):
                # 빈칸 일 대
                if lab[nrow][ncol] == 0 and visited[nrow][ncol] == -1:
                    visited[nrow][ncol] = visited[row][col] + 1
                    max_time = max(visited[nrow][ncol], max_time)
                    queue.append((nrow, ncol))
                # 비활성 바이러스일 대
                elif lab[nrow][ncol] == 2 and visited[nrow][ncol] == -1:
                    visited[nrow][ncol] = visited[row][col] + 1
                    queue.append((nrow, ncol))

    for row in range(n):
        for col in range(n):
            if lab[row][col] != 1 and visited[row][col] == -1:
                return INF
    return max_time


def print_lab(lab):
    for row in lab:
        print(row)
    print()


def combine(iter, k):
    answer = []

    def dfs(elements, start, target):
        if target == 0:
            answer.append(elements[:])
            return

        for i in range(start, len(iter)):
            elements.append(iter[i])
            dfs(elements, i+1, target - 1)
            elements.pop()
    dfs([], 0, k)
    return answer


n, m = map(int, input().split(' '))

lab = [list(map(int, input().split(' '))) for _ in range(n)]
virus_positions = []
for i in range(n):
    for j in range(n):
        if lab[i][j] == 2:
            virus_positions.append((i, j))
answer = INF

for virus in combine(virus_positions, m):
    answer = min(bfs(lab, n, virus), answer)

if answer == INF:
    print(-1)
else:
    print(answer)
