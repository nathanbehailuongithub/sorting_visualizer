import pygame
import random
import math
pygame.init()

class DrawInformation:
    BLACK = 0,0,0
    WHITE = 255,255,255
    GREEN = 0,255,0
    RED = 255, 0, 0
    BACKGROUND_COLOR = WHITE
    GRADIENT = [(128,128,128), (160,160,160), (192,192,192)]

    FONT = pygame.font.SysFont('comicsans', 15)
    LARGE_FONT = pygame.font.SysFont('comicsans', 25)

    SIDE_PADDING = 100
    UPPER_PADDING = 150

    def __init__(self, width, height, lst):
        self.width = width
        self.height = height

        self.window = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")

        self.set_list(lst)

    def set_list(self, lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)
        self.bar_width = round((self.width - self.SIDE_PADDING) / len(lst))
        self.bar_height = math.floor((self.height - self.UPPER_PADDING) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PADDING // 2


def generate_starting_list(n, min, max):
    lst = []

    for i in range(n):
        val = random.randint(min, max)
        lst.append(val)

    return lst

def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LARGE_FONT.render(f"{algo_name} - {'Ascending' if ascending else {'Descending'}}", 1, draw_info.GREEN)
    draw_info.window.blit(title, (draw_info.width /2 - title.get_width() /2 , 5)) # places image onto screens 

    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending ", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width /2 - controls.get_width() /2 , 35)) # places image onto screens 

    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort ", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width /2 - sorting.get_width() /2 , 65)) # places image onto screens 

    
    draw_list(draw_info)
    pygame.display.update()

def draw_list(draw_info, color_positions = {}, clear_bg = False):
    lst = draw_info.lst

    if clear_bg:
         clear_rect = (draw_info.SIDE_PADDING // 2, draw_info.UPPER_PADDING, draw_info.width - draw_info.SIDE_PADDING , draw_info.height - draw_info.UPPER_PADDING)
         pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i , val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.bar_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.bar_height

        color = draw_info.GRADIENT[i%3]

        if i in color_positions:
             color = color_positions[i]

        pygame.draw.rect(draw_info.window, color, (x,y, draw_info.bar_width, draw_info.height))
    
    if clear_bg:
         pygame.display.update()

def bubble_sort(draw_info, ascending = True):
    lst = draw_info.lst
    for i in range(len(lst) - 1):
        for j in range(len(lst) - 1 -i):
            num1 = lst[j]
            num2 = lst[ j + 1]

            if (num1 > num2 and ascending) or (num1 < num2  and not ascending):
                lst[j], lst[j+1] = lst[j+1], lst[j]
                draw_list(draw_info, {j: draw_info.GREEN , j+1 :draw_info.RED}, True)
                yield True #generator : pause but store value of yield

    return lst
            
                             

def main():
    run = True
    clock = pygame.time.Clock()
    num_of_blocks = 50
    min_value = 0
    max_value = 100
    lst = generate_starting_list(num_of_blocks, min_value, max_value)
    draw_info = DrawInformation(800, 600, lst)
    sorting = False

    ascending = True
    sorting_algorithm = bubble_sort
    sorting_algorithm_name = "Sorting_algorithm"
    sorting_algorithm_generator = None

    while run:
        clock.tick(60) # FPS
        if sorting:
            try:
                next(sorting_algorithm_generator)
            except StopIteration:
                sorting = False
        else:
             draw(draw_info, sorting_algorithm_name, ascending)
        
    

        draw(draw_info,sorting_algorithm_name, ascending)
        pygame.display.update()

        # clicking exit mode
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type != pygame.KEYDOWN:
                continue
            
            if event.key == pygame.K_r:
                    lst = generate_starting_list(num_of_blocks, min_value, max_value)
                    draw_info.set_list(lst)
                    sorting = False

            elif event.key == pygame.K_SPACE and sorting == False:
                    sorting = True
                    sorting_algorithm_generator = sorting_algorithm(draw_info ,ascending)

            elif event.key == pygame.K_a  and not sorting:
                    ascending = True
            elif event.key == pygame.K_d and not sorting:
                    ascending = False



    pygame.quit()

if __name__ == "__main__": #
    main()