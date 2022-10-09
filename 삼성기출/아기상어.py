# start: 23:45
# end : 01:41
from collections import deque
import heapq


dx = [1, -1, 0, 0]
dy = [0, 0, 1, -1]


def check_fish(n, fishes, baby_shark):
    is_empty = True
    for row in range(n):
        for col in range(n):
            if fishes[row][col] == 9 or fishes[row][col] == 0:
                continue
            if fishes[row][col] > baby_shark[2]:
                continue
            is_empty = False
    return is_empty


def bfs(n,  baby_shark, fishes):

    visited = [[False]*n for _ in range(n)]
    queue = deque()
    queue.append((baby_shark[0], baby_shark[1], 0))
    visited[baby_shark[0]][baby_shark[1]] = True

    candidates = []

    while queue:
        x, y, distance = queue.popleft()
        for i in range(4):
            nx = x+dx[i]
            ny = y+dy[i]

            if 0 <= nx < n and 0 <= ny < n and not visited[nx][ny]:
                if fishes[nx][ny] > baby_shark[2]:
                    continue

                visited[nx][ny] = True
                if 0 == fishes[nx][ny] or baby_shark[2]:
                    # 0이거나 같은 곳은 가보자
                    queue.append((nx, ny, distance+1))

                if 0 < fishes[nx][ny] < baby_shark[2]:
                    # 아기상어보다 작거나 같으면 candidate이다
                    heapq.heappush(candidates, (distance+1, nx, ny))

    return candidates


def solution():
    # 갈 수 있는 곳에 더 이상 물고기가 없다면?

    # 갈 수 있는 곳 중
    # 먹을 수 있는 물고기가 1마리 => 먹는다
    # 먹을 수 있는 물고기가 1마리보다 크다 => 가장 가까운 물고기 먹는다.
    # 가장 가까운 물고기 == 가장 가까운 이동 거리 (BFS)
    #  가장 가까운 물고기가 많다면 ? => 가장 위 => 가장 왼쪽 물고기 먹는다.
    # sort(key = lambda x: (x[0],x[1]))
    # heapq를 사용해보자

    # 물고기 먹으면 해당 칸 물고기 0, 아기상어 크기는 자신의 크기만큼 먹으면 1 증가
    # 엄마 도움 요청하지 않고 물고기를 먹을 수 있는 시간 구하기
    n = int(input())
    fishes = []
    baby_shark = [-1, -1, 2, 0]  # [x, y, size, consume]
    time = 0
    # init fishes & baby shark
    for row in range(n):
        fish_row = list(map(int, input().split(' ')))
        fishes.append(fish_row)
        if baby_shark[0] == -1 and baby_shark[1] == -1:
            for col in range(n):
                if fish_row[col] == 9:
                    baby_shark = [row, col, 2, 0]

    while not check_fish(n, fishes, baby_shark):

        candidates = bfs(n, baby_shark, fishes)
        if not candidates:
            break
        # 가장 가깝고, 가장 왼쪽, 위의 물고기 먹자
        next_fish_to_eat = heapq.heappop(candidates)
        distance, row, col = next_fish_to_eat

        current_size = baby_shark[2]
        current_consume = baby_shark[3]
        next_size = current_size
        next_consume = current_consume + 1

        if next_consume >= current_size:
            next_size += 1
            next_consume -= current_size
        # 상어가 이동한다.
        fishes[row][col] = 9
        fishes[baby_shark[0]][baby_shark[1]] = 0
        baby_shark = [row, col, next_size, next_consume]

        time = time + distance  # 이동 거리만큼 시간 추가

    return time


print(solution())
