from util import print_board, our_print_board


class Piece():
    def __init__(self, coord):
        self.coord = coord
        self.neighbours = []

class Cell():
    def __init__(self, piece):
        self.piece = piece
        self.nb_allies = [] # neighbouring allies

class Board():
    def __init__(self, n):
        self.n = n
        self.cells = dict() # since dict lookup costs O(1) by using hash
        self.red_starters = []
        self.blue_starters = []
        self.red_enders = dict()
        self.blue_enders = dict()
        self.round = 0
        # init cells
        for r in range(self.n):
            for q in range(self.n):
                self.cells.update({(r,q):Cell(0)}) 
        # init end cells for both sides
        for i in range(self.n):
            self.red_enders.update({(self.n-1, i):1})
            self.blue_enders.update({(i, self.n-1):1})

    def outside_range(self, coord):
        return coord[0] >= self.n or coord[1] >= self.n or coord[0] < 0 or coord[1] < 0
    
    def endgame_dfs(self, im_red):
        enders = self.red_enders if im_red else self.blue_enders
        frontier = self.red_starters if im_red else self.blue_starters
        checked = dict()
        # push goal states
        while(len(frontier)>0):
            curr = frontier.pop()
            # curr is in the end states
            if enders[curr]:
                return 1 if im_red else -1
            # not in the end states, check if we have seen this node
            if not checked[curr]:
                # push it into the checked dict
                checked.update({curr:1})
                # expand and add to the end of frontier
                for nb in self.cells[curr].nb_allies:
                    frontier.append(nb)
        return -2 # indicate no winner yet, the game goes on

    def check_game_state(self, im_red):
        if self.round == 343:
            return 0 # draw
        return self.endgame_dfs(im_red)

    def remove_piece(self, coord):
        # from it's neighbouring allies's nb allies list, remove itself
        for nb in self.cells[coord].nb_allies:
            if self.outside_range(nb):
                pass
            else:
                self.cells[nb].nb_allies.remove(coord)
        # remove itself from the board
        self.cells[coord].piece=0
        self.cells[coord].nb_allies=[]

    def valid_and_color(self, coord, color):
        if self.outside_range(coord):
            return False

        return self.cells[coord].piece == color

    def check_captures(self, im_red, coord):

        if im_red:
            if self.valid_and_color((coord[0],  coord[1] - 1), 1) and self.valid_and_color((coord[0] + 1,  coord[1] - 1), -1) and self.valid_and_color(( coord[0] - 1,  coord[1]), -1):
               self.remove_piece(( coord[0] + 1,  coord[1] - 1))
               self.remove_piece(( coord[0] - 1,  coord[1]))

            if self.valid_and_color(( coord[0],  coord[1]+1), 1) and self.valid_and_color((  coord[0]+1,  coord[1]), -1) and self.valid_and_color((  coord[0]-1,  coord[1]+1), -1):
            
               self.remove_piece(( coord[0]+1,  coord[1]))
               self.remove_piece(( coord[0] - 1,  coord[1]+1))
            

            if self.valid_and_color(( coord[0]+1,  coord[1]-1), 1) and self.valid_and_color((  coord[0],  coord[1]-1), -1) and self.valid_and_color((  coord[0]+1,  coord[1]), -1):
            
               self.remove_piece(( coord[0],  coord[1]-1))
               self.remove_piece((   coord[0] + 1,  coord[1]))
            

            if self.valid_and_color(( coord[0]-1,  coord[1]+1), 1) and self.valid_and_color((  coord[0]-1,  coord[1]), -1) and self.valid_and_color((  coord[0],  coord[1]+1), -1):
            
               self.remove_piece(( coord[0]-1,  coord[1]))
               self.remove_piece((   coord[0],  coord[1]+1))
            


            if self.valid_and_color(( coord[0]-1,  coord[1]), 1) and self.valid_and_color((  coord[0],  coord[1]-1), -1) and self.valid_and_color((  coord[0]-1,  coord[1]+1), -1):
            
               self.remove_piece(( coord[0],  coord[1]-1))
               self.remove_piece((   coord[0]-1,  coord[1]+1))
            

            if self.valid_and_color(( coord[0]+1,  coord[1]), 1) and self.valid_and_color((  coord[0]+1,  coord[1]-1), -1) and self.valid_and_color((  coord[0],  coord[1]+1), -1):
            
               self.remove_piece(( coord[0]+1,  coord[1]-1))
               self.remove_piece((   coord[0],  coord[1]+1))
            

            # 1.5 dist
            if self.valid_and_color(( coord[0]+2,  coord[1]-1), 1) and self.valid_and_color((  coord[0]+1,  coord[1]-1), -1) and self.valid_and_color((  coord[0]+1,  coord[1]), -1):
            
               self.remove_piece(( coord[0]+1,  coord[1]-1))
               self.remove_piece((   coord[0]+1,  coord[1]))
            
            if self.valid_and_color(( coord[0]-2,  coord[1]+1), 1) and self.valid_and_color((  coord[0]-1,  coord[1]), -1) and self.valid_and_color((  coord[0]-1,  coord[1]+1), -1):
            
               self.remove_piece(( coord[0]-1,  coord[1]))
               self.remove_piece((   coord[0]-1,  coord[1]+1))
            
            if self.valid_and_color(( coord[0]+1,  coord[1]-2), 1) and self.valid_and_color((  coord[0],  coord[1]-1), -1) and self.valid_and_color((  coord[0]+1,  coord[1]-1), -1):
            
               self.remove_piece(( coord[0],  coord[1]-1))
               self.remove_piece((   coord[0]+1,  coord[1]-1))
            
            if self.valid_and_color(( coord[0]-1,  coord[1]+2), 1) and self.valid_and_color((  coord[0]-1,  coord[1]+1), -1) and self.valid_and_color((  coord[0],  coord[1]+1), -1):
            
               self.remove_piece(( coord[0]-1,  coord[1]+1))
               self.remove_piece((   coord[0],  coord[1]+1))
            

            if self.valid_and_color(( coord[0]-1,  coord[1]-1), 1) and self.valid_and_color((  coord[0],  coord[1]-1), -1) and self.valid_and_color((  coord[0]-1,  coord[1]), -1):
            
               self.remove_piece(( coord[0],  coord[1]-1))
               self.remove_piece((   coord[0]-1,  coord[1]))
            
            if self.valid_and_color(( coord[0]+1,  coord[1]+1), 1) and self.valid_and_color((  coord[0]+1,  coord[1]), -1) and self.valid_and_color((  coord[0],  coord[1]+1), -1):
            
               self.remove_piece(( coord[0]+1,  coord[1]))
               self.remove_piece((   coord[0],  coord[1]+1))
            

        else:

            if self.valid_and_color((coord[0],  coord[1] - 1), -1) and self.valid_and_color(( coord[0] + 1,  coord[1] - 1),1) and self.valid_and_color(( coord[0] - 1,  coord[1]),1):
               self.remove_piece(( coord[0] + 1,  coord[1] - 1))
               self.remove_piece((   coord[0] - 1,  coord[1]))
            

            if self.valid_and_color(( coord[0],  coord[1]+1), -1) and self.valid_and_color(( coord[0]+1,  coord[1]),1) and self.valid_and_color(( coord[0]-1,  coord[1]+1),1):
            
               self.remove_piece(( coord[0]+1,  coord[1]))
               self.remove_piece((   coord[0] - 1,  coord[1]+1))
            

            if self.valid_and_color((coord[0]+1,  coord[1]-1), -1) and self.valid_and_color(( coord[0],  coord[1]-1),1) and self.valid_and_color(( coord[0]+1,  coord[1]),1):
            
               self.remove_piece(( coord[0],  coord[1]-1))
               self.remove_piece((   coord[0] + 1,  coord[1]))
            

            if self.valid_and_color(( coord[0]-1,  coord[1]+1), -1) and self.valid_and_color(( coord[0]-1,  coord[1]),1) and self.valid_and_color(( coord[0],  coord[1]+1),1):
            
               self.remove_piece(( coord[0]-1,  coord[1]))
               self.remove_piece((   coord[0],  coord[1]+1))
            


            if self.valid_and_color(( coord[0]-1,  coord[1]), -1) and self.valid_and_color(( coord[0],  coord[1]-1),1) and self.valid_and_color(( coord[0]-1,  coord[1]+1),1):
            
               self.remove_piece(( coord[0],  coord[1]-1))
               self.remove_piece((   coord[0]-1,  coord[1]+1))
            

            if self.valid_and_color(( coord[0]+1,  coord[1]), -1) and self.valid_and_color(( coord[0]+1,  coord[1]-1),1) and self.valid_and_color(( coord[0],  coord[1]+1),1):
            
               self.remove_piece(( coord[0]+1,  coord[1]-1))
               self.remove_piece((   coord[0],  coord[1]+1))
            

            # 1.5 dist
            if self.valid_and_color(( coord[0]+2,  coord[1]-1), -1) and self.valid_and_color(( coord[0]+1,  coord[1]-1),1) and self.valid_and_color(( coord[0]+1,  coord[1]),1):
            
               self.remove_piece(( coord[0]+1,  coord[1]-1))
               self.remove_piece((   coord[0]+1,  coord[1]))
            
            if self.valid_and_color(( coord[0]-2,  coord[1]+1), -1) and self.valid_and_color(( coord[0]-1,  coord[1]),1) and self.valid_and_color(( coord[0]-1,  coord[1]+1),1):
            
               self.remove_piece(( coord[0]-1,  coord[1]))
               self.remove_piece((   coord[0]-1,  coord[1]+1))
            
            if self.valid_and_color((coord[0]+1,  coord[1]-2), -1) and self.valid_and_color(( coord[0],  coord[1]-1),1) and self.valid_and_color(( coord[0]+1,  coord[1]-1),1):
            
               self.remove_piece(( coord[0],  coord[1]-1))
               self.remove_piece((   coord[0]+1,  coord[1]-1))
            
            if self.valid_and_color((coord[0]-1,  coord[1]+2), -1) and self.valid_and_color(( coord[0]-1,  coord[1]+1),1) and self.valid_and_color(( coord[0],  coord[1]+1),1):
            
               self.remove_piece(( coord[0]-1,  coord[1]+1))
               self.remove_piece((   coord[0],  coord[1]+1))
            

            if self.valid_and_color((coord[0]-1,  coord[1]-1), -1) and self.valid_and_color(( coord[0],  coord[1]-1),1) and self.valid_and_color(( coord[0]-1,  coord[1]),1):
            
               self.remove_piece(( coord[0],  coord[1]-1))
               self.remove_piece((   coord[0]-1,  coord[1]))
            
            if self.valid_and_color(( coord[0]+1,  coord[1]+1), -1) and self.valid_and_color((coord[0]+1,  coord[1]),1) and self.valid_and_color((coord[0],  coord[1]+1),1):
            
               self.remove_piece(( coord[0]+1,  coord[1]))
               self.remove_piece((   coord[0],  coord[1]+1))
            
        
    def add_piece(self, im_red, coord):
        r = coord[0]
        q = coord[1]
        self.cells[coord].piece = 1 if im_red else -1
        for c in [(r+1,q-1),(r+1,q),(r,q+1),(r-1,q+1),(r-1,q),(r,q-1)]:
            if self.outside_range(c):
                pass
            elif (im_red and self.cells[c].piece == 1) or ((not im_red) and self.cells[c].piece == -1):
                self.cells[c].nb_allies.append(coord)
                self.cells[coord].nb_allies.append(c)

    def steal(self, target_coord):
        self.round+=1
        self.remove_piece(target_coord)
        self.cells[(target_coord[1],target_coord[0])].piece = -1
        

    def move(self, im_red, coord):
        if self.outside_range(coord) or self.cells[coord].piece != 0:
            print("invalid move!")
            return False
        self.round += 1
        self.add_piece(im_red, coord)
        self.check_captures(im_red, coord)
        game_state = self.check_game_state(im_red)
        if game_state == 1:
            print("Red wins!!")
        elif game_state == -1:
            print("Blue wins!!")
        elif game_state == 0:
            print("Draw, no winner.")
        
        return True


def partb_print_board(board):
    board_dict = dict()
    for coord,cell in board.cells.items():
        if cell.piece == -1:
            board_dict.update({coord:"bB"})
        elif cell.piece == 1:
            board_dict.update({coord:"rR"})
    print_board(board.n, board_dict, "", True)


game = Board(7)
game.move(True, (3,2))
partb_print_board(game)
game.steal((3,2))
partb_print_board(game)
game.move(True, (2,2))
partb_print_board(game)
game.move(False, (1,2))
partb_print_board(game)
game.move(True, (1,3))
partb_print_board(game)
game.move(False, (0,0))
partb_print_board(game)
game.move(True, (6,6))
partb_print_board(game)
