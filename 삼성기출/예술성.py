# start 22:44
# end 02:30
from collections import deque, defaultdict
from copy import deepcopy

dx = [-1, 0, 0, 1]
dy = [0, -1, 1, 0]
# 상, 좌, 우, 하


def is_in(n, row, col):
    return 0 <= row < n and 0 <= col < n


def calculate_collaboration_score(n, groupA, groupB):
    number_a = groupA['number']
    group_a_length = groupA['length']
    number_b = groupB['number']
    group_b_length = groupB['length']
    adj_count = 0

    group_a_items = groupA['items']
    group_b_items = groupB['items']

    for item in group_a_items:
        x, y = item
        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if is_in(n, nx, ny) and (nx, ny) in group_b_items:
                adj_count += 1

    # print('(',group_a_length,'+',group_b_length,')','*',number_a,'*',number_b,'*',adj_count)
    return (group_a_length + group_b_length) * number_a * number_b * adj_count


def get_group(n, board, visited, row, col):
    queue = deque([(row, col)])
    number = board[row][col]
    # count = 1
    visited[row][col] = True
    current_group = set()
    current_group.add((row, col))

    length = 1

    while queue:
        x, y = queue.popleft()

        for i in range(4):
            nx = x + dx[i]
            ny = y + dy[i]
            if is_in(n, nx, ny) and not visited[nx][ny]:
                if board[nx][ny] == number:
                    visited[nx][ny] = True
                    queue.append((nx, ny))
                    current_group.add((nx, ny))
                    length += 1

    return length, number, current_group


def get_groups(n, board, visited):
    groups = []
    score = 0
    for row in range(n):
        for col in range(n):
            if not visited[row][col]:
                length, number, group = get_group(n, board, visited, row, col)
                group_info = dict()
                group_info['length'] = length
                group_info['items'] = group
                group_info['number'] = number
                groups.append(group_info)
    return groups


def rotate_sub_matrix(board, n, start_row, end_row, start_col, end_col):  # (시작, 끝+1)
    # 위아래 반으로 접자
    half_n = n // 2
    for row_offset in range(0, half_n // 2):
        row = start_row + row_offset
        swap_row = end_row - row_offset - 1
        for col in range(start_col, end_col):
            board[row][col], board[swap_row][col] = board[swap_row][col], board[row][col]

    # transpose
    for row_offset in range(1, (n // 2)):
        check_row = start_row + row_offset
        for col_offset in range(0, row_offset):
            check_col = start_col + col_offset
            board[check_row][check_col], board[check_col][check_row] = board[check_col][check_row], board[check_row][check_col]


def rotate_cross(n, board):
    queue = deque()
    half = n//2
    for row in range(0, half):
        item = board[row][half]
        queue.append(item)
        board[row][half] = board[half][n - row - 1]

    for col in range(n, n//2):
        item = board[half][col]
        queue.append(item)
        board[half][col] = queue.popleft()

    for row in range(n - 1, half, -1):
        item = board[row][half]
        queue.append(item)
        board[row][half] = queue.popleft()

    for col in range(n-1, half, -1):
        board[half][col] = queue.popleft()


def rotate_entire_matrix(n, board):
    mx = n//2
    my = n//2
    new_board = deepcopy(board)
    # 가운데 돌려주기
    # 가운데 1
    for y in range(my):
        new_board[n-1-y][my] = board[mx][y]
        # print(mx,y,N-1-y,my)
    # 가운데 2
    for x in range(n-1, mx, -1):
        new_board[mx][x] = board[x][my]
        # print(x,my,mx,x)

    # 가운데 3
    for y in range(n-1, my, -1):
        new_board[n-1-y][my] = board[mx][y]
        # print(mx,y,N-1-y,my)
    # 가운데 4
    for x in range(mx):
        new_board[mx][x] = board[x][my]
        # print(x,my,mx,x)

    # 90도 회전
    # 1구역

    for x in range(mx):
        for y in range(my):
            new_board[y][my-x-1] = board[x][y]

    # 2구역
    for x in range(mx):
        for y in range(my+1, n):
            new_board[y-my-1][n - x-1] = board[x][y]

    # 3구역
    for x in range(mx+1, n):
        for y in range(my):
            new_board[mx + 1 + y][n - x-1] = board[x][y]
    # 4구역
    for x in range(mx+1, n):
        for y in range(my+1, n):
            new_board[n - my + y - n//2 - 1][n + mx - x] = board[x][y]

    return new_board


def main():
    n = int(input().rstrip())
    board = [list(map(int, input().rstrip().split(' '))) for _ in range(n)]

    total_score = 0
    for _ in range(4):
        visited = [[False] * n for _ in range(n)]
        groups = []

        groups = get_groups(n, board, visited)

        score = 0
        group_length = len(groups)

        for group_index in range(0, group_length):
            for adj_group_index in range(group_index+1, group_length):
                temp_score = calculate_collaboration_score(
                    n, groups[group_index], groups[adj_group_index])
                score += temp_score

        total_score += score

        board = rotate_entire_matrix(n, board)

    return total_score


print(main())
