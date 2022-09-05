# start_time : 21:03
# end_time : 22:06

def is_in_seats(n, x, y):
	return 0<=x<n and 0<=y<n

def check_adj_seats(n, classroom, favorites, x, y):
	dx= [0,0,-1,1]
	dy=[1,-1,0,0]
	
	free_count = 0
	favorite_count = 0

	for i in range(4):
		nx = dx[i] + x
		ny = dy[i] + y
		if is_in_seats(n, nx, ny):
			if classroom[nx][ny] in favorites:
				favorite_count+=1
			if classroom[nx][ny]==0:
				free_count+=1
		
	return free_count, favorite_count

def change_seats(n, classroom, current_student, favorites):
	candidate_seats = []

	max_favorites=-1
	max_free_seats=-1

	for x in range(n):
		for y in range(n):
			if classroom[x][y]!=0:
				continue
			free_count, favorite_count =check_adj_seats(n, classroom, favorites, x, y)
			
			if max_favorites > favorite_count and max_free_seats > free_count:
				continue
			
			max_favorites = favorite_count if favorite_count > max_favorites else max_favorites
			max_free_seats = free_count if free_count > max_free_seats else max_free_seats
			
			candidate_seats.append((favorite_count,free_count, x, y))
	candidate_seats.sort(key=lambda x: (x[0],x[1],-x[2],-x[3]), reverse=True)
	r,c = candidate_seats[0][2],candidate_seats[0][3]
	classroom[r][c]=current_student

def get_review(n,classroom,students):
	sum_of_review = 0
	for x in range(n):
		for y in range(n):
			student = classroom[x][y]
			favorites = students[student]
			_, favorite_count = check_adj_seats(n,classroom,favorites,x,y)
			if favorite_count==1:
				sum_of_review += 1
			elif favorite_count==2:
				sum_of_review+=10
			elif favorite_count==3:
				sum_of_review+=100
			elif favorite_count==4:
				sum_of_review+=1000
	return sum_of_review

def main():
	n = int(input())
	classroom =[[0]*n for _ in range(n)]
	number_of_students = n**2
	students=dict()
	for _ in range(number_of_students):
		inputs = list(map(int, input().split(' ')))
		student_id, favorites = inputs[0], inputs[1:]
		
		students[student_id]=favorites
		change_seats(n, classroom, student_id, favorites)

	answer = get_review(n,classroom, students)
	return answer
print(main())
