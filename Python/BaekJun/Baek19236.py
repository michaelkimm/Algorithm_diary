from collections import deque

# x, 북, 북서, 서, 남서, 남, 동남, 동, 북동
di = [0, -1, -1, 0, 1, 1, 1, 0, -1]
dj = [0, 0, -1, -1, -1, 0, 1, 1, 1]

# input
graph = []
for _ in range(4):
    inputLine = list(map(int, input().split()))
    temp = []
    for idx in range(0, 8, 2):
        temp.append((inputLine[idx], inputLine[idx + 1]))
    graph.append(temp)

def eatFish(graph, fishPose, sharkPose=(-1, -1)):
    if sharkPose != (-1, -1):
        graph[sharkPose[0]][sharkPose[1]] = (0, 0)
    fishNum = graph[fishPose[0]][fishPose[1]][0]
    fishDir = graph[fishPose[0]][fishPose[1]][1]
    graph[fishPose[0]][fishPose[1]] = ('s', fishDir)
    sharkPose = fishPose
    sharkDir = fishDir
    return fishNum, sharkPose, sharkDir

def duplicateGraph(graph):
    return [[graph[i][j] for j in range(len(graph[0]))] for i in range(len(graph))]

def isMovable(fi, fj, fishDir, graph):
    global di, dj
    ni = fi + di[fishDir]
    nj = fj + dj[fishDir]
    # 이동 불가능 = 상어가 있거나 경계 넘는 칸
    if not (0 <= ni < 4 and 0 <= nj < 4):
        return False
    if graph[ni][nj][0] == 's':
        return False
    # 이동 가능 = 빈칸(0,0)과 물고기 있는 칸
    return True

def changeSeat(fi, fj, fishNum, fishDir, graph, fishes):
    ni = fi + di[fishDir]
    nj = fj + dj[fishDir]
    temp = graph[ni][nj]
    graph[ni][nj] = (fishNum, fishDir)
    graph[fi][fj] = temp
    fishes[temp[0]] = (temp, fi, fj)

def moveFishes(graph):
    fishes = [(num, -1, -1) for num in range(17)]
    # 물고기 정렬
    for i in range(4):
        for j in range(4):
            if graph[i][j] != (0, 0) and graph[i][j][0] != 's':
                fishNum = graph[i][j][0]
                fishes[fishNum] = (graph[i][j], i, j)

    # 물고기 작은 순서대로 움직이기
    for fishNum in range(1, 17):
        # 물고기가 없는 자리라면 pass
        if fishes[fishNum] == (fishNum, -1, -1):
            continue

        (fishNum, fishDir), fi, fj = fishes[fishNum]
        for rotateCnt in range(8):
            newFishDir = (fishDir + rotateCnt) % 9 if (fishDir + rotateCnt) % 9 != 0 else 1
            if isMovable(fi, fj, newFishDir, graph):
                changeSeat(fi, fj, fishNum, newFishDir, graph, fishes)
                break
    
def getHashableWithList(graph):
    return tuple([tuple([graph[i][j] for j in range(len(graph[0]))]) for i in range(len(graph))])

def bfs(graph):
    # 시작
    eatenFishNumSum, sharkPose, sharkDir = eatFish(graph, fishPose=(0, 0))
    maxEatenFishNumSum = eatenFishNumSum
    newGraph = duplicateGraph(graph)
    q = deque([(newGraph, sharkDir, sharkPose, eatenFishNumSum)])
    visited = set()
    visited.add(getHashableWithList(newGraph))

    while q:
        graph, sharkDir, sharkPose, eatenFishNumSum = q.popleft()

        # 물고기 움직이기
        moveFishes(graph)

        maxEatenFishNumSum = max(maxEatenFishNumSum, eatenFishNumSum)

        # 간선
        # 상어 움직이기
        for dist in range(1, 4):
            ni = sharkPose[0] + dist * di[sharkDir]
            nj = sharkPose[1] + dist * dj[sharkDir]
            if not (0 <= ni < 4 and 0 <= nj < 4) or not (1 <= graph[ni][nj][0] <= 16):
                continue

            newGraph = duplicateGraph(graph)
            tempEatenFishNumSum, newSharkPose, newSharkDir = eatFish(newGraph, (ni, nj), sharkPose)
            newEatenFishNum = eatenFishNumSum + tempEatenFishNumSum
            if getHashableWithList(newGraph) in visited:
                continue
            visited.add(getHashableWithList(newGraph))
            q.append((newGraph, newSharkDir, newSharkPose, newEatenFishNum))
    return maxEatenFishNumSum

print(bfs(graph))