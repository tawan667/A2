from processing import *
import random 

# Draft for function designs
# function design
# --- CONFIGURATION ---
GRID_SIZE = 8
CELL_SIZE = 48
BOARD_X = 58
BOARD_Y = 60

PALETTE = [
    (245, 93, 62),   # Orange-Red
    (66, 133, 244),  # Blue
    (52, 168, 83),   # Green
    (251, 188, 5),   # Yellow
    (171, 71, 188),  # Purple
]

SHAPE_TEMPLATES = [
    # 1x1
    ([(0, 0)], 0),
    # 2x2 Square
    ([(0, 0), (1, 0), (0, 1), (1, 1)], 1),
    # 3x3 Square
    ([(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (0, 2), (1, 2), (2, 2)], 2),
    # เส้นตรงแนวราบ
    ([(0, 0), (1, 0)], 3),
    ([(0, 0), (1, 0), (2, 0)], 4),
    ([(0, 0), (1, 0), (2, 0), (3, 0)], 0),
    # เส้นตรงแนวตั้ง
    ([(0, 0), (0, 1)], 1),
    ([(0, 0), (0, 1), (0, 2)], 2),
    ([(0, 0), (0, 1), (0, 2), (0, 3)], 3),
    # L 
    ([(0, 0), (0, 1), (1, 1)], 4),
    ([(0, 0), (1, 0), (0, 1)], 0),
    ([(0, 0), (1, 0), (1, 1)], 1),
    ([(0, 1), (1, 1), (1, 0)], 2),
]

def draw_square(x,y,size, fill_color, stroke_color, corner_weight):
    # ส่วนที่ 1 : สร้างพื้นทึบด้วยเส้นแนวนอนมีความหนาเท่ากับพื้นที่ทั้งหมด
    strokeCap(SQUARE)
    stroke(fill_color[0],fill_color[1],fill_color[2]) # ใส่สี RGB 
    strokeWeight(size)   
    line(x, y+size/2 , x+size , y+size/2)
    
    # ส่วนที่ 2 : เส้นกรอบ 
    stroke(stroke_color[0],stroke_color[1],stroke_color[2])
    strokeWeight(corner_weight)      # ความหนาไม่เท่ากันบางจุด 
    line(x, y, x + size, y)
    line(x, y + size, x + size, y + size)
    line(x, y, x, y + size)
    line(x + size, y, x + size, y + size)


class Board:
    def __init__(self, size, cell_size, origin_x, origin_y):
        self.size = size
        self.cell_size = cell_size
        self.ox = origin_x
        self.oy = origin_y
        
        self.grid = []  # 2D array เก็บค่าตำแหน่งในตาราง 8*8 
        
        row_idx = 0
        while row_idx < self.size :
            self.grid.append([]) # เพิ่มแถวใหม่ที่ยังว่างเปล่าเข้าไปก่อน
            col_idx = 0
            while col_idx < self.size :
                self.grid[row_idx].append(0) # เติม 0 เข้าไปในแถวที่ r ทีละ column
                col_idx = col_idx + 1
            row_idx = row_idx + 1

    def draw(self): # Draw board  ( check from self.grid )
        row_idx = 0
        py = self.oy # เริ่มวาดตำแหน่งบนสุด
        while row_idx < self.size:
            col_idx = 0
            px = self.ox # ให้เริ่มวาดที่ตำแหน่งซ้ายสุด เมื่อขึ้นแถวใหม่
            while col_idx < self.size:
                if self.grid[row_idx][col_idx] == 0:
                    fill_color = (255, 255, 255)  #ตั้งค่าสีพื้นให้เป็นสีขาว
                    stroke_color = (0, 0, 0)       #ตั้งค่าสีกรอบให้เป็นสีดำ
                else:  # ถ้าไม่ว่างให้ใส่สีอื่นๆ ตาม PALETTE
                    fill_color = PALETTE[self.grid[row_idx][col_idx] - 1]
                    stroke_color = PALETTE[self.grid[row_idx][col_idx] - 1]

                draw_square(px, py, self.cell_size , fill_color, stroke_color, 2)

                px = px + self.cell_size # เลื่อนตำแหน่งเป็นหน่วย pixel
                col_idx += 1

            py = py + self.cell_size
            row_idx = row_idx + 1

                    
    def can_place(self, piece, target_r, target_c):
        pass
    def place(self, piece, target_r, target_c):
        pass
        
    
    def clear_lines(self):
        rows_to_clear = []
        cols_to_clear = []

        # Check full rows
        # Check full columns
        # Clear detected rows
        # Clear detected columns

class Piece:
    def __init__(self, blocks, color_idx, anchor_x, anchor_y):
        self.blocks = blocks
        self.color_idx = color_idx
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y
        self.x = anchor_x
        self.y = anchor_y
        self.is_dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.mini_cell = 24
    
    def draw(self):
        pass
    def contains_point(self, px, py):
        pass
    def reset_pos(self):
        pass

# --- GLOBAL GAME STATE ---
board = None
hand = [0, 0, 0]
score = 0
game_over = False
selected_piece = None
selected_index = -1

def spawn_hand():
    global hand

def is_hand_empty():
    pass
def check_game_over():
    global game_over

def setup():
    global board, score, game_over
    size(500,600)

    board = Board(GRID_SIZE, CELL_SIZE, BOARD_X, BOARD_Y)


def draw():
    background(100, 100, 100)
    board.draw()
    # Draw selected piece on top
    if selected_piece != None:
        pass
    # When Game over
    if game_over :
        pass

def mousePressed():
    global selected_piece, selected_index, game_over

def mouseDragged():
        pass

def mouseReleased():
    pass
    global selected_piece, selected_index, score, game_over
    if selected_piece == None:
        pass
    if board.can_place(selected_piece, target_r, target_c):
        pass


draw = draw
run()