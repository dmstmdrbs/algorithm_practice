n, m, k, c = map(int, input().rstrip().lstrip().split(' '))
trees = [list(map(int, input().rstrip().lstrip().split(' ')))
         for _ in range(n)]

for row in range(n):
    for col in range(n):
        if trees[row][col] == -1:
            trees[row][col] = 'w'


def is_in(row, col):
    return 0 <= row < n and 0 <= col < n


dx = [0, 0, 1, -1]
dy = [1, -1, 0, 0]


def grow_up():
    add_trees = [[0 for _ in range(n)] for _ in range(n)]

    for row in range(n):
        for col in range(n):
            # 제초제가 있거나 나무가 없거나 벽인 경우 패스
            if trees[row][col] == 'w' or trees[row][col] <= 0:
                continue
            count = 0
            for i in range(4):
                nrow = row + dx[i]
                ncol = col + dy[i]
                if is_in(nrow, ncol):
                    if trees[nrow][ncol] != 'w' and trees[nrow][ncol] > 0:
                        count += 1
            add_trees[row][col] = count
    for row in range(n):
        for col in range(n):
            if trees[row][col] == 'w' or trees[row][col] <= 0:
                continue
            trees[row][col] += add_trees[row][col]


def spread_tree():
    new_trees = [[0 for _ in range(n)] for _ in range(n)]

    for row in range(n):
        for col in range(n):
            if trees[row][col] != 'w' and trees[row][col] > 0:
                empty_pos = []
                for i in range(4):
                    nrow = row + dx[i]
                    ncol = col + dy[i]
                    if is_in(nrow, ncol) and trees[nrow][ncol] == 0:
                        empty_pos.append((nrow, ncol))
                length = len(empty_pos)
                for x, y in empty_pos:
                    new_trees[x][y] += trees[row][col] // length

    for row in range(n):
        for col in range(n):
            if new_trees[row][col] > 0:
                trees[row][col] = new_trees[row][col]


ddx = [1, 1, -1, -1]
ddy = [1, -1, 1, -1]


def find_remover_center():

    temp = []
    for row in range(n):
        for col in range(n):
            # 벽이거나 빈칸이면 따지는 의미가 없음. 해당 칸에서 퍼지지 못함
            # 현재 제초제가 뿌려진 칸이면 의미없음. 빈칸이기 때문
            if trees[row][col] == 'w' or trees[row][col] <= 0:
                continue
            count = trees[row][col]
            for i in range(4):
                for ki in range(k):
                    # 각 방향당
                    # k만큼
                    nrow = row + ddx[i] * (ki+1)
                    ncol = col + ddy[i] * (ki+1)
                    if is_in(nrow, ncol):
                        if trees[nrow][ncol] == 'w' or trees[nrow][ncol] <= 0:
                            break

                        count += trees[nrow][ncol]

            temp.append((count, row, col))
    temp.sort(key=lambda x: (-x[0], x[1], x[2]))
    if not temp:
        return (0, 0, 0)
    return temp[0]


def decrease_remover():
    for row in range(n):
        for col in range(n):
            if trees[row][col] != 'w' and trees[row][col] < 0:
                trees[row][col] += 1


def remove_trees():
    count, row, col = find_remover_center()
    if count == 0:
        return 0
    # print('center ', (row, col))
    trees[row][col] = -c
    for i in range(4):
        # 각 방향당
        for ki in range(1, k+1):
            # k만큼
            nrow = row + ddx[i] * ki
            ncol = col + ddy[i] * ki
            if is_in(nrow, ncol):
                # 벽이면 break
                if trees[nrow][ncol] == 'w':
                    break
                # 0이면 여기까지
                if trees[nrow][ncol] <= 0:
                    trees[nrow][ncol] = -c
                    break
                elif trees[nrow][ncol] > 0:
                    trees[nrow][ncol] = -c

    return count


def print_trees():
    print('-------------------')
    for row in trees:
        print(row)
    print('-------------------')


total_count = 0
# print_trees()

for _ in range(m):
    print(_)
    grow_up()
    print_trees()

    spread_tree()
    print_trees()

    decrease_remover()
    print_trees()

    total_count += remove_trees()
    print_trees()

print(total_count)
