import pygame, sys
import random
import copy
import time
class Error(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
class Reversi:
    def __init__(self, size = 8):
        if size%2:
            raise Error('棋盤大小要是偶數')
        if size < 6:
            raise Error('棋盤太小了')
        pygame.init()
        pygame.display.set_caption("Reversi")
        screen_info = pygame.display.Info()
        screen_width = screen_info.current_w
        screen_height = screen_info.current_h
        self.screen_height = min(screen_width, screen_height)//3
        self.screen_width = self.screen_height+min(screen_width, screen_height)//6
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.margin = screen_height//144
        self.font = pygame.font.Font('freesansbold.ttf', 24)
        self.data_font = pygame.font.Font('freesansbold.ttf', 36)
        self.block_size = (self.screen_height - 2*self.margin)//size
        self.size = size
    def reset(self, seed=None):
    
        self.board = [[0]*self.size for _ in range(self.size)]
        # Black: 1, White: -1, Nothing: 0
        self.board[self.size//2 - 1][self.size//2 - 1] = 1
        self.board[self.size//2][self.size//2] = 1
        self.board[self.size//2][self.size//2 - 1] = -1
        self.board[self.size//2 - 1][self.size//2] = -1
        self.black_cnt = 2
        self.white_cnt = 2
        self.now_turn = -1
        self.game_over = False
    def flip(self, pos, board = None, player = None):
        actual = not board and not player
        board = board if board else self.board
        player = player if player else self.now_turn
        row, col = pos
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        board[row][col] = player
        if actual:
            self.black_cnt += (self.now_turn==1)
            self.white_cnt += (self.now_turn==-1)
        for d in directions:
            r, c = row + d[0], col + d[1]
            while 0 <= r < self.size and 0 <= c < self.size and board[r][c] == -player:
                r += d[0]
                c += d[1]
            if 0 <= r < self.size and 0 <= c < self.size and board[r][c] == player:
                r, c = row + d[0], col + d[1]
                while board[r][c] == -player:
                    board[r][c] = player
                    if actual:
                        self.black_cnt += self.now_turn
                        self.white_cnt -= self.now_turn
                    r += d[0]
                    c += d[1]
        if not actual:
            return board
    def is_valid_move(self, pos, player = None, board = None):
        player = player if player else self.now_turn
        board = board if board else self.board
        row, col = pos
        if board[row][col] != 0:
            return False
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]
        for d in directions:
            r, c = row + d[0], col + d[1]
            if 0 <= r < self.size and 0 <= c < self.size and board[r][c] == -player:
                r += d[0]
                c += d[1]
                while 0 <= r < self.size and 0 <= c < self.size:
                    if board[r][c] == 0:
                        break
                    if board[r][c] == player:
                        return True
                    r += d[0]
                    c += d[1]
        return False
    def need_pass(self, player = None):
        player = player if player else self.now_turn
        for row in range(self.size):
            for col in range(self.size):
                if self.board[row][col] == 0:
                    if self.is_valid_move((row, col), player):
                        return False
        return True
    def turn_player(self):
        self.now_turn = -self.now_turn
    def step(self, pos):
        pos_i, pos_j = pos
        if pos_i < 0 or pos_j <0 or pos_i >= self.size or pos_j >= self.size:
            return False
        if self.is_valid_move(pos):
            self.flip(pos)
            self.turn_player()
        return True
    def render(self, data = False):
        def pos(self, position):
            i, j = position
            return (self.margin + j * self.block_size + self.block_size//2 + 1, self.margin + i * self.block_size + self.block_size//2 + 1)
        def render_grid(self):
            for i in range(1, self.size):
                pygame.draw.line(self.screen, BLACK, (self.margin + i * self.block_size, self.margin), (self.margin + i * self.block_size, self.screen_height - self.margin), 2)
            for i in range(1, self.size):
                pygame.draw.line(self.screen, BLACK, (self.margin, self.margin + i * self.block_size), (self.screen_height - self.margin, self.margin + i * self.block_size), 2)
        def render_board(self):
            for i in range(self.size):
                for j in range(self.size):
                    if self.board[i][j] == 1:
                        pygame.draw.circle(self.screen, BLACK, pos(self, (i,j)), self.block_size // 2 - 2)
                    elif self.board[i][j] == -1:
                        pygame.draw.circle(self.screen, WHITE, pos(self, (i,j)), self.block_size // 2 - 2)
        def render_cnt(self):
            black_x, black_y = self.margin + self.size * self.block_size + 4 + self.margin * 2, self.screen_height - self.margin*2 - 2*self.block_size - self.block_size//2
            black_cnt_text = self.data_font.render(f'  {self.black_cnt}' , True, BLACK)
            self.screen.blit(black_cnt_text, (black_x + self.block_size + self.margin, black_y + self.block_size//2 - 18))
            pygame.draw.rect(self.screen, BLACK, (black_x-2, black_y-2, self.block_size+4, self.block_size+4), 2)
            pygame.draw.rect(self.screen, GREEN, (black_x, black_y, self.block_size, self.block_size))
            pygame.draw.circle(self.screen, BLACK, (black_x + self.block_size // 2, black_y + self.block_size // 2), self.block_size // 2 - 2)
            
            white_x, white_y = self.margin + self.size * self.block_size + 4 + self.margin * 2, self.screen_height - self.margin - self.block_size - self.block_size//2
            white_cnt_text = self.data_font.render(f'  {self.white_cnt}' , True, WHITE)
            self.screen.blit(white_cnt_text, (white_x + self.block_size + self.margin, white_y + self.block_size//2 - 18))
            pygame.draw.rect(self.screen, BLACK, (white_x-2, white_y-2, self.block_size+4, self.block_size+4), 2)
            pygame.draw.rect(self.screen, GREEN, (white_x, white_y, self.block_size, self.block_size))
            pygame.draw.circle(self.screen, WHITE, (white_x + self.block_size // 2, white_y + self.block_size // 2), self.block_size // 2 - 2)
        def render_data():
            x, y = self.margin + self.size * self.block_size + 4 + self.margin * 2, self.screen_height - self.margin*3 - 2*self.block_size - self.block_size//2 - 36
            if self.game_over:
                if self.black_cnt > self.white_cnt:
                    data_text = self.data_font.render("Black win!!", True, BLACK)
                elif self.white_cnt > self.black_cnt:
                    data_text = self.data_font.render("White win!!", True, WHITE)
                else:
                    data_text = self.data_font.render("Draw..", True, GRAY)
            else:
                data_text = self.data_font.render("can't move", True, BLACK if self.now_turn == 1 else WHITE)
            self.screen.blit(data_text, (x, y))
        BACK_GROUND = (92, 92, 92)
        GRAY = (50, 50, 50)
        WHITE = (255, 255, 255)
        BLACK = (0, 0, 0)
        GREEN = (0, 128, 0)
        
        #background
        self.screen.fill(BACK_GROUND)
        pygame.draw.rect(self.screen, BLACK, (self.margin - 2, self.margin - 2, self.screen_height - 2*self.margin + 4, self.screen_height - 2*self.margin + 4), 2)
        pygame.draw.rect(self.screen, GREEN, (self.margin, self.margin, self.screen_height - 2*self.margin, self.screen_height - 2*self.margin))
        render_grid(self)
        render_board(self)
        
        turn_text = self.font.render('Now Turn' , True, BLACK)
        self.screen.blit(turn_text, (self.margin + self.size * self.block_size + 4 + self.margin, self.margin))
        turn_x, turn_y = self.margin + self.size * self.block_size + 4 + self.margin * 2, self.margin * 2 + 24
        pygame.draw.rect(self.screen, BLACK, (turn_x-2, turn_y-2, self.block_size+4, self.block_size+4), 2)
        pygame.draw.rect(self.screen, GREEN, (turn_x, turn_y, self.block_size, self.block_size))
        pygame.draw.circle(self.screen, BLACK if self.now_turn==1 else WHITE, (turn_x + self.block_size // 2, turn_y + self.block_size // 2), self.block_size // 2 - 2)
        
        render_cnt(self)
        if data:
            render_data()
        pygame.display.flip()
    def dfs(self, board, player, min_, max_, level, level_limit):
        black, white = 1, -1
        if self.need_game_over() or level>=level_limit:
            return [None, self.count(board, black) - self.count(board, white)]
        if self.need_pass(player):
            get = self.dfs(board, -player, min_, max_, level+1, level_limit)
            return [None, max(max_, get[1]) if player==black else min(min_, get[1])]
        pos = [None, None]
        for row in range(self.size):
            for col in range(self.size):
                if not self.is_valid_move((row, col), player):
                    continue
                if min_ <= max_:
                    return [tuple(pos), max_ if player==black else min_]
                get = self.dfs(self.flip((row, col), copy.deepcopy(board), player), -player, min_, max_, level+1, level_limit)
                if player==black and get[1]>max_:
                    pos, max_ = [row, col], get[1]
                if player==white and get[1]<min_:
                    pos, min_ = [row, col], get[1]
        return [tuple(pos), max_ if player==black else min_]
    def count(self, board, player):
        return sum(1 for a in board for b in a if b==player)
    def need_game_over(self):
        return self.need_pass(1) and self.need_pass(-1)
    def close(self):
        pygame.quit()
        sys.exit()
    def run(self):
        self.reset()
        start_time = time.time()
        update_interval = 0.3
        can_update = True
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and can_update:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    col = (mouse_x - self.margin) // self.block_size
                    row = (mouse_y - self.margin) // self.block_size
                    if self.step((row, col)):
                        self.render()
                    if self.need_game_over():
                        self.game_over = True
                    elif self.need_pass():
                        self.render(data=True)
                        start_time = time.time()
                        can_update = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if time.time()-start_time >= update_interval and can_update:
                start_time = time.time()
                self.render()
            if self.game_over and can_update:
                self.render(data=True)
                start_time = time.time()
                can_update = False
            if not can_update and time.time()-start_time >= (5 if self.game_over else 2):
                can_update = True
                if self.game_over:
                    self.reset()
                    start_time = time.time()
                    continue
                self.turn_player()
    def ai(self, player = -1, level_limit = 3):
        self.reset()
        start_time = time.time()
        update_interval = 0.3
        calculate_start_time = time.time()
        calculate_interval = 0.8
        can_update = True
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and can_update and self.now_turn == player:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    col = (mouse_x - self.margin) // self.block_size
                    row = (mouse_y - self.margin) // self.block_size
                    if self.step((row, col)):
                        self.render()
                        calculate_start_time = time.time()
                    if self.need_game_over():
                        self.game_over = True
                    elif self.need_pass():
                        self.render(data=True)
                        start_time = time.time()
                        can_update = False
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if self.now_turn == -player and can_update and time.time() - calculate_start_time >= calculate_interval:
                get = self.dfs(copy.deepcopy(self.board), -player, 1e9, -1e9, 0, level_limit)
                pos = get[0]
                print('AI predict: leading ', get[1] * -player)
                if self.step(pos):
                    self.render()
                if self.need_game_over():
                    self.game_over = True
                elif self.need_pass():
                    self.render(data=True)
                    start_time = time.time()
                    can_update = False
            if time.time()-start_time >= update_interval and can_update:
                start_time = time.time()
                self.render()
            if self.game_over and can_update:
                self.render(data=True)
                start_time = time.time()
                can_update = False
            if not can_update and time.time()-start_time >= (5 if self.game_over else 2):
                can_update = True
                if self.game_over:
                    self.reset()
                    start_time = time.time()
                    calculate_start_time = time.time()
                    continue
                self.turn_player()
            
                
            
if __name__ == '__main__':
    import os
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
    game = Reversi(8)
    game.ai(1, 8)
    