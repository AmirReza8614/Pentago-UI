import pygame, sys

class Board:
    def __init__(self, display, rect, color):
        self._display = display
        self._rect = pygame.Rect(rect)
        self._colors = [color, (255, 255, 255), (0, 0, 0)]
        self._rects = []
        self._on_drag = False
        self._drag_pos = (0, 0)
        self._drag_road = 0
        self._rotate = 0
        self._count_motion = 0

        lrect = self._rect.left
        rrect = self._rect.right
        trect = self._rect.top
        brect = self._rect.bottom
        x = (rrect-lrect)/3
        y = (brect-trect)/3
        listy = ["trect", "trect + y + 1", "trect + (y * 2) + 1"]
        listx = ["lrect", "lrect + x + 1", "lrect + (x * 2) + 1"]

        for commandy in listy:
            for commandx in listx:
                self._rects.append(pygame.Rect(eval(commandx), eval(commandy), x ,y))

        
            

    def show(self, table):
        surf = pygame.Surface((self._rect[2], self._rect[3]))
        surf.fill(self._colors[0])

        rect = surf.get_rect()
        lrect = rect.left
        rrect = rect.right
        trect = rect.top
        brect = rect.bottom
        x = (rrect-lrect)/3
        y = (brect-trect)/3

        pygame.draw.line(surf, self._colors[1], (lrect + x, trect), (lrect + x, brect - 1))
        pygame.draw.line(surf, self._colors[1], (lrect + x * 2, trect), (lrect + x * 2, brect - 1))
        pygame.draw.line(surf, self._colors[1], (lrect, trect + y), (rrect - 1, trect + y))
        pygame.draw.line(surf, self._colors[1], (lrect, trect + y * 2), (rrect - 1, trect + y * 2))


        cenx = (lrect + rrect)/2
        ceny = (trect + brect)/2

        listx = ["cenx - x", "cenx", "cenx + x"]
        listy = ["ceny - y", "ceny", "ceny + y"]

        cirsize = (rrect-lrect)/10
        table = self.__rotate(table)

        for commandx, row in zip(listx, table):
            for commandy, item  in zip(listy, row):
                if item == "white":
                    pygame.draw.circle(surf, (255, 255, 255), (eval(commandx) ,eval(commandy)), cirsize)
                elif item == "black":
                    pygame.draw.circle(surf, (0, 0, 0), (eval(commandx) ,eval(commandy)), cirsize)

        rotSurf = pygame.transform.rotate(surf, self._rotate)
        rotSurf = pygame.transform.scale(rotSurf, (self._rect.width, self._rect.height))

        self._display.blit(rotSurf, self._rect)




    def handle_events(self, event, turn):
        output = None

        if event.type == pygame.MOUSEBUTTONDOWN:
            self._count_motion = 0
            if self.is_tapped(pygame.mouse.get_pos()) != -1:
                self._on_drag = True
                self._drag_pos = pygame.mouse.get_pos()

        elif event.type == pygame.MOUSEMOTION:
            now_pos = pygame.mouse.get_pos()
            start_pos = self._drag_pos
            diff_x = now_pos[0]-start_pos[0]
            diff_y = now_pos[1]-start_pos[1]
            self._count_motion += 1
            if self._on_drag and self.is_tapped(now_pos) != -1 and not turn:
                point = 0
                if start_pos[1] < self._rect.center[1]:
                    point += diff_x
                else:
                    point += -diff_x
                
                if start_pos[0] < self._rect.center[0]:
                    point += -diff_y
                else:
                    point += diff_y

                
                self._drag_road = point

                if point > 180:
                    point = 180
                if -180 > point:
                    point = -180

                self._rotate = -point/2

        elif event.type == pygame.MOUSEBUTTONUP:
            self._on_drag = False
            self._rotate = 0

            if self._drag_road > (self._rect.right - self._rect.left)/2:
                output = "c"

            elif self._drag_road < 0 and -self._drag_road > (self._rect.right - self._rect.left)/2:
                output = "cc"

            elif self._count_motion > 5:
                output = None

            elif self.is_tapped(pygame.mouse.get_pos()) != -1 and turn:
                output = int(self.is_tapped(pygame.mouse.get_pos()))

            self._drag_road = 0
            self._count_motion = 0

        return output



    def is_tapped(self, pos):
        for count, rect in enumerate(self._rects):
            if rect.collidepoint(pos[0], pos[1]):
                return count
        return -1
                



    def __rotate(self, intable):
        outtable = [[0,0,0],[0,0,0],[0,0,0]]
        for count, item in enumerate(intable):
            outtable[0][count] = item[0]
            outtable[1][count] = item[1]
            outtable[2][count] = item[2]
        return outtable








