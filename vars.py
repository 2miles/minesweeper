COLS = 20  # number of cols in grid
ROWS = 10  # number of rows in grid
MINES = 5  # number of mines placed

BG_COLOR = (192, 192, 192)

# Dimentions
BOX_SIZE = 32
BORDER = 22
TOP_AREA = BOX_SIZE * 2
grid_w = COLS * BOX_SIZE
grid_h = ROWS * BOX_SIZE
SCREEN_W = grid_w + BORDER * 2  # Display width
SCREEN_H = grid_h + TOP_AREA + BORDER * 3  # Display height
FACE_W = 52

# Locations
GRID_LOC_X = BORDER
GRID_LOC_Y = TOP_AREA + BORDER * 2
TIMER_LOC_X = grid_w - 64
TIMER_LOC_Y = BORDER + 6
MINE_COUNTER_LOC_X = BORDER + 6
MINE_COUNTER_LOC_Y = BORDER + 6
FACE_LOC_X = SCREEN_W / 2 - FACE_W / 2
FACE_LOC_Y = (BORDER + TOP_AREA / 2) - FACE_W / 2
