import pygame
from sprites import *
from config import *
import sys
import json


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font('arial.ttf', 32)
        self.character_spritesheet = Spritesheet('img/character.png')
        self.terrain_spritesheet = Spritesheet('img/terrain.png')
        self.enemy_spritesheet = Spritesheet('img/enemy.png')
        self.intro_background = pygame.image.load('img/introbackground.png')
        self.battle_mode = False

    def create_tile_map(self):
        for i, row in enumerate(TILEMAP):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "B":
                    Block(self, j, i)
                if column == "E":
                    Enemy(self, j, i)
                if column == "P":
                    self.player = Player(self, j, i)

    def new(self):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.create_tile_map()

    def events(self):
        # game loop events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
                self.running = False

    def update(self):
        self.all_sprites.update()
        if self.player.battle_mode:
            self.battle_mode = True

    def draw(self):
        self.screen.fill(BLACK)
        self.all_sprites.draw(self.screen)
        self.clock.tick(FPS)
        pygame.display.update()

    def main(self):
        # game loop
        while self.playing:
            if self.battle_mode:
                self.pokemon_battle()
            else:
                self.events()
                self.update()
                self.draw()

        self.running = False

    def game_over(self):
        pass

    def intro_screen(self):
        intro = True

        title = self.font.render('Pokemon', True, BLACK)
        title_rect = title.get_rect(x=10, y=10)

        play_button = Button(10, 50, 100, 50, WHITE, BLACK, 'Play', 32)
        quit_button = Button(10, 110, 100, 50, WHITE, BLACK, 'Quit', 32)
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    intro = False
                    self.running = False
            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if play_button.is_pressed(mouse_pos, mouse_pressed):
                intro = False

            if quit_button.is_pressed(mouse_pos, mouse_pressed):
                pygame.quit()
                sys.exit()

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.screen.blit(quit_button.image, quit_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def pokemon_selection(self):
        selection = True

        title = self.font.render('Starter Selection', True, BLACK)
        title_rect = title.get_rect(x=200, y=10)

        charmander = StarterButton(235, 60, 150, 150, 'img/charmander.png')
        squirtle = StarterButton(120, 240, 150, 150, 'img/squirtle.png')
        bulbasaur = StarterButton(350, 240, 150, 150, 'img/bulbasaur.png')
        self.pokemon_data = json.load(open("pokemon_data.json"))
        while selection:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    selection = False
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if charmander.rect.collidepoint(mouse_pos):
                        for data in self.pokemon_data:
                            if data["name"] == "Charmander":
                                self.player_pokemon = pokemon(data["name"], data["img"], data["health"], data["attack"],
                                                              data["skill1"], data["skill2"], 100, 250)
                                selection = False
                    elif squirtle.rect.collidepoint(mouse_pos):
                        for data in self.pokemon_data:
                            if data["name"] == "Squirtle":
                                self.player_pokemon = pokemon(data["name"], data["img"], data["health"], data["attack"],
                                                              data["skill1"], data["skill2"], 100, 250)
                                selection = False
                    elif bulbasaur.rect.collidepoint(mouse_pos):
                        for data in self.pokemon_data:
                            if data["name"] == "Bulbasaur":
                                self.player_pokemon = pokemon(data["name"], data["img"], data["health"], data["attack"],
                                                              data["skill1"], data["skill2"], 100, 250)
                                selection = False

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(charmander.image, charmander.rect)
            self.screen.blit(squirtle.image, squirtle.rect)
            self.screen.blit(bulbasaur.image, bulbasaur.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def pokemon_battle(self):
        battle = True

        current_health = self.player_pokemon.health
        title = self.font.render('Battle', True, BLACK)
        title_rect = title.get_rect(x=200, y=10)

        p_health = self.font.render('HP: {}/{}'.format(current_health,self.player_pokemon.health), True, BLACK)
        p_health_rect = p_health.get_rect(x=270, y=250)
        p_skill1 = Button(270, 300, 100, 50, WHITE, BLACK, self.player_pokemon.skill1, 30)
        p_skill2 = Button(380, 300, 100, 50, WHITE, BLACK, self.player_pokemon.skill2, 30)


        turn = 1
        data = random.choice(self.pokemon_data)
        enemies_pokemon = pokemon(data["name"], data["img"], data["health"], data["attack"],
                                  data["skill1"], data["skill2"], 400, 50)
        while battle:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.battle_mode = False
                    battle = False
                    self.running = False

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(p_health, p_health_rect)
            self.screen.blit(p_skill1.image, p_skill1.rect)
            self.screen.blit(p_skill2.image, p_skill2.rect)
            self.screen.blit(self.player_pokemon.image, self.player_pokemon.rect)
            self.screen.blit(enemies_pokemon.image, enemies_pokemon.rect)
            self.clock.tick(FPS)
            pygame.display.update()


g = Game()
# g.intro_screen()
g.pokemon_selection()
# g.pokemon_battle()
g.new()
while g.running:
    g.main()
    g.game_over()
pygame.quit()
sys.exit()
