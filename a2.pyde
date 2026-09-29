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
        self.blocks = blocks # พิกัด block นับเป็นช่อง (not pixel unit)
        self.color_idx = color_idx
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y
        self.x = anchor_x    # x , y คือ ตำแหน่งปัจจุบันของมุมซ้ายบน (pixel)
        self.y = anchor_y
        self.is_dragging = False
        self.drag_offset_x = 0  # ระยะจากมุมซ้ายบนถึงเมาส์ 
        self.drag_offset_y = 0
        self.mini_cell = 24
    
    def draw(self):
        block_color = PALETTE[self.color_idx]   # สีของ block
        edge_color = (0, 0, 0)         # สีขอบของทุก block ให้เป็นสีดำ

        if self.is_dragging:        # ถ้ากำลังถูกลากอยู่ ใช้ขนาด pixel เท่ากับช่องจริงบนกระดาน (ใหญ่)
            unit = CELL_SIZE        
        else:                       # ถ้ายังวางอยู่ในมือเฉยๆ ใช้ขนาด pixel ย่อส่วน (เล็ก)
            unit = self.mini_cell   

        i = 0
        while i < len(self.blocks):      # วนไล่ทีละ block
            offset = self.blocks[i]      # พิกัดของ block นี้ ( not pixel )
            bx = self.x + offset[0] * unit   # แปลงเป็นตำแหน่ง pixel (แนวนอน)
            by = self.y + offset[1] * unit   # แปลงเป็นตำแหน่ง pixel (แนวตั้ง)

            draw_square(bx, by, unit , block_color, edge_color, 1)  # วาด 1 ช่อง = 1 block
            i += 1                            # เลื่อนไป block ถัดไป
    
    def contains_point(self, px, py):
        # check ขนาดช่องเดียวกับตอน draw() เพื่อให้พื้นที่ตรวจตรงกับที่เห็นบนจอ
        if self.is_dragging:
            unit = CELL_SIZE
        else:
            unit = self.mini_cell

        i = 0
        while i < len(self.blocks):          # วนตรวจทีละ block
            offset = self.blocks[i]
            bx = self.x + offset[0] * unit   # มุมซ้ายบนของ block (pixel)
            by = self.y + offset[1] * unit

            # ถ้าจุด (px, py) อยู่ในพื้นที่สี่เหลี่ยมของ block นี้ = คลิกโดนชิ้นส่วน
            if px >= bx and px < bx + unit and py >= by and py < by + unit:
                return True
            i += 1

        return False                         # ไม่โดน block ไหนเลย
    
    def reset_pos(self):
        # ส่งชิ้นส่วนกลับไปตำแหน่ง anchor ในมือ
        self.x = anchor_x
        self.y = anchor_y
        self.is_dragging = False # อัพเดทให้ไม่ใช่สถานะกำลังลาก

# --- GLOBAL GAME STATE ---
board = None
hand = [0, 0, 0] # เอาไว้เก็บชิ้นส่วนที่อยู่ในมือผู้เล่น สูงสุด 3 ชิ้นพร้อมกัน
score = 0
game_over = False
selected_piece = None  # ชิ้นส่วนที่ผู้เล่นกำลังลากอยู่
selected_index = -1

