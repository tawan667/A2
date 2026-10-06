
import random

# --- CONFIGURATION ---
GRID_SIZE = 8
CELL_SIZE = 48
BOARD_X = 58
BOARD_Y = 60
SAVE_FILE = "savegame.txt"      # ไฟล์ที่ใช้บันทึกเกม

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


def draw_square(x, y, size, fill_color, stroke_color, corner_weight):
    # ส่วนที่ 1 : สร้างพื้นทึบด้วยเส้นแนวนอนมีความหนาเท่ากับพื้นที่ทั้งหมด
    strokeCap(SQUARE)
    stroke(fill_color[0], fill_color[1], fill_color[2])  # ใส่สี RGB
    strokeWeight(size)
    line(x, y + size / 2, x + size, y + size / 2)

    # ส่วนที่ 2 : เส้นกรอบ
    stroke(stroke_color[0], stroke_color[1], stroke_color[2])
    strokeWeight(corner_weight)
    line(x, y, x + size, y)
    line(x, y + size, x + size, y + size)
    line(x, y, x, y + size)
    line(x + size, y, x + size, y + size)


def draw_outline(x, y, size, color, weight):
    # วาดเฉพาะกรอบสี่เหลี่ยม (ไม่มีสีพื้น) ใช้กับ ghost preview
    strokeCap(SQUARE)
    stroke(color[0], color[1], color[2])
    strokeWeight(weight)
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
        while row_idx < self.size:
            self.grid.append([])  # เพิ่มแถวใหม่ที่ยังว่างเปล่าเข้าไปก่อน
            col_idx = 0
            while col_idx < self.size:
                self.grid[row_idx].append(0)  # เติม 0 เข้าไปในแถวที่ r ทีละ column
                col_idx = col_idx + 1
            row_idx = row_idx + 1

    def draw(self):  # Draw board  ( check from self.grid )
        row_idx = 0
        py = self.oy  # เริ่มวาดตำแหน่งบนสุด

        while row_idx < self.size:
            col_idx = 0
            px = self.ox  # ให้เริ่มวาดที่ตำแหน่งซ้ายสุด เมื่อขึ้นแถวใหม่         
            while col_idx < self.size:
                if self.grid[row_idx][col_idx] == 0:
                    fill_color = (255, 255, 255)  # ช่องว่าง สีพื้นขาว
                else:  # ถ้าไม่ว่างให้ใส่สีตาม PALETTE
                    fill_color = PALETTE[self.grid[row_idx][col_idx] - 1]

                stroke_color = (0, 0, 0)  # สีกรอบเป็นสีดำทุกช่อง เพื่อให้เห็นช่องแบ่ง

                draw_square(px, py, self.cell_size, fill_color, stroke_color, 2)

                px = px + self.cell_size  # เลื่อนตำแหน่งเป็นหน่วย pixel
                col_idx += 1

            py = py + self.cell_size
            row_idx = row_idx + 1

    def can_place(self, piece, target_r, target_c):
        ok = True  # กำหนดให้สามารถวางได้ไว้ก่อน

        # วนตรวจ block ทีละ block ของชิ้นส่วน ว่า block นั้นวางลงกระดานได้ไหม
        i = 0
        while i < len(piece.blocks) and ok:  # หยุดลูปทันทีเมื่อ ok เป็น False
            row = target_r + piece.blocks[i][1]
            col = target_c + piece.blocks[i][0]

            if row < 0 or row >= self.size or col < 0 or col >= self.size:
                ok = False  # ตกขอบเขต
            elif self.grid[row][col] != 0:
                ok = False  # ช่องไม่ว่าง
            i += 1

        return ok

    def place(self, piece, target_r, target_c):
        color_value = piece.color_idx + 1  # คำนวณเลขสีสำหรับเขียนลงกระดาน
        i = 0
        while i < len(piece.blocks):
            row = target_r + piece.blocks[i][1]  # แถวจริงบนกระดาน
            col = target_c + piece.blocks[i][0]  # คอลัมน์จริงบนกระดาน

            # เก็บสีลงในช่องกระดานนั้น
            self.grid[row][col] = color_value
            i += 1

    def clear_lines(self):
        rows_to_clear = []  # ลิสต์เก็บ "เลขแถว" (0-7) เมื่อแถวนั้นเต็มทุกช่อง
        cols_to_clear = []  # ลิสต์เก็บ "เลขคอลัมน์" (0-7) เมื่อคอลัมน์นั้นเต็มทุกช่อง

        # Check full rows: นับจำนวนช่องที่มี block ในแต่ละแถว
        r = 0
        while r < self.size:
            filled = 0  # ตัวนับช่องที่ไม่ว่าง
            c = 0
            while c < self.size:
                if self.grid[r][c] != 0:
                    filled += 1
                c += 1
            if filled == self.size:  # นับได้ครบทั้งแถว = แถวเต็ม
                rows_to_clear.append(r)
            r += 1

        # Check full columns: นับแบบเดียวกันตามแนวตั้ง
        c = 0
        while c < self.size:
            filled = 0
            r = 0
            while r < self.size:
                if self.grid[r][c] != 0:
                    filled += 1
                r += 1
            if filled == self.size:
                cols_to_clear.append(c)
            c += 1

        # Clear detected rows: วนตามเลขแถวในลิสต์ แล้วล้างทั้งแถว
        i = 0
        while i < len(rows_to_clear):
            r = rows_to_clear[i]
            c = 0
            while c < self.size:
                self.grid[r][c] = 0
                c += 1
            i += 1

        # Clear detected columns: เหมือนกัน แต่ล้างทั้งคอลัมน์
        i = 0
        while i < len(cols_to_clear):
            c = cols_to_clear[i]
            r = 0
            while r < self.size:
                self.grid[r][c] = 0
                r += 1
            i += 1

        # คะแนน = (แถวที่ล้าง + คอลัมน์ที่ล้าง) x 100
        return (len(rows_to_clear) + len(cols_to_clear)) * 100


