import pygame
import sys
import os


def load_image(name):
    fullname = os.path.join(os.getcwd(), 'img', name)
    if not os.path.isfile(fullname):
        sys.exit()
    image = pygame.image.load(fullname)
    return image


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png')

player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()

tile_width = tile_height = 50
FPS = 50
clock = pygame.time.Clock()

map_file = input('Введите имя файла с картой уровня: ')


def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    fon = pygame.transform.scale(load_image('fon.jpg'), (width, height))
    screen.blit(fon, (0, 0))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return
        pygame.display.flip()
        clock.tick(FPS)


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.speed = tile_width
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.pos_x = 4
        self.pos_y = 4

    def update(self, event, level_map):
        super().update(event)

        if event is not None:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    if level_map[self.pos_x][self.pos_y - 1] != '#':
                        self.rect.y -= tile_height
                        self.pos_y -= 1
                elif event.key == pygame.K_d:
                    if level_map[self.pos_x + 1][self.pos_y] != '#':
                        self.rect.x += tile_width
                        self.pos_x += 1
                elif event.key == pygame.K_s:
                    if level_map[self.pos_x][self.pos_y + 1] != '#':
                        self.rect.y += tile_height
                        self.pos_y += 1
                elif event.key == pygame.K_a:
                    if level_map[self.pos_x - 1][self.pos_y] != '#':
                        self.rect.x -= tile_width
                        self.pos_x -= 1


if __name__ == '__main__':
    pygame.init()
    size = width, height = 600, 600
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Перемещение героя')
    running = True

    level_map = load_level(map_file)
    player, level_x, level_y = generate_level(level_map)
    start_screen()
    while running:
        for event in pygame.event.get():
            player_group.update(event, level_map)
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pass
        screen.fill((0, 0, 0))
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.flip()