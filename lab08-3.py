import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Paint App")

clock = pygame.time.Clock()
screen.fill((255, 255, 255))

# Түстер мен құралдар
current_color = (0, 0, 0)
tool = "brush"
radius = 5

# UI батырмалар үшін түс тізімі
color_options = [
    ((0, 0, 0), (10, 10, 30, 30)),      # black
    ((255, 0, 0), (50, 10, 30, 30)),    # red
    ((0, 255, 0), (90, 10, 30, 30)),    # green
    ((0, 0, 255), (130, 10, 30, 30))    # blue
]

font = pygame.font.SysFont("Arial", 18)

def draw_ui():
    for color, rect in color_options:
        pygame.draw.rect(screen, color, rect)

    # Актив құралдарды жазу
    screen.blit(font.render(f"Tool: {tool}", True, (0,0,0)), (10, 50))

running = True
drawing = False
start_pos = None

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Құрал таңдау
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                tool = "brush"
            elif event.key == pygame.K_e:
                tool = "eraser"
            elif event.key == pygame.K_r:
                tool = "rect"
            elif event.key == pygame.K_c:
                tool = "circle"

        # Түс таңдау
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            for color, rect in color_options:
                if pygame.Rect(rect).collidepoint(mx, my):
                    current_color = color

            drawing = True
            start_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:
            drawing = False
            end_pos = event.pos

            # Фигураны сызу (бір-ақ рет)
            if tool == "rect":
                x1, y1 = start_pos
                x2, y2 = end_pos
                width = x2 - x1
                height = y2 - y1
                pygame.draw.rect(screen, current_color, (x1, y1, width, height), 2)

            elif tool == "circle":
                x1, y1 = start_pos
                x2, y2 = end_pos
                radius = int(((x2 - x1)**2 + (y2 - y1)**2)**0.5 / 2)
                center = ((x1 + x2) // 2, (y1 + y2) // 2)
                pygame.draw.circle(screen, current_color, center, radius, 2)

    # Brush және eraser – үздіксіз сызу
    if drawing and tool in ["brush", "eraser"]:
        mx, my = pygame.mouse.get_pos()
        color = current_color if tool == "brush" else (255, 255, 255)
        pygame.draw.circle(screen, color, (mx, my), radius)

    # UI отрисовка
    draw_ui()

    pygame.display.flip()
    clock.tick(60)
