from collections import deque


class Solution(object):
    def solve(self, board):
        """
        :type board: List[List[str]]
        :rtype: None Do not return anything, modify board in-place instead.
        """

        m = len(board)
        n = len(board[0])
        visited = [[False]*n for _ in range(m)]

        dx = [1, -1, 0, 0]
        dy = [0, 0, -1, 1]

        def is_in(row, col):
            return 0 <= row < m and 0 <= col < n

        # 가장자리에 있는 o는 뒤집히면 안된다. => 뒤집히면 아노디는게 있느면 다 뒤집으면 안됨
        def bfs(row, col):
            visited[row][col] = True
            queue = deque()
            queue.append((row, col))
            surrounded = set([(row, col)])

            while queue:
                row, col = queue.popleft()

                for i in range(4):
                    nrow = row + dx[i]
                    ncol = col + dy[i]

                    if is_in(nrow, ncol) and not visited[nrow][ncol] and board[nrow][ncol] == 'O':
                        queue.append((nrow, ncol))
                        visited[nrow][ncol] = True
                        surrounded.add((nrow, ncol))
            return surrounded

        def flip(surrounded):
            for group in surrounded:
                can_flip = True
                for row, col in list(group):
                    if row in [0, m-1] or col in [0, n-1]:
                        can_flip = False
                        break
                if not can_flip:
                    continue
                for row, col in list(group):
                    board[row][col] = 'X'

        to_flip = []
        for row in range(m):
            for col in range(n):
                if not visited[row][col] and board[row][col] == 'O':
                    surrounded = bfs(row, col)
                    to_flip.append(surrounded)
        flip(to_flip)