class Piece:
    def __init__(self, blocks, color_idx, anchor_x, anchor_y, template_idx=0):
        self.blocks = blocks  # พิกัด block นับเป็นช่อง (not pixel unit)
        self.color_idx = color_idx
        self.template_idx = template_idx  # index ของรูปทรงใน SHAPE_TEMPLATES (ใช้ตอน save)
        self.anchor_x = anchor_x
        self.anchor_y = anchor_y
        self.x = anchor_x  # x , y คือ ตำแหน่งปัจจุบันของมุมซ้ายบน (pixel)
        self.y = anchor_y
        self.is_dragging = False
        self.drag_offset_x = 0  # ระยะจากมุมซ้ายบนถึงเมาส์
        self.drag_offset_y = 0
        self.mini_cell = 24

    def draw(self):
        block_color = PALETTE[self.color_idx]  # สีของ block
        edge_color = (0, 0, 0)  # สีขอบของทุก block ให้เป็นสีดำ

        if self.is_dragging:  # ถ้ากำลังถูกลากอยู่ ใช้ขนาด pixel เท่ากับช่องจริงบนกระดาน (ใหญ่)
            unit = CELL_SIZE
        else:  # ถ้ายังวางอยู่ในมือเฉยๆ ใช้ขนาด pixel ย่อส่วน (เล็ก)
            unit = self.mini_cell

        i = 0
        while i < len(self.blocks):  # วนไล่ทีละ block
            offset = self.blocks[i]  # พิกัดของ block นี้ ( not pixel )
            bx = self.x + offset[0] * unit  # แปลงเป็นตำแหน่ง pixel (แนวนอน)
            by = self.y + offset[1] * unit  # แปลงเป็นตำแหน่ง pixel (แนวตั้ง)

            draw_square(bx, by, unit, block_color, edge_color, 1)  # วาด 1 ช่อง = 1 block
            i += 1

    def contains_point(self, px, py):
        # ใช้ขนาดช่องเดียวกับตอน draw() เพื่อให้พื้นที่ตรวจตรงกับที่เห็นบนจอ
        if self.is_dragging:
            unit = CELL_SIZE
        else:
            unit = self.mini_cell

        i = 0
        while i < len(self.blocks):  # วนตรวจทีละ block
            offset = self.blocks[i]
            bx = self.x + offset[0] * unit  # มุมซ้ายบนของ block (pixel)
            by = self.y + offset[1] * unit

            # ถ้าจุด (px, py) อยู่ในพื้นที่สี่เหลี่ยมของ block นี้ = คลิกโดนชิ้นส่วน
            if px >= bx and px < bx + unit and py >= by and py < by + unit:
                return True
            i += 1

        return False  # ไม่โดน block ไหนเลย

    def reset_pos(self):
        # ส่งชิ้นส่วนกลับไปตำแหน่ง anchor ในมือ
        self.x = self.anchor_x
        self.y = self.anchor_y
        self.is_dragging = False


