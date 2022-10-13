
from collections import deque

dx = [1, -1, 0, 0]
dy = [0, 0, 1, -1]


def is_in(row, col):
    return 0 <= row < n and 0 <= col < n


def bfs(visited, x, y):
    queue = deque([(x, y)])
    members = set([(x, y)])
    head, tail = (x, y), (x, y)

    while queue:
        row, col = queue.popleft()
        if board[row][col] == 1:
            head = (row, col)
        elif board[row][col] == 3:
            tail = (row, col)

        for i in range(4):
            nrow, ncol = row + dx[i], col + dy[i]
            if is_in(nrow, ncol) and not visited[nrow][ncol] and 0 < board[nrow][ncol] <= 4:
                if board[nrow][ncol] == 4:
                    visited[nrow][ncol] = True
                    continue
                members.add((nrow, ncol))
                queue.append((nrow, ncol))
                visited[nrow][ncol] = True

    return members, head, tail


def get_teams():
    teams = []
    visited = [[False]*n for _ in range(n)]

    for row in range(n):
        for col in range(n):
            if not visited[row][col] and board[row][col] == 1:
                visited[row][col] = True
                team, head, tail = bfs(visited, row, col)

                teams.append({
                    'members': team,
                    'head': head,
                    'tail': tail
                })

    return teams


def get_first_met_position(round):
    found = (-1, -1)
    if 1 <= round <= n:
        # print('공 방향:왼->오')
        row = round - 1
        for col in range(n):
            if 0 < board[row][col] < 4:
                found = (row, col)
                break
    elif n < round <= 2*n:
        # print('공 방향:아래->위')
        col = round - n - 1
        for row in reversed(range(n)):
            if 0 < board[row][col] < 4:
                found = (row, col)
                break
    elif 2*n < round <= 3*n:
        # print('공 방향:오->왼')
        row = (round - 2*n) - 1
        row = n - row - 1
        for col in reversed(range(n)):
            if 0 < board[row][col] < 4:
                found = (row, col)
                break
    elif 3*n < round < 4*n or round == 0:
        col = round - 3*n - 1
        col = n - col - 1
        # print('공 방향:위->아래')
        if round == 0:
            col = 0
        for row in (range(n)):
            if 0 < board[row][col] < 4:
                found = (row, col)
                break
    return found


def get_head_tail(position):
    found_head = (-1, -1)
    found_tail = (-1, -1)
    for team in teams:
        team_members = team['members']
        if position in team_members:
            found_head = team['head']
            found_tail = team['tail']
            break
    return found_head, found_tail


def get_place_of_member_in_team(head, member):
    # current_team에서 head로부터 몇 번째에 속하는지 탐색
    queue = deque([(head[0], head[1], 1)])
    visited = [[False]*n for _ in range(n)]
    visited[head[0]][head[1]] = True

    place_of_member = 1
    path = []
    while queue:
        row, col, place = queue.popleft()
        if row == member[0] and col == member[1]:
            place_of_member = place
            break
        for i in range(4):
            nrow = row + dx[i]
            ncol = col + dy[i]

            if is_in(nrow, ncol) and not visited[nrow][ncol]:
                if (row, col) == head:
                    if board[nrow][ncol] == 2:
                        visited[nrow][ncol] = True
                        queue.append((nrow, ncol, place+1))
                        # path.append((nrow, ncol))
                    else:
                        continue
                else:
                    if board[nrow][ncol] in [2, 3]:
                        visited[nrow][ncol] = True
                        queue.append((nrow, ncol, place+1))
                        # path.append((nrow, ncol))
    # print(path)
    return place_of_member


def move_team():
    for idx, team in enumerate(teams):
        head = team['head']
        tail = team['tail']
        members = team['members']

        new_head = (-1, -1)
        new_tail = (-1, -1)

        for i in range(4):
            nrow, ncol = head[0] + dx[i], head[1] + dy[i]
            if is_in(nrow, ncol):
                # head 와 tail이 붙어있을 경우. 다음 head는 tail이다.
                if board[nrow][ncol] == 4:
                    new_head = (nrow, ncol)
                    break
        for i in range(4):
            nrow, ncol = tail[0] + dx[i], tail[1] + dy[i]
            if is_in(nrow, ncol):
                if board[nrow][ncol] == 2:
                    new_tail = (nrow, ncol)
                    break

        board[tail[0]][tail[1]] = 4
        board[head[0]][head[1]] = 2
        if new_head == (-1, -1):  # head - tail 붙음
            # new_head = tail
            new_head = tail
            board[tail[0]][tail[1]] = 1
        else:
            board[new_head[0]][new_head[1]] = 1
            members.remove(tail)
            members.add(new_head)
        board[new_tail[0]][new_tail[1]] = 3

        teams[idx] = {
            'members': members,
            'head': new_head,
            'tail': new_tail
        }
    return


def print_board():
    print('-----------------')
    for row in board:
        print(row)
    print('-----------------')


n, m, k = map(int, input().rstrip().lstrip().split(' '))

board = [list(map(int, input().rstrip().lstrip().split(' ')))
         for _ in range(n)]

teams = get_teams()

round_mod = 4*n

total_score = 0


for current_round in range(1, k+1):
    move_team()
    # print('round start', current_round)
    # print_board()

    direction = current_round % round_mod
    ball_member = get_first_met_position(direction)

    if ball_member == (-1, -1):
        continue

    head_of_team, tail_of_team = get_head_tail(ball_member)
    place_of_member = get_place_of_member_in_team(
        head_of_team, ball_member)
    # print('몇번째 맞았냐?', ball_member, place_of_member)
    for idx, team in enumerate(teams):
        if team['head'] == head_of_team:
            teams[idx]['head'] = tail_of_team
            teams[idx]['tail'] = head_of_team
            break
    total_score += place_of_member ** 2
# print_board()

print(total_score)
