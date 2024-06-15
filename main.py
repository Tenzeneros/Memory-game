import tkinter as tk
import random
from PIL import Image, ImageTk
from tkinter import messagebox


BACKGROUND_COLOR = '#7469B6'
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 680
IMAGE_SIZE = (200, 300)
MARGIN = 10


def load_and_resize_image(filepath, size):
    """Load an image and resize it to fit within the specified size."""
    img = Image.open(filepath)
    img.thumbnail(size, Image.LANCZOS)
    return ImageTk.PhotoImage(img)


window = tk.Tk()
window.title("Memory Game")
window.config(padx=20, pady=20, bg=BACKGROUND_COLOR)
window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")


canvas = tk.Canvas(window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, background='#FFE6E6', highlightthickness=0)
canvas.pack()


images = [load_and_resize_image(f'a{i}.jpg', IMAGE_SIZE) for i in range(1, 6)] * 2
random.shuffle(images)

back_image = Image.open("bgpic.png")
back_image = back_image.resize(IMAGE_SIZE, Image.LANCZOS)
back_image = ImageTk.PhotoImage(back_image)


#Grid
grid_size = (2, 5)
grid = [[None for _ in range(grid_size[1])] for _ in range(grid_size[0])]
card_states = [[False for _ in range(grid_size[1])] for _ in range(grid_size[0])]
revealed_cards = []
pairs_found = 0


index = 0
for i in range(grid_size[0]):
    for j in range(grid_size[1]):
        grid[i][j] = images[index]
        index += 1


def on_card_click(event):
    global revealed_cards

    # Calculate row and column from click position
    col = event.x // (IMAGE_SIZE[0] + MARGIN)
    row = event.y // (IMAGE_SIZE[1] + MARGIN)

    if row < grid_size[0] and col < grid_size[1] and not card_states[row][col]:
        card_states[row][col] = True
        revealed_cards.append((row, col))
        draw_cards()

        
        if len(revealed_cards) == 2:
            window.after(800, check_match)


# Check for a match between two revealed cards
def check_match():
    global revealed_cards, pairs_found

    if len(revealed_cards) == 2:
        (row1, col1), (row2, col2) = revealed_cards
        if grid[row1][col1] == grid[row2][col2]:
            # Match found, leave them revealed
            pairs_found += 1
            revealed_cards = []
            if pairs_found == len(images) // 2:
                messagebox.showinfo(title="Victory", message="You found them all! GOOD JOB!")
        else:
            # No match
            card_states[row1][col1] = False
            card_states[row2][col2] = False
            revealed_cards = []

    draw_cards()


def draw_cards():
    canvas.delete("all")
    for i in range(grid_size[0]):
        for j in range(grid_size[1]):
            x0 = j * (IMAGE_SIZE[0] + MARGIN)
            y0 = i * (IMAGE_SIZE[1] + MARGIN)
            if card_states[i][j]:
                canvas.create_image(x0, y0, anchor="nw", image=grid[i][j])
            else:
                canvas.create_image(x0, y0, anchor="nw", image=back_image)

# event
canvas.bind("<Button-1>", on_card_click)


draw_cards()


window.mainloop()