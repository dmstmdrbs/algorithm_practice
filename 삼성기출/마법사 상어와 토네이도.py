import math


def print_field(field):
	n = len(field)
	for i in range(n):
		print(field[i])

def is_out_of_field(n, r, c):
	return (r >= n or r < 0) or (c >=n or c < 0)

def move_tornado(n, field, tornado, r, c, direction, distance):
	# 토네이도 -> 실제 좌표 보정을 위한 dx, dy
	# tx + dx = x
	# ty + dy = y
	dx = r - 2
	dy = c - 2

	# 현재 위치의 모래가 모두 이동한다.
	sand = field[r][c]
	remain_sand = sand
	
	field[r][c] = 0
	ax,ay=-1,-1
	sand_out_of_field = 0
	for tx in range(5):
		for ty in range(5):
			x = tx + dx
			y = ty + dy
			
			moved_sand_ratio = tornado[tx][ty]
			if moved_sand_ratio=='x' or moved_sand_ratio=='y':
				continue
			if moved_sand_ratio=='a':
				ax=x
				ay=y
				continue
			moved_sand = math.floor(moved_sand_ratio * sand)
			# remain_sand -= moved_sand
			remain_sand -= moved_sand
			if is_out_of_field(n, x, y):
				# 필드 밖
				sand_out_of_field += moved_sand
			else:
				# 필드 안에 
				field[x][y] += moved_sand

	if is_out_of_field(n,ax,ay):
		sand_out_of_field += remain_sand
	else:
		field[ax][ay] += remain_sand
	return sand_out_of_field

def get_center_position(n):
	return (n // 2, n//2)

def solution():
	amount_of_sand = 0
	n=int(input())
	field = [list(map(int, input().split(' '))) for _ in range(n)]
	tornado=[
		[
			[0, 0, 0.02, 0, 0],
			[0, 0.1, 0.07, 0.01, 0],
			[0.05, 'a', 'y', 'x', 0],
			[0, 0.1, 0.07, 0.01, 0],
			[0, 0, 0.02, 0, 0]
		],
		[
			[0, 0, 0, 0, 0],
			[0, 0.01,'x',0.01, 0],
			[0.02,0.07,'y',0.07,0.02],
			[0, 0.1, 'a', 0.1, 0],
			[0, 0, 0.05, 0, 0]
		],
		[
			[0, 0, 0.02, 0, 0],
			[0, 0.01, 0.07, 0.1, 0],
			[0, 'x', 'y', 'a', 0.05],
			[0, 0.01, 0.07, 0.1, 0],
			[0, 0, 0.02, 0, 0]
		],
		[
			[0, 0, 0.05, 0, 0],
			[0, 0.1,'a',0.1, 0],
			[0.02,0.07,'y',0.07,0.02],
			[0, 0.01, 'x', 0.01, 0],
			[0, 0, 0, 0, 0]
		]
	]
	r,c = get_center_position(n)
	
	#		  좌,하,우,상
	dx = [0, 1, 0, -1]
	dy = [-1, 0, 1, 0]

	move_distance = 1
	move_direction = 0
	exit_flag = False
	while True:
		# 한 방향으로 2행을 이동
		for _ in range(2):
			# 한 변에서의 이동
			for _ in range(move_distance):
				if exit_flag:
					break
				r = r + dx[move_direction]
				c = c + dy[move_direction]
				
				if r==0 and c==0:
					exit_flag=True
					
				out_of_field = move_tornado(n, field, tornado[move_direction], r, c, move_direction, move_distance)
				amount_of_sand += out_of_field
	
			if exit_flag:
				break
			move_direction = (move_direction + 1) % 4
		
		if exit_flag:
			break
		# 이동하는 한 변의 길이 추가
		move_distance += 1
		# 방향 전환
	return amount_of_sand


print(solution())