def spawn_hand():
    global hand
    slot_w = width / 3  # แบ่งความกว้างจอออกเป็น 3 ส่วนเท่าๆ กัน สำหรับ 3 slot
    slot_x = 0           # เริ่มขอบซ้ายสุดของจอ แล้วบวกสะสมทีละ slot
    mini_cell = 24       # ขนาดช่องของชิ้นส่วนตอนอยู่ในมือ

    i = 0
    while i < len(hand):                 # วนสร้างชิ้นส่วนใหม่ให้ครบทุกช่องใน hand
        pick = random.choice(SHAPE_TEMPLATES)   # สุ่ม 1 รูปทรงจากลิสต์ SHAPE_TEMPLATES
        shape = pick[0]                  # ดึงรูปทรง (blocks) ออกมา
        hue = pick[1]                    # hue = เฉดสี ดึง color_idx ออกมา

        # หาความกว้างจริงของชิ้นส่วนนี้ 
        max_col = 0                     # เก็บค่าคอลัมน์ที่อยู่ขวาสุดของรูปทรงนี้ เริ่มที่ 0
        j = 0
        while j < len(shape):           # วนดูทุกบล็อกในรูปทรง
            if shape[j][0] > max_col:                                                      
                max_col = shape[j][0]   # อัปเดตค่าคอลัมน์ขวาสุดใหม่
            j += 1
        piece_width = (max_col + 1) * mini_cell   # แปลงเป็นความกว้าง pixel ของชิ้นส่วนนี้

        new_x = slot_x + (slot_w / 2) - (piece_width / 2)   # ลบครึ่งความกว้างจริง
        new_y = 490                          # ตำแหน่ง y ตายตัว วางแถวเดียวกันทุกชิ้น

        hand[i] = Piece(shape, hue, new_x, new_y)   # สร้าง Piece ใหม่ เก็บลงช่องที่ i ของ hand

        slot_x += slot_w                 # เลื่อนไปเตรียมตำแหน่ง slot ถัดไป
        i += 1                           # เลื่อนไปช่องถัดไปของ hand
def is_hand_empty():
    pass
def check_game_over():
    global game_over

def setup():
    global board, score, game_over
    size(500,600)

    board = Board(GRID_SIZE, CELL_SIZE, BOARD_X, BOARD_Y)

    score = 0
    game_over = False

    spawn_hand()
 


def draw():
    background(100, 100, 100)
    board.draw()

    slot = 0      # วาดชิ้นส่วนในมือแต่ละ slot 3 ช่อง
    while slot < len(hand):
        if hand[slot] != 0:      # ข้ามช่องที่ว่าง (ค่า 0)
            hand[slot].draw()
        slot += 1

    # Draw selected piece on top
    if selected_piece != None:
        pass
    # When Game over
    if game_over :
        pass

def mousePressed():
    global selected_piece, selected_index, game_over
    
    # ถ้าแพ้แล้ว คลิกเพื่อเริ่มเกมใหม่
    if game_over:
        setup()
        return

    # หาชิ้นส่วนที่เมาส์คลิกโดน
    i = 0
    while i < len(hand):
        piece = hand[i]
        # ถ้าเจอให้เตรียมพร้อมสำหรับการลาก
        if piece != 0 and piece.contains_point(mouseX, mouseY):
            selected_piece = piece
            selected_index = i

            # ระยะจากมุมซ้ายบนของชิ้นส่วน(ขนาดเล็กในมือ) ถึงเมาส์
            # คูณสเกลเป็นขนาดใหญ่ เพราะตอนลากชิ้นส่วนจะขยายเป็น 2 เท่า
            scale = CELL_SIZE / piece.mini_cell   
            piece.drag_offset_x = (mouseX - piece.x) * scale
            piece.drag_offset_y = (mouseY - piece.y) * scale

            # เริ่มสถานะลาก และขยับตำแหน่งทันทีให้เมาส์อยู่บน block เดิม
            piece.is_dragging = True
            piece.x = mouseX - piece.drag_offset_x
            piece.y = mouseY - piece.drag_offset_y
            return          
        i += 1

def mouseDragged():
        if selected_piece != None : # มีการลากชิ้นส่วนเกิดขึ้น
            # คำนวณตำแหน่งมุมซ้ายบนใหม่ของชิ้นส่วนตามเมาส์ โดยรักษาระยะ offset ที่คำนวณไว้ตอนคลิก
            selected_piece.x = mouseX - selected_piece.drag_offset_x 
            selected_piece.y = mouseY - selected_piece.drag_offset_y

def mouseReleased():
    pass
    global selected_piece, selected_index, score, game_over
    if selected_piece == None:
        pass
    if board.can_place(selected_piece, target_r, target_c):
        pass


draw = draw
run()