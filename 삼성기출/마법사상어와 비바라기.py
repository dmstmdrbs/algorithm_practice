def get_index(n, cur, move):
		return (n + cur + move) % n

dx = [0, 0, -1, -1, -1, 0, 1, 1, 1]
dy = [0, -1, -1, 0, 1, 1, 1, 0, -1]
def move_cloud(n, clouds, direction, distance):

	new_clouds=[]
	for i in range(len(clouds)):
		x,y = clouds[i]
		nx,ny=get_index(n,x,dx[direction]*distance), get_index(n,y,dy[direction]*distance)
		new_clouds.append((nx,ny))
	return new_clouds

def water_copy(game_map, rained, n):
		for cloud in rained:
				r,c = cloud
				water=0
				test = [(r-1,c-1),(r-1,c+1),(r+1,c-1),(r+1,c+1)]
				for test_case in test:
						x,y=test_case
						if 0<=x<n and 0<=y<n and game_map[x][y]>0:
							# 대각선 OK
							water+=1
				game_map[r][c]+=water

def make_cloud(game_map, cloud_map, n):
		new_cloud=[]
		for x in range(n):
			for y in range(n):
				if game_map[x][y] >= 2 and cloud_map[x][y]==False:
					new_cloud.append((x,y))
					game_map[x][y] -= 2
		return new_cloud

n,m = map(int,input().split(' '))

game_map = [list(map(int,input().split(' '))) for _ in range(n)]
clouds = [(n-1,0),(n-1,1),(n-2,0),(n-2,1)]

for tc in range(m):
	d, s = map(int, input().split(' '))
	clouds = move_cloud(n, clouds, d, s)
	cloud_map=[[False]*n for _ in range(n)]

	for cloud_piece in clouds:
		x,y=cloud_piece
		game_map[x][y]+=1
		cloud_map[x][y] = True
	
	water_copy(game_map, clouds, n)
	clouds = make_cloud(game_map, cloud_map, n)
	

answer = 0
for i in range(n):
	answer += sum(game_map[i])
print(answer)