# --- GLOBAL GAME STATE ---
board = None
hand = [0, 0, 0]  # ชิ้นส่วนในมือผู้เล่น สูงสุด 3 ชิ้นพร้อมกัน
score = 0
combo_streak = 0         # จำนวนครั้งที่ล้างแถว/คอลัมน์ติดต่อกัน
game_over = False
selected_piece = None    # ชิ้นส่วนที่ผู้เล่นกำลังลากอยู่
selected_index = -1      # ช่องใน hand ของชิ้นที่ลาก (-1 = ยังไม่ได้เลือก)

status_notice = ""       # ข้อความแจ้งผล save/load
status_timer = 0         # นับถอยหลังเวลาแจ้งผลข้อความเป็นจำนวนเฟรม ถึง 0 แล้วข้อความหาย
clear_msg = ""           # ข้อความ CLEAR +N ที่แสดงมุมขวาบน
clear_timer = 0          # นับถอยหลังการแสดงข้อความ เป็นจำนวนเฟรม

def make_piece(template_idx, color_idx, slot):
    # สร้างชิ้นส่วนจากรูปทรง + สี และคำนวณตำแหน่งบ้านตามช่อง slot (0-2) ในมือ
    slot_w = width / 3.0
    shape = SHAPE_TEMPLATES[template_idx][0]

    # หาความกว้างจริงของชิ้นส่วน
    max_col = 0
    j = 0
    while j < len(shape):
        if shape[j][0] > max_col:
            max_col = shape[j][0]
        j += 1
    piece_width = (max_col + 1) * 24

    new_x = slot * slot_w + (slot_w / 2) - (piece_width / 2)
    new_y = 490
    return Piece(shape, color_idx, new_x, new_y, template_idx)


def spawn_hand():
    global hand
    i = 0
    while i < len(hand):  # สุ่มชิ้นส่วนใหม่ให้ครบทุกช่องใน hand
        t_idx = random.randint(0, len(SHAPE_TEMPLATES) - 1)
        hand[i] = make_piece(t_idx, SHAPE_TEMPLATES[t_idx][1], i)
        i += 1


def is_hand_empty():  # check ว่าในมือยังว่างไหม
    i = 0
    while i < len(hand):
        if hand[i] != 0:
            return False
        i += 1
    return True


def check_game_over():
    global game_over

    # รวบรวมชิ้นส่วนในมือที่ "รูปทรงไม่ซ้ำกัน"
    unique_pieces = []
    i = 0
    while i < len(hand):
        piece = hand[i]
        if piece != 0:  # ข้ามช่องที่ใช้ไปแล้ว
            is_duplicate = False
            j = 0
            while j < len(unique_pieces):
                if unique_pieces[j].blocks == piece.blocks:
                    is_duplicate = True
                j += 1
            if is_duplicate == False:
                unique_pieces.append(piece)
        i += 1

    # ลองวางแต่ละชิ้นที่รวบรวมมาลงทุกช่องของกระดาน
    game_over = True  # สมมติว่าเกมจบไว้ก่อน
    k = 0
    while k < len(unique_pieces) and game_over == True:
        r = 0
        while r < board.size and game_over == True:
            c = 0
            while c < board.size and game_over == True:
                if board.can_place(unique_pieces[k], r, c):
                    game_over = False  # เจอที่วาง แสดงว่าเกมยังไม่จบ
                c += 1
            r += 1
        k += 1
    return game_over


