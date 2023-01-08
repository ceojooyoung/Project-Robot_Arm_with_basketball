import pygame
import numpy as np
import os

# 게임 윈도우 크기
WINDOW_WIDTH = 1000
WINDOW_HEIGHT =1000

# 색 정의
BLACK = (0, 0, 0)
WHITE = (255, 255, 255) 
GRAY = ((204, 204, 204), (153, 153, 153), (102, 102, 102), (51, 51, 51))
RED = (255, 0, 0)
PINK = ((255, 51, 51), (255, 102, 102), (255, 153, 153), (255, 204, 204))
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def Rmat(deg):
    radian = np.deg2rad(deg)
    c = np.cos(radian)
    s = np.sin(radian)
    R = np.array( [[ c, -s, 0], [s, c, 0], [0, 0, 1] ] )
    return R
def Tmat(a,b):
    H = np.eye(3)
    H[0,2] = a
    H[1,2] = b
    return H
def INIT() :
    global clock
    global screen
    global current_path
    global assets_path
    global font
    pygame.init()
    pygame.display.set_caption("20221557 박주영 Final Project")
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    clock = pygame.time.Clock()
    # assets 경로 설정
    current_path = os.path.dirname(__file__)
    assets_path = os.path.join(current_path, 'assets')
INIT()

done = False
font = pygame.font.SysFont('arial', 30, True, False)
font1 = pygame.font.SysFont('arial', 100, True, False)

# 이미지 로드
ball_img = pygame.image.load(os.path.join(assets_path, "basketball.png"))
background = pygame.image.load(os.path.join(assets_path, "background.jpg"))
body = pygame.image.load(os.path.join(assets_path, "body.png"))

#사운드 로드
bounce_sound = pygame.mixer.Sound(os.path.join(assets_path, "bounce.mp3"))
s1 = pygame.mixer.Sound(os.path.join(assets_path, "s1.mp3"))
s2 = pygame.mixer.Sound(os.path.join(assets_path, "s2.mp3"))
s3 = pygame.mixer.Sound(os.path.join(assets_path, "s3.mp3"))
s4 = pygame.mixer.Sound(os.path.join(assets_path, "s4.mp3"))
goal_sound = pygame.mixer.Sound(os.path.join(assets_path, "goal.mp3"))


class ball :
    def __init__(self, img) -> None:
        self.img = img
        self.x = center[0]
        self.y = center[1]
        self.dx = 0
        self.dy = 0
        self.cor = [self.x, self.y]
        
    def move(self) :
        global caught
        global q
        global goal
        if caught :
            self.x = (q[5][1][0]+q[6][2][0])/2
            self.y = (q[5][1][1]+q[6][2][1])/2
            self. dx = 0
            self. dy = 0
            self.cor = [self.x, self.y]
        else:
            if (685< self.x < 785 and self.y < 300) and self.y+self.dy > 300 : goal = True
            if self.y +self.dy <= WINDOW_HEIGHT-ball_radius : self.y += self.dy
            self.x += self.dx
            self.cor = [self.x, self.y]      
         
    def gravity(self) :
        if self.y < WINDOW_HEIGHT - 2*ball_radius : 
            self.dy += 1
        
    def bounce(self) :
        global ball_radius
        global caught
        if not caught :
            if self.x >= WINDOW_WIDTH - 2*ball_radius :
                if self.dx >=1 : 
                    self.dx -= 1
                    bounce_sound.play()
                self.dx *= -1
            elif self.x <= 2*ball_radius :
                if self.dx <= -1 : 
                    self.dx += 1
                    bounce_sound.play()
                self.dx *= -1
            elif self.y > WINDOW_HEIGHT - 2*ball_radius :
                if self.dy >=1 : 
                    self.dy -= 1
                    bounce_sound.play()
                self.dy *= -1
            
    def draw(self) :
        self.bounce()
        self.move()
        self.gravity()
        screen.blit(self.img, [self.x-ball_radius, self.y-ball_radius])

    def throw(self) :
        global caught
        if caught :
            radian = np.deg2rad(degree[0]+degree[1]+degree[2])
            self.dx = np.cos(radian)*30
            self.dy = np.sin(radian)*30
            
            caught = False

