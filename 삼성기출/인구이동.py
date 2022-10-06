# 시작 : 19:03
# 제출 1 : 19:41
from collections import deque
import math


def get_next_people(totoal_people, num_of_united_countries):
    return math.floor(totoal_people / num_of_united_countries)


dx = [0, 0, 1, -1]
dy = [1, -1, 0, 0]


def get_united_countries(n, countries, checked, l, r, row, col):
    checked[row][col] = True

    queue = deque()
    queue.append((row, col))
    united = [(row, col)]
    sum_of_united = countries[row][col]

    while queue:
        row, col = queue.popleft()
        current_people = countries[row][col]
        for i in range(4):
            nr = row+dx[i]
            nc = col+dy[i]
            if 0 <= nr < n and 0 <= nc < n and not checked[nr][nc] and l <= abs(current_people-countries[nr][nc]) <= r:
                checked[nr][nc] = True
                united.append((nr, nc))
                sum_of_united += countries[nr][nc]
                queue.append((nr, nc))
    return united, sum_of_united


def main():
    n, l, r = map(int, input().split(' '))
    countries = [list(map(int, input().split(' '))) for _ in range(n)]

    days = 0
    while True:
        checked = [[False]*n for _ in range(n)]
        united_countries = []
        for row in range(n):
            for col in range(n):
                if not checked[row][col]:
                    united, sum_of_united = get_united_countries(n,
                                                                 countries, checked, l, r, row, col)
                    if len(united) > 1:
                        united_countries.append((united, sum_of_united))
        # print(united_countries)
        if not united_countries:
            break

        for united, sum_of_people in united_countries:
            spread_people = get_next_people(sum_of_people, len(united))
            for row, col in united:
                countries[row][col] = spread_people
        days += 1
        # print(countries)
    print(days)


main()
