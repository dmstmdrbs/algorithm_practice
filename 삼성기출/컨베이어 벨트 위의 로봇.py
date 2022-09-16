from collections import deque

def get_next_index(n, x):
	return x % (2*n)

def move_robots(conveyer, robots, n):
	for index in reversed(range(0, n-1)):
		next_index = index+1
		if conveyer[next_index] > 0 and robots[index] and not robots[next_index]:
			robots[next_index]=True
			conveyer[next_index]-=1
			robots[index]=False
	return

def get_zero_count(conveyer):
	zero_count=0
	for durability in conveyer:
		if durability!=0:
			continue
		zero_count+=1
	return zero_count


def conveyer_belt():
	n,k = map(int, input().split(' '))
	conveyer = deque(list(map(int, input().split(' '))))
	robots=deque([False] * 2*n) # 로봇의 index

	count=0
	while True:
		count+=1
		# step 1.
		poped=conveyer.pop()
		conveyer.appendleft(poped)
		poped=robots.pop()
		robots.appendleft(poped)
		
		robots[n-1] = False

		# step 2.
		move_robots(conveyer, robots, n)

		robots[n-1] = False

		# step 3.
		if conveyer[0] > 0 and not robots[0]:
			robots[0]=True
			conveyer[0] -= 1
		
		# step 4.
		if get_zero_count(conveyer) >= k:
			break

	return count

print(conveyer_belt()) 
