import pygame
import jackbox as sk
import download

auto = False


def closest_color(color, palette):
    r1, g1, b1 = color
    closest_dis = 10000
    cc = 0, 0, 0
    for r2, g2, b2 in palette:
        dis = ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5
        if dis < closest_dis:
            closest_dis = dis
            cc = r2, g2, b2

    return cc


def convert(pic, bg):
    x_max, y_max = pic.get_size()
    pixel = []
    for y in range(y_max):
        pixel.append([])
        for x in range(x_max):
            pixel[y].append(list(pic.get_at((x, y))[:3]))

    for y in range(y_max):
        for x in range(x_max):
            oldpixel = pixel[y][x]
            newpixel = closest_color(pixel[y][x], sk.colors + (sk.bg_colors[bg], ))
            pixel[y][x] = list(newpixel)

            for i in (0, 1, 2):
                quant_error = oldpixel[i] - newpixel[i]

                if x != x_max - 1:
                    pixel[y][x + 1][i] += quant_error * 7 / 16
                if y != y_max - 1 and x:
                    pixel[y + 1][x - 1][i] += quant_error * 3 / 16
                if y != y_max - 1:
                    pixel[y + 1][x][i] += quant_error * 5 / 16
                if y != y_max - 1 and x != x_max - 1:
                    pixel[y + 1][x + 1][i] += quant_error * 1 / 16

    for x in range(x_max):
        for y in range(y_max):
            # print(pixel[y][x])
            pic.set_at((x, y), pixel[y][x] + [255])


def gui(PATH):
    pygame.init()
    image = pygame.image.load(PATH)

    height = 473
    SIZE = int(height * (image.get_width() /image.get_height())), height

    display = pygame.display.set_mode(SIZE)
    content = pygame.Surface(SIZE)

    pygame.display.set_caption("TeeKO Bot")

    scale = auto
    dither = False
    draw = False
    bg = 1

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN or (scale+dither+draw):
                try:
                    event.key
                except AttributeError:
                    event.key = 0

                if event.key == ord('c') or dither:
                    pygame.display.set_caption("Dither...")
                    dither = False
                    convert(image, bg)
                    if auto:
                        draw = True

                elif event.key == ord('s') or scale:
                    image = pygame.image.load(PATH)
                    pygame.display.set_caption("Scale...")
                    scale = False
                    if image.get_width() > image.get_height():
                        width = sk.canvas[1][0] // sk.brush
                        height = int(width * (image.get_height() / image.get_width()))
                    else:
                        height = sk.canvas[1][1] // sk.brush
                        width = int(height * (image.get_width() / image.get_height()))
                    image = pygame.transform.scale(image, (int(width), int(height)))
                    
                    dither = True

                elif event.key == ord('d') or draw:
                    pygame.display.set_caption("Drawing...")
                    draw = False
                    x_max, y_max = image.get_size()
                    pixel = []
                    for y in range(y_max):
                        pixel.append([])
                        for x in range(x_max):
                            pixel[y].append(image.get_at((x, y))[:3])
                    sk.draw(pixel)
                    pygame.display.set_caption("Done")

                elif event.key == ord('q'):
                    running = False

                elif event.key == ord('1'):
                    bg = 0

                elif event.key == ord('2'):
                    bg = 1

                elif event.key == ord('3'):
                    bg = 2

                elif event.key == ord('4'):
                    bg = 3
                
                elif event.key == ord('5'):
                    bg = 4

        content.fill((0, 0, 0))

        content.blit(pygame.transform.scale(image, display.get_size()), (0, 0))

        display.blit(content, (0, 0))
        pygame.display.flip()

    pygame.quit()


def main():
    keyword = input("Word: ")
    path = download.choose(keyword)
    gui(path)
    main()



if __name__ == "__main__":
    print("TeeKO bot by willy")
    main()