# ---------------- SAVE / LOAD ----------------

def my_split(text, sep):
    # ตัดข้อความตามตัวคั่น sep ที่ต้องการ
    # ข้ามอักขระ [ ] และขึ้นบรรทัดใหม่ เพื่อให้อ่านรูปแบบ [0,0,...] ได้
    parts = []  # ลิสต์ตัวอักษรที่เก็บมา
    current = "" # เก็บตัวอักษรที่อ่านมา
    i = 0
    while i < len(text):
        ch = text[i]  
        if ch == sep:
            parts.append(current)  # เจอตัวคั่น ให้เพิ่มค่าเข้าในลิสต์
            current = ""  # เริ่มเก็บใหม่
        elif ch != "[" and ch != "]" and ch != "\n" and ch != "\r":
            current = current + ch   
        i += 1
    parts.append(current)  # เก็บชิ้นสุดท้าย
    return parts


def save_game():
    global status_notice, status_timer
    try:
        f = open(SAVE_FILE, "w")

        # บรรทัดที่ 1 : กระดานแบบ 2D  [แถว0]/[แถว1]/...
        board_text = ""
        r = 0
        while r < board.size:
            board_text = board_text + "["  # # เปิดวงเล็บ ต้นแถว
            c = 0
            while c < board.size:
                board_text = board_text + str(board.grid[r][c])  # ใส่ค่าของช่องในกระดาน
                if c < board.size - 1:
                    board_text = board_text + ","  # คั่นระหว่างช่อง (ไม่ใส่หลังช่องสุดท้าย)
                c += 1
            board_text = board_text + "]"
            if r < board.size - 1:
                board_text = board_text + "/"  # คั่นระหว่างแถว (ไม่ใส่หลังแถวสุดท้าย)
            r += 1
        f.write(board_text + "\n")  # \n ขึ้นบรรทัดใหม่ตอนเขียนลงไฟล์

        # บรรทัดที่ 2 : คะแนน,streak
        f.write(str(score) + "," + str(combo_streak) + "\n")

        # บรรทัดที่ 3 : ชิ้นส่วนในมือ  รูปทรง:สี;รูปทรง:สี;EMPTY
        hand_text = ""
        i = 0
        while i < len(hand):
            if hand[i] == 0:
                hand_text = hand_text + "EMPTY"
            else:
                hand_text = hand_text + str(hand[i].template_idx) + ":" + str(hand[i].color_idx)
            if i < len(hand) - 1:
                hand_text = hand_text + ";"
            i += 1
        f.write(hand_text + "\n")

        f.close()
        status_notice = "Game Saved!"
    except:
        status_notice = "Save Failed!"
    status_timer = 60


