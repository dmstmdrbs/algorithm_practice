# 시작 : 2시 46분
# 끝 : 3시 58분
from collections import deque
import math


def get_amount_of_spread_dust(amount):
    return int(math.floor(amount / 5))


def get_remain_dust(amount, number_of_spreaded):
    return amount - get_amount_of_spread_dust(amount) * number_of_spreaded


dx = [0, 0, -1, 1]
dy = [1, -1, 0, 0]


def spread_dust(amount, air, R, C, r, c):
    def is_in(row, col):
        return 0 <= row < R and 0 <= col < C

    spreaded_dust = []
    next_amount = get_amount_of_spread_dust(amount)
    for i in range(4):
        nr = r + dx[i]
        nc = c + dy[i]
        if is_in(nr, nc) and air[nr][nc] != -1:
            spreaded_dust.append((nr, nc, next_amount))

    return spreaded_dust


def move_air(air, air_conditioner, R, C):
    r1, c1 = air_conditioner[0]  # 반시계 방향
    r2, c2 = air_conditioner[1]  # 시계 방향

    counter_clock_queue = deque([])
    clock_queue = deque([])

    # counter clock

    # add queue
    # (r1, 1 ~ C-1)
    for col in range(1, C):
        counter_clock_queue.append(air[r1][col])
    # (r1 ~ 0, C-1)
    for row in reversed(range(0, r1)):
        counter_clock_queue.append(air[row][C-1])
    # (0, C-1 ~ 0)
    for col in reversed(range(0, C - 1)):
        counter_clock_queue.append(air[0][col])
    # (0 ~ r1 - 1, 0)
    for row in range(1, r1 - 1):
        counter_clock_queue.append(air[row][0])
    # pop queue
    air[r1][c1+1] = 0  # from air conditioner
    # (r1, 2 ~ C-1)
    for col in range(2, C):
        air[r1][col] = counter_clock_queue.popleft()
    # (r1 ~ 0, C-1)
    for row in reversed(range(0, r1)):
        air[row][C-1] = counter_clock_queue.popleft()
    # (0, C-1 ~ 0)
    for col in reversed(range(0, C - 1)):
        air[0][col] = counter_clock_queue.popleft()
    # (0 ~ r1 - 1, 0)
    for row in range(1, r1):
        air[row][0] = counter_clock_queue.popleft()

    # clock
    # (r2, 1 ~ C-1)
    for col in range(1, C):
        clock_queue.append(air[r2][col])
    # (r2 ~ R-1, C-1)
    for row in range(r2 + 1, R):
        clock_queue.append(air[row][C-1])
    # (R - 1, C-1 ~ 0)
    for col in reversed(range(0, C - 1)):
        clock_queue.append(air[R - 1][col])
    # (R-1 ~ r2 + 2, 0)
    for row in reversed(range(r2 + 2, R - 1)):
        clock_queue.append(air[row][0])

    # pop queue
    air[r2][c1+1] = 0  # from air conditioner
    # (r2, 2 ~ C-1)
    for col in range(2, C):
        air[r2][col] = clock_queue.popleft()
    # (r2 ~ R-1, C-1)
    for row in range(r2 + 1, R):
        air[row][C-1] = clock_queue.popleft()
    # (0, C-1 ~ 0)
    for col in reversed(range(0, C - 1)):
        air[R - 1][col] = clock_queue.popleft()
    # (R-1 ~ r2 - 1, 0)
    for row in reversed(range(r2 + 1, R - 1)):
        air[row][0] = clock_queue.popleft()


def spread_all_dust(air, air_conditioner, R, C):
    remain_dust = []
    spreaded_dust = []  # (row,col,amount)[]
    for row in range(R):
        for col in range(C):
            if air[row][col] <= 0:
                continue
            spreaded = spread_dust(
                air[row][col], air, R, C, row, col)
            spreaded_dust.extend(spreaded)
            remain_dust.append(
                (row, col, get_remain_dust(air[row][col], len(spreaded))))

    for row, col, amount in remain_dust:
        air[row][col] = amount
    for row, col, amount in spreaded_dust:
        air[row][col] += amount

    move_air(air, air_conditioner, R, C)
    return


def get_dust_amount_in_air(air):
    total_amount = 0
    for row in air:
        for col in row:
            if col <= 0:
                continue
            total_amount += col
    return total_amount


def solution():
    R, C, T = map(int, input().split(' '))

    air = [list(map(int, input().split(' '))) for _ in range(R)]

    air_conditioner = []

    for row in range(R):
        if air[row][0] == -1:
            air_conditioner.append((row, 0))
            air_conditioner.append((row+1, 0))
            break

    for _ in range(T):
        spread_all_dust(air, air_conditioner, R, C)

    return get_dust_amount_in_air(air)


print(solution())
