# start time: 16:40
# end time: 18:52

from collections import deque
import sys

input = sys.stdin.readline

def rotate_clock_90(ice_map, length, r, c):
	new_ice_map = [[-1]*length for _ in range(length)]

	for i in range(length):
		for j in range(length):
			ni = j
			nj = length - i - 1
			new_ice_map[ni][nj] = ice_map[r+i][c+j]

	for i in range(length):
		for j in range(length):
			ice_map[r+i][c+j] = new_ice_map[i][j]

def is_in_map(n,r,c):
	return 0<=r<n and 0<=c<n

def check_neighbor_ice(ice_map,length, r,c):

		neighbors = [(r-1,c),(r+1,c),(r,c-1),(r,c+1)]
		count = 0
		for neighbor in neighbors:
			x,y = neighbor
			if is_in_map(length,x,y) and ice_map[x][y] > 0:
					count+=1
		return True if count >=3 else False

def count_ice_with_bfs(ice_map, visited, n, r, c):
	queue=deque()
	queue.append((r,c))
	visited[r][c]=True
	count = 1

	dx=[0,0,-1,1]
	dy=[1,-1,0,0]

	while queue:
		x,y = queue.popleft()
		for i in range(4):
			nx = x + dx[i]
			ny = y + dy[i]
			if is_in_map(n,nx,ny) and not visited[nx][ny] and ice_map[nx][ny]>0:
				visited[nx][ny]=True
				count+=1
				queue.append((nx,ny))
	return count

def check_biggest_ice(ice_map,n):
	biggest = 0
	visited = [[False]*n for _ in range(n)]

	for r in range(n):
		for c in range(n):
			if not visited[r][c] and ice_map[r][c] != 0:
				count_ice = count_ice_with_bfs(ice_map, visited, n, r, c)
				biggest = biggest if biggest > count_ice else count_ice
	return biggest

def firestorm():
	n,q = map(int, input().split(' '))
	length_of_ice_map=2**n

	ice_map = [list(map(int, input().split(' '))) for _ in range(length_of_ice_map)]

	Ls = list(map(int,input().split(' ')))

	for L in Ls:
		line = 2 ** L # 쪼개진 맵의 한 변의 길이
		for r in range(0, length_of_ice_map, line):
			for c in range(0, length_of_ice_map, line):
					rotate_clock_90(ice_map, line, r, c)

		decrement_ice = deque()
		for r in range(length_of_ice_map):
			for c in range(length_of_ice_map):
				if not check_neighbor_ice(ice_map, length_of_ice_map, r, c):
					decrement_ice.append((r,c))
		
		while decrement_ice:
			r,c = decrement_ice.popleft()
			if ice_map[r][c] != 0:
				ice_map[r][c] -= 1

	sum_of_ice=0
	for r in range(length_of_ice_map):
			for c in range(length_of_ice_map):
				sum_of_ice += ice_map[r][c]
	return sum_of_ice, check_biggest_ice(ice_map, length_of_ice_map)

def main():
	sum_of_ice, ice_block = firestorm()
	print(sum_of_ice)
	print(ice_block)

main()
		