def load_game():
    global score, combo_streak, selected_piece, selected_index, game_over
    global status_notice, status_timer

    # อ่านไฟล์ ถ้าเปิดไม่ได้แปลว่ายังไม่เคย save
    try:
        f = open(SAVE_FILE, "r")
        lines = f.readlines()
        f.close()
    except:
        status_notice = "No Save Found!"
        status_timer = 60
        return

    # แปลงข้อมูลเก็บไว้ในตัวแปรชั่วคราวก่อน ถ้าไฟล์เสียจะไม่กระทบเกมที่กำลังเล่น
    try:
        if len(lines) < 3:
            status_notice = "Corrupt Save!"
            status_timer = 60
            return

        # บรรทัดที่ 1 : กระดาน
        row_texts = my_split(lines[0], "/")
        new_grid = []
        r = 0
        while r < board.size:
            cell_texts = my_split(row_texts[r], ",")
            new_row = []
            c = 0
            while c < board.size:
                new_row.append(int(cell_texts[c]))
                c += 1
            new_grid.append(new_row)
            r += 1

        # บรรทัดที่ 2 : คะแนน,streak
        score_parts = my_split(lines[1], ",")
        new_score = int(score_parts[0])
        new_streak = int(score_parts[1])

        # บรรทัดที่ 3 : ชิ้นส่วนในมือ
        hand_texts = my_split(lines[2], ";")
        new_hand = []
        i = 0
        while i < len(hand):
            if hand_texts[i] == "EMPTY":
                new_hand.append(0)
            else:
                pair = my_split(hand_texts[i], ":")
                new_hand.append(make_piece(int(pair[0]), int(pair[1]), i))
            i += 1
    except:
        status_notice = "Corrupt Save!"
        status_timer = 60
        return

    # ข้อมูลถูกต้องทั้งหมดแล้ว จึงนำมาใช้จริง
    board.grid = new_grid
    score = new_score
    combo_streak = new_streak
    i = 0
    while i < len(hand):
        hand[i] = new_hand[i]
        i += 1

    selected_piece = None
    selected_index = -1
    check_game_over()  # คำนวณสถานะเกมจบใหม่ (ตั้งค่า game_over ให้เอง)

    status_notice = "Game Loaded!"
    status_timer = 60


def keyPressed():
    if key == 's' or key == 'S':
        save_game()
    elif key == 'l' or key == 'L':
        load_game()


# ---------------- MAIN ----------------

def setup():
    global board, score, combo_streak, game_over, status_notice, status_timer
    global clear_msg, clear_timer
    size(500, 600)

    board = Board(GRID_SIZE, CELL_SIZE, BOARD_X, BOARD_Y)

    score = 0
    combo_streak = 0
    game_over = False
    status_notice = ""
    status_timer = 0
    clear_msg = ""
    clear_timer = 0

    spawn_hand()

# ข้อความแถบด้านบน: คะแนน ปุ่มลัด สถานะเกม และ streak
def draw_hud():  
    noStroke()
    fill(255, 255, 255)
    textSize(22)
    text("Score: " + str(score), BOARD_X, 32)

    textSize(12)
    fill(210, 210, 210)
    text("[S] Save  |  [L] Load", BOARD_X, 50)

    textSize(16)
    if game_over:
        fill(255, 90, 90)
        text("Status: YOU LOSE", 290, 32)
    else:
        fill(120, 255, 120)
        text("Status: Playing", 290, 32)

    if combo_streak > 1:
        fill(255, 170, 60)
        text("Streak x" + str(combo_streak), 290, 52)

# ข้อความ CLEAR +N มุมขวาบน 
def draw_clear_msg():
    global clear_timer
    if clear_timer > 0:
        noStroke()
        fill(255, 220, 60)
        textSize(18)
        text(clear_msg, width - 120, 52)
        clear_timer = clear_timer - 1

# กรอบบอกช่องที่ชิ้นส่วนจะลงถ้าปล่อยตอนนี้
def draw_ghost_preview():
    if selected_piece != None:
        cs = board.cell_size
        g_c = int(round((selected_piece.x - board.ox) / float(cs)))
        g_r = int(round((selected_piece.y - board.oy) / float(cs)))

        if board.can_place(selected_piece, g_r, g_c):
            g_color = PALETTE[selected_piece.color_idx]
            i = 0
            while i < len(selected_piece.blocks):
                gx = board.ox + (g_c + selected_piece.blocks[i][0]) * cs
                gy = board.oy + (g_r + selected_piece.blocks[i][1]) * cs
                draw_outline(gx, gy, cs, g_color, 3)
                i += 1

# วาดชิ้นส่วนในมือ ข้ามช่องว่าง และข้ามชิ้นที่กำลังถูกลาก
def draw_hand():
    slot = 0
    while slot < len(hand):
        if hand[slot] != 0 and hand[slot].is_dragging == False:
            hand[slot].draw()
        slot += 1

    if selected_piece != None:
        selected_piece.draw()

# ข้อความแจ้งผล Save / Load
def draw_status_notice():
    global status_timer
    if status_timer > 0:
        noStroke()
        fill(255, 255, 255)
        textSize(16)
        text(status_notice, BOARD_X, 472)
        status_timer = status_timer - 1

