import heapq
import math

n, m, k = map(int, input().split())

# 각 칸에 여러개의 나무가 있다. 어린 나무부터 양분을 흡수한다.
grid = [[[] for _ in range(n)] for _ in range(n)]  # 나무 테이블
remain_fees = [[5]*n for _ in range(n)]  # 양분 테이블
fees = [list(map(int, input().split(' '))) for _ in range(n)]


for _ in range(m):
    r, c, age = map(int, input().split(' '))
    r = r-1
    c = c-1
    grid[r][c].append(age)


# 각 칸의 나무는 양분을 먹지 못하는 순간 죽는다.

# 봄   => 나무가 자신의 나이만큼 양분을 먹고, 나이가 1 증가한다.
def do_spring_summer(n, grid, remain_fees):

    for row in range(n):
        for col in range(n):
            grid[row][col].sort()

            for idx, tree in enumerate(grid[row][col]):
                if tree > remain_fees[row][col]:
                    # 이 뒤는 다 죽는다
                    # 여름 => 봄에 죽은 나무가 양분으로 벼함. 나무가 죽으면 Math.floor(age / 2) 만큼 칸의 양분이 증가한다.
                    for dead in grid[row][col][idx:]:
                        remain_fees[row][col] += dead // 2

                    grid[row][col] = grid[row][col][:idx]
                    break
                else:
                    # 성장
                    grid[row][col][idx] += 1
                    remain_fees[row][col] -= tree


# 가을 => 나무 번식 => 나무의 나이가 5의 배수, 인접한 칸에 나이가 1인 나무 생성


def do_autumn(n, grid):
    new_trees = []
    for row in range(n):
        for col in range(n):
            for tree in grid[row][col]:
                if tree > 0 and tree % 5 == 0:
                    grow_new_trees(n, grid, row, col)
    return

# 겨울 => 양분 추가. 추가 양분의 양 A[r][c]


def do_winter(n, remain_fees, origin_fees):
    for row in range(n):
        for col in range(n):
            remain_fees[row][col] += origin_fees[row][col]
    return


dx = [-1, -1, -1, 0, 0, 1, 1, 1]
dy = [-1, 0, 1, -1, 1, -1, 0, 1]


def is_in_grid(length, row, col):
    return 0 <= row < length and 0 <= col < length


def grow_new_trees(n, grid, row, col):
    for i in range(8):
        nr = row + dx[i]
        nc = col + dy[i]
        if is_in_grid(n, nr, nc):
            grid[nr][nc].append(1)


def count_trees(grid):
    count = 0
    for row in grid:
        for trees in row:
            for tree in trees:
                if tree > 0:
                    count += 1

    return count


def print_fees(fees):
    for row in fees:

        print(row)


count = 0
while k:
    do_spring_summer(n, grid, remain_fees)

    do_autumn(n, grid)
    do_winter(n, remain_fees, fees)
    k -= 1

count = count_trees(grid)
print(count)