# 농구공 변수 초기화
def ballset() :
    global center
    global ball_radius
    global basketball
    center = np.array([WINDOW_WIDTH//2, WINDOW_HEIGHT//2])
    ball_radius = 50
    basketball = ball(ball_img)

# 폴리곤 초기화
def polyset() :
    global poly
    global poly1
    global cor
    global cor1
    poly = np.array( [[0, 0, 1], [150, 0, 1], [150, 20, 1], [0, 20, 1]])
    poly = poly.T # 3x4 matrix 
    poly1 = np.array( [[0, 0, 1], [60, 0, 1], [60, 14, 1], [0, 14, 1]])
    poly1 = poly1.T # 3x4 matrix
    cor = np.array([10, 10, 1])
    cor1 = np.array([7, 7, 1])

# 게임 변수 초기화
def gameset() :
    global degree
    global moving
    global movingtime
    global caught
    global k
    global H
    global pp
    global corp
    global q
    global catch
    global goal
    global message_time
    message_time = 0
    degree = [0, 0, 0, 90]
    moving = False
    movingtime = 0
    caught = False
    goal = False
    k = [0, 0, 0, 0]
    H=[0 for i in range(7)]
    pp=[0 for i in range(7)]
    corp=[0 for i in range(7)]
    q=[0 for i in range(7)]
    catch=0

def drawgradation(p) :
    for i in range(4) : pygame.draw.polygon(screen, GRAY[3-i], p, 10-2*i)
def drawgradation1(p) :
    for i in range(4) : pygame.draw.polygon(screen, GRAY[3-i], p, 8-2*i)
def drawcircle(pos):
    for i in range(4) : pygame.draw.circle(screen, GRAY[3-i], pos, 20-2*i)
    for i in range(4) : pygame.draw.circle(screen, GRAY[i], pos, 12-2*i)
def drawcircle1(pos):
    for i in range(4) : pygame.draw.circle(screen, GRAY[3-i], pos, 16-2*i)
    for i in range(4) : pygame.draw.circle(screen, GRAY[i], pos, 12-2*i)
def drawlight(pos) :
    pygame.draw.circle(screen, RED, pos, 9)
    for i in range(4) : pygame.draw.circle(screen, PINK[i], pos, 8-2*i)
def UI() :
    screen.blit(font.render("press Z, X to operate bottom motor", True, BLACK), (60, 40))
    screen.blit(font.render("press C, V to operate middle motor", True, BLACK), (60, 70))
    screen.blit(font.render("press <-, -> to operate top motor", True, BLACK), (60, 100))
    screen.blit(font.render("press Space to catch", True, BLACK), (60, 130))

def rotate(H, degree, poly, cor, poly1, cor1, pp, corp, catch) :
    # 회전 반영
    H[0] = Tmat(100, 800) @ Tmat(10, 10) @ Rmat(degree[0]) @ Tmat(-10, -10) 
    pp[0] = H[0] @ poly
    corp[0] = H[0] @ cor

    H[1] = H[0] @ Tmat(150, 0)
    H[1] = H[1] @ Tmat(10, 10) @ Rmat(degree[1]) @ Tmat(-10, -10)
    pp[1] = H[1] @ poly 
    corp[1] = H[1] @ cor

    H[2] = H[1] @ Tmat(150, 0)
    H[2] = H[2] @ Tmat(10, 10) @ Rmat(degree[2]) @ Tmat(-10, -10)
    pp[2] = H[2] @ poly
    corp[2] = H[2] @ cor

    H[3] = H[2] @ Tmat(150, 0)
    H[3] = H[3] @ Tmat(7, 7) @ Rmat(degree[3]+catch) @ Tmat(-7, -7)
    corp[3] = H[3] @ cor1
    pp[3] = H[3] @poly1

    H[4] = H[2] @ Tmat(150, 0)
    H[4] = H[4] @ Tmat(7, 7) @ Rmat(degree[3]+180-catch) @ Tmat(-7, -7)
    corp[4] = H[4] @ cor1
    pp[4] = H[4] @ poly1

    H[5] = H[3] @ Tmat(60, 0)
    H[5] = H[5] @ Tmat(7, 7) @ Rmat(degree[3]+180) @ Tmat(-7, -7)
    corp[5] = H[5] @ cor1
    pp[5] = H[5] @poly1

    H[6] = H[4] @ Tmat(60, 0)
    H[6] = H[6] @ Tmat(7, 7) @ Rmat(degree[3]) @ Tmat(-7, -7)
    corp[6] = H[6] @ cor1
    pp[6] = H[6] @poly1
def drawrobotarm(q, pp, corp) :
    for i in range(7) : q[i] = pp[i][0:2, :].T
    for i in range(7) : drawgradation(q[i])
    for i in range(5) : drawcircle(corp[i][:2])
    for i in range(7) :
        drawcircle1(corp[i][:2])
        drawlight(corp[i][:2])
def catchmotion() :
    global moving
    global movingtime
    global catch
    movingtime -=1
    if movingtime > 20 :
        catch-=2
    elif 1 < movingtime<= 20 :
        catch+=2
    if movingtime <=0 :
        catch=0
        moving = False

def D(pos1, pos2) : return (pos1[0]-pos2[0])**2+(pos1[1]-pos2[1])**2 #점과 점 거리 제곱 반환
def DbLD(pos1, pos2, pos3) : #직선과 점 거리 제곱 반환
    a = pos2[1]-pos1[1]
    b = pos1[0]-pos2[0]
    c = pos1[1]*pos2[0]-pos2[1]*pos1[0]
    return (a*pos3[0]+b*pos3[1]+c)**2/(a**2+b**2)
def IN(L, p, q) : #폴리곤 안에 점이 속하는 지
    a = 0
    b = 0
    c = 0
    d = 0
    if q > (L[1][1]-L[0][1] / L[1][0]-L[0][0] * (p-L[0][0]))+L[0][1] : a = 1
    else : a = -1
    if q > (L[2][1]-L[1][1] / L[2][0]-L[1][0] * (p-L[1][0]))+L[1][1] : b = 1
    else : b = -1
    if q > (L[3][1]-L[2][1] / L[3][0]-L[2][0] * (p-L[2][0]))+L[2][1] : c = 1
    else : c = -1
    if q > (L[0][1]-L[3][1] / L[0][0]-L[3][0] * (p-L[0][0]))+L[0][1] : d = 1
    else : d = -1
    if a*c < 0 and b*d < 0 : return True
    else : return False
def is_caught() :
    global caught
    if DbLD(q[5][1], q[6][2], basketball.cor) < ball_radius**2 :
        print(D(basketball.cor, [(q[5][1][0]+q[6][2][0])/2,(q[5][1][1]+q[6][2][1])/2]))
        if D(basketball.cor, [(q[5][1][0]+q[6][2][0])/2,(q[5][1][1]+q[6][2][1])/2]) <= 3600 : 
            caught = True
            return True
        else :
            caught = False 
            return False

ballset()
polyset()
gameset()

# 게임 반복 구간
while not done:
# 이벤트 반복 구간
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN :
            if event.key==pygame.K_LEFT: 
                k[2] = -2
                s3.play(0, 0, 10)
            elif event.key==pygame.K_RIGHT:
                k[2] = 2
                s3.play(0, 0, 10)
            elif event.key==pygame.K_z:
                k[0] = -2
                s1.play()
            elif event.key==pygame.K_x:
                k[0] = 2
                s1.play()
            elif event.key==pygame.K_c:
                k[1] = -2
                s2.play()
            elif event.key==pygame.K_v:
                k[1] = 2
                s2.play()
            elif event.key==pygame.K_SPACE and not moving:
                movingtime = 40
                moving = True
                if not caught : is_caught()
                else : basketball.throw()
                s4.play()

        elif event.type == pygame.KEYUP :
            if event.key==pygame.K_LEFT: 
                k[2] = 0
            elif event.key==pygame.K_RIGHT:
                k[2] = 0
            elif event.key==pygame.K_z:
                k[0] = 0
            elif event.key==pygame.K_x:
                k[0] = 0
            elif event.key==pygame.K_c:
                k[1] = 0
            elif event.key==pygame.K_v:
                k[1] = 0

    # 키보드 입력을 각도값에 반영
    for i in range(4) : degree[i] += k[i]

    # 잡기 동작 수행하기
    catchmotion()

    # 윈도우 화면 채우기
    screen.fill(WHITE)
    screen.blit(background, [0,0])

    if goal : 
        goal_sound.play()
        message_time = 30
        goal = False
    if message_time :
        message_time -= 1
        screen.blit(font1.render("Goal~~~!", True, BLUE), [center[0]-150, 200])

    # UI 삽입
    UI()
    # 로봇팔 그리기
    screen.blit(body, [0, 650])
    rotate(H, degree, poly, cor, poly1, cor1, pp, corp, catch)
    drawrobotarm(q, pp, corp)
    basketball.draw()
    pygame.display.flip()
    clock.tick(60)

# 게임 종료
pygame.quit()
