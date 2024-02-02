# JumpKingMario
점프킹 마리오


## 게임 소개
마리오가 점프를 하며 장애물을 피하는 게임
<br>

## 게임 규칙
‘스페이스 바’를 누르면 마리오가 위로 올라간다.
장애물에 닿거나 아래로 떨어지면 게임이 끝난다.
게임오버가 되면 replay와 continue중 선택이 가능하며, continue는 총 2번의 기회가 주어진다.
장애물을 통과하면 점수가 오른다.
5초마다 게임의 속도가 빨라진다.


## 주요 기능
1. 중력 및 점프 로직
   
    def update(self):  # 마리오 상태 업데이트 메소드
        self.y += self.gravity  # 마리오의 y 좌표에 중력 값을 더해 아래로 이동
        self.gravity += 0.2  # 점프 이후 더 빠르게 떨어지도록 점차적으로 중력을 더함
        if self.jump:  # 점프 중일 경우
            self.gravity = -self.jumpspeed  # 중력 값을 음의 점프 속도로 설정해 위로 이동
            self.jump -= 1  # 점프 상태 감소

2. 파이프 속도 증가
   
    if game_time - last_speed_increase >= 5:  # 마지막 속도 증가 이후 5초가 경과했으면
        current_speed += 0.3  # 파이프의 속도 증가
        last_speed_increase = game_time  # 마지막 속도 증가 시간 업데이트

3. 파이프 통과 시 점수 증가

    if mario.x > pipe.x + pipe.width and not pipe.passed:  # 마리오가 파이프를 지나가면
        pipe.passed = True  # 파이프의 통과 상태를 True로 설정
        score += 1  # 점수 증가