# แสดงข้อความกลางจอ  ตอนเกมจบ 
def draw_game_over(): 
    
    if game_over:
        noStroke()

        fill(255, 90, 90)
        textSize(40)
        text("YOU LOSE", width / 2 - 85, 298)

        fill(255, 255, 255)
        textSize(16)
        text("Click to restart", width / 2 - 55, 335)

def draw():
    background(100, 100, 100)

    draw_hud()
    draw_clear_msg()
    board.draw()
    draw_ghost_preview()
    draw_hand()
    draw_status_notice()
    draw_game_over()

def mousePressed():
    global selected_piece, selected_index

    # ถ้าแพ้แล้ว คลิกเพื่อเริ่มเกมใหม่
    if game_over:
        setup()
        return

    # หาชิ้นส่วนที่เมาส์คลิกโดน
    i = 0
    while i < len(hand):
        piece = hand[i]
        if piece != 0 and piece.contains_point(mouseX, mouseY):
            selected_piece = piece
            selected_index = i

            # ระยะจากมุมซ้ายบนของชิ้นส่วน (ขนาดเล็กในมือ) ถึงเมาส์
            # คูณ scale เพราะตอนลากชิ้นส่วนจะขยายเป็น 2 เท่า
            scale = CELL_SIZE / float(piece.mini_cell)
            piece.drag_offset_x = (mouseX - piece.x) * scale
            piece.drag_offset_y = (mouseY - piece.y) * scale

            # เริ่มสถานะลาก และขยับตำแหน่งทันทีให้เมาส์อยู่บน block เดิม
            piece.is_dragging = True
            piece.x = mouseX - piece.drag_offset_x
            piece.y = mouseY - piece.drag_offset_y
            return
        i += 1


def mouseDragged():
    if selected_piece != None:  # มีการลากชิ้นส่วนเกิดขึ้น
        selected_piece.x = mouseX - selected_piece.drag_offset_x
        selected_piece.y = mouseY - selected_piece.drag_offset_y


def mouseReleased():
    global selected_piece, selected_index, score, combo_streak, game_over
    global clear_msg, clear_timer

    # ไม่ได้ถือชิ้นส่วน ให้ออกจากฟังก์ชัน
    if selected_piece == None:
        return

    # แปลงตำแหน่งมุมซ้ายบนของชิ้นส่วน (pixel) เป็นพิกัดช่องบนกระดาน
    col_float = (selected_piece.x - board.ox) / float(board.cell_size)
    row_float = (selected_piece.y - board.oy) / float(board.cell_size)
    target_c = int(round(col_float))
    target_r = int(round(row_float))

    if board.can_place(selected_piece, target_r, target_c):
        board.place(selected_piece, target_r, target_c)

        # คะแนนจากการวาง + คะแนนจากแถว/คอลัมน์ที่ล้างได้
        piece_points = len(selected_piece.blocks) * 10
        line_points = board.clear_lines()

        # combo streak: ล้างได้ติดกันหลายครั้ง ตั้งแต่ครั้งที่ 2 ได้โบนัสครั้งละ 50 x (streak - 1)
        if line_points > 0:
            combo_streak = combo_streak + 1
            combo_bonus = (combo_streak - 1) * 50
            clear_msg = "CLEAR +" + str(line_points)  
            clear_timer = 60
        else:
            combo_streak = 0  # วางแล้วไม่ล้างอะไร streak กลับเป็น 0
            combo_bonus = 0
        
     

        score = score + piece_points + line_points + combo_bonus

        hand[selected_index] = 0  # เอาชิ้นที่ใช้แล้วออกจากมือ

        if is_hand_empty():
            spawn_hand()  # หมดทั้ง 3 ชิ้น สุ่มชุดใหม่
        game_over = check_game_over()
    else:
        selected_piece.reset_pos()  # วางไม่ได้ ส่งกลับที่เดิม

    # เคลียร์การเลือก
    selected_piece = None
    selected_index = -1


draw = draw
