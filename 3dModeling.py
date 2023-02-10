import pygame
import time
import math


#game initialization
pygame.init()
pygame.mixer.init()

#constant values
## Colors
BLACK =(0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
GREY = (98,98,98)

## Environment
WIDTH = 10000
HEIGHT = 10000
DEPTH = 10000

## Screen
FPS = 60


def draw_text_on_screen(text,position=(0,0)):
    font = pygame.font.SysFont(None, 40)
    img = font.render(f"{text}", True, BLACK)
    screen.blit(img, position)

def matrix_multiply(matrix1,matrix2):
    # Check
    if len(matrix1[0]) != len(matrix2):
        print("Matrix multiplication error!")
        return
    Clen = len(matrix2[0]) # column length
    Rlen = len(matrix1)    # row length

    temp = [[0 for i in range(Clen)] for j in range(Rlen)]
    for i in range(0, Rlen):
        for j in range(0,Clen):
            for k in range(0,len(matrix1[0])):
                temp[i][j] += matrix1[i][k] * matrix2[k][j]
    return temp

def matrix_0Add_1Subtract(matrix1,matrix2,option=0): # option 0 is add, 1 is subtract
    a = 1
    if option == 1:
        a = -1
    Clen = len(matrix1[0]) # column length
    Rlen = len(matrix1)    # row length

    temp = [[0 for i in range(Clen)] for j in range(Rlen)]
    for i in range(0, Rlen):
        for j in range(0,Clen):
                temp[i][j] = matrix1[i][j] + a * matrix2[i][j]
    return temp

def rotation_matrix(angle):
    return [
        [math.cos(angle), -math.sin(angle)],
        [math.sin(angle), math.cos(angle)]
    ]

def ThreeD_rotation(coordinate,pitch=0,yaw=0,roll=0):
    x = coordinate[0]
    y = coordinate[1]
    z = coordinate[2]
    
    # Rotate about X-axis
    [[y, z]] = matrix_multiply([[y,z]], rotation_matrix(-pitch))
    # Rotate about Y-axis
    [[z, x]] = matrix_multiply([[z,x]], rotation_matrix(-yaw))
    # Rotate about Z-axis
    [[x, y]] = matrix_multiply([[x,y]], rotation_matrix(-roll))

    return [x,y,z]

## Shapes functions (return vertices and edges lists)
## square matrix:Square(Length)[0] 
## square edges :Square(Length)[1] 
## square faces :Square(Length)[2] 
def Square(length):
    return [[
        [0,0,0],
        [0,length,0],
        [length,0,0],
        [length,length,0],
        [0,0,length],
        [0,length,length],
        [length,0,length],
        [length,length,length]
    ],[
        [0,1],[0,2],[1,3],[0,4],[4,5],[4,6],[6,7],[3,7],[5,7],[2,6],[2,3],[1,5]
    ],[
        [0,2,3,1],[6,4,5,7],[3,1,5,7],[3,2,6,7],[1,0,4,5],[2,0,4,6]
    ]]
## pyramid matrix:Pyramid(Length)[0] 
## pyramid edges :Pyramid(Length)[1] 
## pyramid faces :Pyramid(Length)[2] 
def Pyramid(length):
    return [[
        [0,0,0],
        [length,0,0],
        [0,0,length],
        [length,0,length],
        [length/2,length,length/2]
    ],[
        [0,2],[0,1],[1,3],[2,3],[0,4],[1,4],[2,4],[3,4]
    ],[
        [4,0,1],[4,0,2],[4,2,3],[4,1,3], [1,0,2,3]
    ]]

def Sphere(Radius):
    vertices = []
    for sita in range(0,181,4):
        for theta in range(0,91,4):
            sita = sita/180 * math.pi
            theta = theta/180 * math.pi
            
            z = Radius * math.cos(theta)
            if theta == 0:
                r = Radius
            else:
                r = z / math.tan(theta)
            x = r * math.cos(sita)
            y = math.sqrt(r*r - x*x )
            vertices.append([x, y, 0])
            vertices.append([x, -y, 0])
    return [vertices,["None"],["None"]]


Sphere(10)
## Animations
def Animation(Object,vertices,animations):
    value = vertices
    for animation in animations:
        # Checks for animations
        if animation[0:9] == "Transform": 
            value = Transform(vertices,[Object.position],int(animation[9:len(animation)]))
            vertices = value

        if animation[0:6] == "Rotate":
            if len(animation)>6:
                Center = animation[7:len(animation)-1]
                center = [0,0,0]
                temp = 0
                index1 = 0
                index2 = 0
                for char in Center:
                    if char == ",":
                        center[index1] = int(Center[temp:index2])
                        temp = index2 + 1
                        index1 += 1
                    index2 += 1
                center[index1] = int(Center[temp:len(Center)])
                value = Rotate(vertices,[center],1)
                vertices = value
            else:
                value = Rotate(vertices,[Object.position],1)
                vertices = value

    return value
    
def Rotate(position,center,speed):
    angular_speed =  time * speed/180 * math.pi
    [[x,y,z]] = matrix_0Add_1Subtract(position,center,1)
    
    # Rotate about Y-axis
    [[z, x]] = matrix_multiply([[z,x]], rotation_matrix(angular_speed))
    # Rotate about X-axis
    [[y, z]] = matrix_multiply([[y,z]], rotation_matrix(angular_speed))
    # Rotate about Z-axis
    [[x, y]] = matrix_multiply([[x,y]], rotation_matrix(angular_speed))

    [[x,y,z]] = matrix_0Add_1Subtract([[x,y,z]],center,0)
    return [[x,y,z]]

def Transform(position,center,angle):
    sita = angle/180 * math.pi
    [[x,y,z]] = matrix_0Add_1Subtract(position,center,1)
    # Rotate about Y-axis
    [[z, x]] = matrix_multiply([[z,x]], rotation_matrix(sita))
    # Rotate about X-axis
    [[y, z]] = matrix_multiply([[y,z]], rotation_matrix(sita))
    # Rotate about Z-axis
    [[x, y]] = matrix_multiply([[x,y]], rotation_matrix(sita))
    [[x,y,z]] = matrix_0Add_1Subtract([[x,y,z]],center,0)
    return [[x,y,z]]


def Get_screen_position(Player,Object, vertices, animation):
    # Animation 
    [vertices] = Animation(Object,[vertices],animation)
    Xr0 = vertices[0] - Player.position[0]
    Yr0 = vertices[1] - Player.position[1]
    Zr0 = vertices[2] - Player.position[2]
    if Zr0 == 0:
        Zr0 = 0.001

    
    sita_y = Player.rotation[0]/180*math.pi
    sita_x = Player.rotation[1]/180*math.pi
    # Rotate about Y-axis
    [[Zr, Xr]] = matrix_multiply([[Zr0,Xr0]], rotation_matrix(sita_y))
    # Rotate about X-axis
    [[Yr, Zr]] = matrix_multiply([[Yr0,Zr]], rotation_matrix(sita_x))


    Zr = math.sqrt(abs(Zr)) 

    aspect_ratio = Player.height/Player.width
    Scale = (math.tan(Player.fov/2) * Player.radius)/Zr

    X = Xr * Scale * aspect_ratio
    Y = Yr * Scale

    X = Player.width/2 * (1 + X/WIDTH)
    Y = Player.height/2 * (1 - Y/HEIGHT)

    #Debug
    # if vertice_index == 0:
    #     draw_text_on_screen(f"X={int(Xr)},Y={int(Yr)},Z={int(Zr)}",(500,0))
    #     draw_text_on_screen(f"x={int(Xr0)},y={int(Yr0)},z={int(Zr0)}",(X,Y-100))
    #     draw_text_on_screen(f"X={int(Xr)},Y={int(Yr)},Z={int(Zr)}",(X,Y))
    return [X,Y]

class Player():
    def __init__(self,fov, dimention, radius, position = [5000,5000,0]):
        self.fov = fov/180*math.pi
        self.width = dimention[0]
        self.height = dimention[1]
        self.radius = radius
        self.position = position
        self.rotation = [0,0] #[yaw,pitch]
        # Moving
        self.speed = 10
        self.angular_speed = 1

    def update(self,mouse_movement):             

        # Rotation #
        increment0 = self.rotation[0] + mouse_movement[0] * 0.1 * self.angular_speed
        increment1 = self.rotation[1] + mouse_movement[1] * 0.1 * self.angular_speed

        if increment0 <180 and increment0 >-180:
            self.rotation[0] = increment0
        else:
            self.rotation[0] = -self.rotation[0] + mouse_movement[0] * 0.1 * self.angular_speed
        if increment1 <180 and increment1 >-180:
            self.rotation[1] = increment1
        else:
            self.rotation[1] = -self.rotation[1] + mouse_movement[0] * 0.1 * self.angular_speed

        # Displacement
        pitch = self.rotation[1]/180*math.pi
        yaw = self.rotation[0]/180*math.pi
        forward = ThreeD_rotation([0,0,self.speed],pitch,yaw)
        backward = ThreeD_rotation([0,0,-self.speed],pitch,yaw)
        left = ThreeD_rotation([-self.speed,0,0],pitch,yaw)
        right = ThreeD_rotation([self.speed,0,0],pitch,yaw)
        upward = ThreeD_rotation([0,self.speed,0],pitch,yaw)
        downward = ThreeD_rotation([0,-self.speed,0],pitch,yaw)

        # # Debug
        # draw_text_on_screen(f"forward = {int(forward[0]),int(forward[1]),int(forward[2])}",(0,500))
        # draw_text_on_screen(f"backward = {int(backward[0]),int(backward[1]),int(backward[2])}",(0,550))
        # draw_text_on_screen(f"left = {int(left[0]),int(left[1]),int(left[2])}",(0,600))
        # draw_text_on_screen(f"right = {int(right[0]),int(right[1]),int(right[2])}",(0,650))
        # draw_text_on_screen(f"upward = {int(upward[0]),int(upward[1]),int(upward[2])}",(0,700))
        # draw_text_on_screen(f"downward = {int(downward[0]),int(downward[1]),int(downward[2])}",(0,750))

        if moving_forward:
            [self.position] = matrix_0Add_1Subtract ([self.position],[forward])
        if moving_backward:
            [self.position] = matrix_0Add_1Subtract ([self.position],[backward])
        if moving_left:
            [self.position] = matrix_0Add_1Subtract ([self.position],[left])
        if moving_right:
            [self.position] = matrix_0Add_1Subtract ([self.position],[right])
        if moving_up:
            [self.position] = matrix_0Add_1Subtract ([self.position],[upward])
        if moving_down:
            [self.position] = matrix_0Add_1Subtract ([self.position],[downward])
    
    def Get_Player_Info(self):
        #      [x,y,z]       [x,y]
        return self.position,self.rotation

class Object():
    def __init__(self, initial_position, shape_function, animation = ["None"], color = BLACK, surface_color = GREEN):
        self.position = initial_position
        self.matrix = shape_function[0]
        self.edges = shape_function[1]
        self.faces = shape_function[2]
        self.color = color
        self.face_color = surface_color 
        self.no_of_vertices = len(self.matrix)
        self.animation = animation

    def update(self,player):
        ## Draw vertices
        rects = []
        vertices = [[self.position[0],self.position[1],self.position[2]]] * self.no_of_vertices
        vertices = matrix_0Add_1Subtract(vertices,self.matrix,0)
        for vertice in vertices:
            i = vertices.index(vertice)
            vertices[i] = Get_screen_position(player,self, vertices[i],self.animation)
            rect1 = pygame.Rect(vertices[i],(1,1))
            rects.append(rect1)
        for rect in rects:    
            pygame.draw.rect(screen, self.color, rect,1)
       

        # ## Draw faces
        # if self.faces != ["None"]:
        #     for face in self.faces:
        #         list = []
        #         for vertice in face:
        #             list.append(vertices[vertice])
        #         pygame.draw.polygon(screen,self.face_color,list)

        ## Draw edges
        if self.edges != ["None"]:
            for edge in self.edges:
                pygame.draw.line(screen, self.color, vertices[edge[0]], vertices[edge[1]])


# Create Elements
Environment = Object((0,0,0), Square(WIDTH))
Player1 = Player(90, (1920,1080), 1000, )
Square1 = Object((5000,5000,1010), Square(100),[])
Pyramid1 = Object((5000,5100,1010), Pyramid(100),[])
Pyramid2 = Object((5000,5000,1010), Pyramid(100),["Transform90",])
Square2 = Object((0,0,0), Square(100))
test_square = Object((0,0,0), Square(0))
Sphere1 = Object((5000,5000,1010), Sphere(50),[])

Objects_list = [
    # Environment,
    Square1,
    # Square2,
    Pyramid1,
    Pyramid2,
    # Sphere1,
    # test_square
]

#InitialSetting
clock = pygame.time.Clock()
screen = pygame.display.set_mode((Player1.width,Player1.height))
font_name = pygame.font.match_font('arial')
    

#movement
moving_left = False
moving_right = False
moving_up = False
moving_down = False
moving_forward = False
moving_backward = False

mouse_position = (0,0)

running = True
# For animation
time = 0 
while running:
    clock.tick(FPS)

    ### Mouse Settings ###
    mouse_movement = (0,0)
    mouse_movement = pygame.mouse.get_rel()
    ## Set cursor to middle
    # pygame.mouse.set_curser()

    #DetectInput
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Movements
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                moving_forward = True
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_s:
                moving_backward = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_e:
                moving_down = True
            if event.key == pygame.K_q:
                moving_up = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                moving_forward = False
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_s:
                moving_backward = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_e:
                moving_down = False
            if event.key == pygame.K_q:
                moving_up = False
        
    screen.fill(WHITE)

    # Elements update
    if (pygame.mouse.get_pressed()[0]):
        Player1.update(mouse_movement)
    else:
        Player1.update((0,0))
    
    for objects in Objects_list:
        objects.update(Player1)

    # #Debug
    # draw_text_on_screen(Player1.rotation,(0,450))
    # draw_text_on_screen(Player1.position)

    time += 1
    pygame.display.update()
    
pygame.quit()