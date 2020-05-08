from PIL import Image
from icrawler.builtin import BingImageCrawler
import pygame
import os


def choose(keyword):
    for num in range(1, 11):
        path = "imgs/" + str(num).zfill(6) + ".jpg"
        try:
            os.remove(path)
        except FileNotFoundError:
            pass

    display = pygame.display.set_mode((640, 480))
    content = pygame.Surface((640, 480))

    pygame.display.set_caption("Choose Image")

    images = []
    download(keyword)
    for num in range(1, 11):
        path = "imgs/" + str(num).zfill(6) + ".jpg"
        images.append(pygame.image.load(path))

    pointer = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if pointer > 0:
                        pointer -= 1
                elif event.key == pygame.K_RIGHT:
                    if pointer < len(images)-1:
                        pointer += 1
                elif event.key == pygame.K_RETURN:
                    running = False

        content.fill((0, 0, 0))

        y = content.get_height()
        x = int(y * (images[pointer].get_width() / images[pointer].get_height()))
        pygame.display.set_mode((x, y))
        content = pygame.Surface((x, y))
        content.blit(pygame.transform.scale(images[pointer], (x, y)), (0, 0))

        display.blit(content, (0, 0))
        pygame.display.flip()

    pygame.quit()

    Image.open("imgs/"+str(pointer+1).zfill(6)+".jpg").save("imgs/img.bmp")

    return "imgs/img.bmp"


def download(keyword):
    fd = dict(color="white",
              size="medium",
              layout="tall")

    bing_crawler = BingImageCrawler(
        parser_threads=5, downloader_threads=5,
        storage={'root_dir': 'imgs'})
    bing_crawler.session.verify = False
    bing_crawler.crawl(keyword=keyword, max_num=10,
                       min_size=(10, 10), max_size=None,
                       filters=fd)
