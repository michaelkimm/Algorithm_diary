from collections import deque
import heapq

def solution(jobs):
    answer = 0
    jobs = [[l, s] for s, l in jobs]
    job_q = deque(sorted(jobs, key=lambda x: (x[1], x[0])))
    job_cnt = len(job_q)
    playable_hp = []
    playing = []
    cur_time = 0
    while job_q or playable_hp or playing:
      
        # 플레이 중이면 꺼내고 현재 시간 업데이트
        if playing:
            work_rev, end_time = playing.pop()
            cur_time = end_time
            req2end = end_time - work_rev[1]
            answer += req2end
        else:
            # job_q -> playable
            if job_q:
                work = job_q.popleft()
                heapq.heappush(playable_hp, work)
                cur_time = work[1]
            
        # 현재 시간 기반하여 job_q에서 playable_hp로
        while job_q and (job_q[0][1] <= cur_time):
            work = job_q.popleft()
            heapq.heappush(playable_hp, work) # 작업 시간, 요청 시간
        
        # playable_hp -> playing
        if playable_hp:
            work = heapq.heappop(playable_hp)
            playing.append((work, cur_time + work[0]))
    return answer // job_cnt