## central class
class pentago:
    def __init__(self, Display):
        self._display = Display

        vr1 = 10
        vr2 = vr1 * 2
        rect1 = (vr1, vr1, (width/2)-vr2,(height/2)-vr2)
        rect2 = ((width/2)+vr1, (height/2)+vr1, (width/2)-vr2,(height/2)-vr2)
        rect3 = ((width/2)+vr1, vr1, (width/2)-vr2,(height/2)-vr2)
        rect4 = (vr1, (height/2)+vr1, (width/2)-vr2,(height/2)-vr2)

        self._Boards = []
        self._Boards.append(Board(self._display, rect1, (97, 97, 97)))
        self._Boards.append(Board(self._display, rect3, (171, 133, 133)))
        self._Boards.append(Board(self._display, rect4, (171, 133, 133)))
        self._Boards.append(Board(self._display, rect2, (97, 97, 97)))
        self._state = 0
        self._turn = True

        re = self._display.get_rect()
        self._restrt_rect = pygame.Rect(re.center[0]-50, re.center[1]+50, int(re.width/8), int(re.width/8))


    def show(self, Table):
        if self._state == 0:
            list1=[]; list2=[]; list3=[]; list4=[]
            for count, item in enumerate(Table):
                if count < 3:
                    list1.append(item[:3])
                    list2.append(item[3:])
                else:
                    list3.append(item[:3])
                    list4.append(item[3:])
    
            for i in range(4):
                self._Boards[i].show(eval('list' + str(i+1)))

        else:
            width = self._display.get_rect().width
            myfont = pygame.font.SysFont('Comic Sans MS', int(width/13))
            text = myfont.render('Winner is ' + str(self._state), False, (0, 0, 0))
            self._display.blit(text, text.get_rect(center = self._display.get_rect().center))
            pygame.draw.rect(self._display, (255,255,255), self._restrt_rect, 0, 15)
            myfont = pygame.font.SysFont('Comic Sans MS', int(width/30))
            text = myfont.render('Restart', False, (0, 0, 0))
            self._display.blit(text, text.get_rect(center = self._restrt_rect.center))



    def handle_event(self, event):
        if self._state == 0:
            x = -4
            y = -4
            for i in range(4):
                z = self._Boards[i].handle_events(event, self._turn)
                if z != -1 and z != None and z != "c" and z != "cc":
                    x = i + 1
                    y = z
                    self._turn = False
                    
                elif z == "c" or z == "cc":
                    self._turn = True
                    return [-6, i+1, z]

            if y != -4:
                if x == 1:
                    y += (y // 3) * 3
                elif x == 2:
                    y += ((y // 3)+1) * 3
                elif x == 3:
                    y += ((y // 3) * 3) + 18
                elif x == 4:
                    y += (((y // 3)+1) * 3) + 18

                return [y]
        else:
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if self._restrt_rect.collidepoint(pos[0], pos[1]):
                    self._state = 0
                    return ["restart"]
        return [None]


    def finish(self, winner):
        self._state = winner
            


    
## Its for test   
class Game:
    def __init__(self):
        self._board = []
        for i in range(6):
            self._board.append(["empty" for j in range(6)])
        self._turn = "white"

    def Get_Board(self):
        return self._board

    def put(self, number):
        if self._board[number//6][number%6] == "empty":
            self._board[number//6][number%6] = self._turn
            if self._turn == "white":
                self._turn = "black"
            else:
                self._turn = "white"
            return True
        else:
            return False
    
    def turn(self, board_number, rotation):
        print(board_number, rotation)

    def is_game_finished(self):
        return 0
        

pygame.init()
pygame.font.init()

width = 800
height = 800
display=pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

game = Game()
pentago = pentago(display)

while True:
    display.fill((45, 45, 45, 0.1))
    pentago.show(game.Get_Board())
    pentago.finish(game.is_game_finished())
    for event in pygame.event.get():
        z = pentago.handle_event(event)

        if z[0] == "restart":
            game = Game()

        elif z[0] == -6:
            game.turn(z[1], z[2])

        elif z[0] != None:
            game.put(z[0])

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    clock.tick(60)
