from collections import deque
import math

n,m,k = map(int, input().split(' '))
dx=[-1,-1,0,1,1,1,0,-1]
dy=[0,1,1,1,0,-1,-1,-1]
fireballs = [[deque() for _ in range(n+1)] for _ in range(n+1)]

def get_index(n,current, move):
	return (n + current + move) % n
	


def is_direction_even(fireball_queue):
		is_odd=True
		is_even=True
		for fireball in fireball_queue:
			d = fireball['d']
			if d % 2 == 0:
				is_odd=False
			if d% 2==1:
				is_even=False
		if not is_odd and not is_even:
			return False
		return True

def move_fireball(fireballs,n):
	new_fireballs = [[deque() for _ in range(n)] for _ in range(n)]

	for x in range(n):
		for y in range(n):
			if len(fireballs[x][y]) != 0:
				while fireballs[x][y]:
					fireball = fireballs[x][y].popleft()
					m,s,d= fireball['m'],fireball['s'],fireball['d']
					nx = get_index(n, x, dx[d]*s)
					ny = get_index(n, y, dy[d]*s)
					new_fireballs[nx][ny].append(fireball)
	return new_fireballs

def clean_up_fireball(fireballs,n):
	for x in range(n):
		for y in range(n):
			length_of_fireball = len(fireballs[x][y])
			if length_of_fireball>=2:
				# print('파이어볼 합치기',fireballs[x][y])
				sum_m = 0
				sum_s = 0
				for fireball in fireballs[x][y]:
					sum_m += fireball['m']
					sum_s += fireball['s']
				# print('sum_m,s of',x,y,'is',sum_m,sum_s)
				new_m = math.floor(sum_m/5)
				new_s = math.floor(sum_s/length_of_fireball)
				is_even = is_direction_even(fireballs[x][y])
				fireballs[x][y] = deque()

				if new_m == 0:
						continue

				for i in range(4):
					fireballs[x][y].append({'s': new_s,'m': new_m, 'd': (i*2) if is_even else (i*2)+1 })
				# print('new fireballs[x][y]', new_fireballs[x][y])

def after_fireball(fireballs,n):
	sum_m=0

	for x in range(0,n):
		for y in range(n):
			if len(fireballs[x][y]) !=0:
				sub_sum_m=0
				for fireball in fireballs[x][y]:
					sub_sum_m+=fireball['m']
				sum_m+=sub_sum_m
	return sum_m



for _ in range(m):
	r,c,m,s,d = map(int, input().split())
	fireballs[r-1][c-1].append({
		's':s,
		'm':m,
		'd':d,
	})

answer = 0
for i in range(k):
	fireballs = move_fireball(fireballs,n)
	clean_up_fireball(fireballs,n)

answer = after_fireball(fireballs,n)
print(answer)
	