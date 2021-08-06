import pygame
import random
import sys
SCREEN_WIDTH, SCREEN_HEIGHT = 1880, 1000


class Button:
    """Button class"""

    def __init__(self, left, top, width, height, text_content, algo=None):
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.text = text_content
        self.text_offset = 10
        self.text_size = 12
        self.font = "Comic Sans MS"
        self.bg = "white"
        self.text_color = "black"
        self.algo = algo

    def draw(self, screen):
        button = pygame.Rect(self.left, self.top, self.width, self.height)
        pygame.draw.rect(screen, self.bg, button)
        comic_sans = pygame.font.SysFont(self.font, self.text_size)
        button_text = comic_sans.render(self.text, False, self.text_color)
        screen.blit(button_text, (self.left+self.text_offset, self.top+self.text_offset))


def check_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()


def draw_list(screen, lst, curr=None, buttons=None):
    """Draws the current state of the list and buttons if needed. Highlights the element at curr if wanted"""
    check_quit()
    screen.fill("black")
    if buttons:
        for button in buttons:
            button.draw(screen)
    starting_pos = 100
    bar_width = 10
    colors = ["white", "yellow", "blue", "red", "green", "purple", "orange", "black"]
    for x_offset, y_offset in enumerate(lst):
        bar = pygame.Rect(starting_pos + bar_width * x_offset, 0, bar_width, bar_width * y_offset)
        if x_offset == curr:
            pygame.draw.rect(screen, colors[3], bar)
        else:
            pygame.draw.rect(screen, colors[0], bar)
        pygame.draw.line(screen, colors[-1], (starting_pos + bar_width * x_offset, 0), (starting_pos + bar_width * x_offset,bar_width * y_offset))
    pygame.display.update()


def get_menu_option(buttons):
    """Checks for the position of a mouse click and returns the button if clicked"""
    pos = (-1, -1)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
        elif event.type == pygame.QUIT:
            sys.exit()
    for button in buttons:
        if button.left <= pos[0] <= button.left+button.width and button.top <= pos[1] <= button.top+button.height:
            return button
    return None


def main():
    """Sets parameters and handles the main program loop"""
    MIN, MAX, NUM_ITEMS = 1, 90, 150
    lst = [random.randint(MIN, MAX) for _ in range(NUM_ITEMS)]

    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.font.init()
    pygame.display.set_caption("Sort Visuals")
    draw_list(screen, lst)

    randomize_button = Button(100, 925, 100, 50, "Randomize")
    bubble_button = Button(255, 925, 100, 50, "Bubble Sort", visual_bubble_sort)
    selection_button = Button(410, 925, 100, 50, "Selection Sort", visual_selection_sort)
    insertion_button = Button(565, 925, 100, 50, "Insertion Sort", visual_insertion_sort)
    # stop_button = Button(720, 925, 100, 50, "Stop")
    buttons = [randomize_button, bubble_button, selection_button, insertion_button]

    running = True
    while running:
        draw_list(screen, lst, None, buttons)
        pressed = get_menu_option(buttons)
        if pressed is not None:
            if pressed.algo is not None:
                pressed.algo(screen, lst)
            elif pressed.text == randomize_button.text:
                random.shuffle(lst)
                draw_list(screen, lst)
    pygame.quit()


def buffer(screen, lst, delay, curr=None):
    """Draws the list during sorting and handles timing"""
    draw_list(screen, lst, curr)
    pygame.time.wait(delay)
    pygame.event.pump()


def visual_bubble_sort(screen, lst):
    """Bubble sort with modifications for visuals"""
    DELAY = 2
    size = len(lst)
    for i in range(size):
        for j in range(size-i-1):
            if lst[j] >= lst[j+1]:
                lst[j], lst[j+1] = lst[j+1], lst[j]
            buffer(screen, lst, DELAY, j+1)


def visual_selection_sort(screen, lst):
    """Selection sort with modifications for visuals"""
    DELAY = 25
    for i in range(len(lst)):
        min_idx = i
        buffer(screen, lst, DELAY, i)
        for j in range(i+1, len(lst)):
            if lst[min_idx] > lst[j]:
                min_idx = j
        lst[i], lst[min_idx] = lst[min_idx], lst[i]
        buffer(screen, lst, DELAY, min_idx)


def visual_insertion_sort(screen, lst):
    """Insertion sort with modifications for visuals"""
    DELAY = 25
    for i in range(1, len(lst)):
        key = lst[i]
        j = i-1
        buffer(screen, lst, DELAY, i)
        while j >= 0 and key < lst[j]:
            lst[j + 1] = lst[j]
            j -= 1
        lst[j + 1] = key
        buffer(screen, lst, DELAY, j+1)


if __name__ == '__main__':
    main()
