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
        self.enemy_counter = 0
        self.boss_mode = False

    def create_tile_map(self, tilemap):
        for i, row in enumerate(tilemap):
            for j, column in enumerate(row):
                Ground(self, j, i)
                if column == "B":
                    Block(self, j, i)
                if column == "E":
                    Enemy(self, j, i, self.boss_mode)
                    self.enemy_counter += 1
                if column == "P":
                    self.player = Player(self, j, i)

    def new(self, map):
        self.playing = True

        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.blocks = pygame.sprite.LayeredUpdates()
        self.enemies = pygame.sprite.LayeredUpdates()
        self.attacks = pygame.sprite.LayeredUpdates()

        self.create_tile_map(map)

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
        if self.enemy_counter == 0:
            self.boss_fight()

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
                        self.player_pokemon = self.pokemon_generation(False, 100, 250, "Charmander")
                        selection = False
                    elif squirtle.rect.collidepoint(mouse_pos):
                        self.player_pokemon = self.pokemon_generation(False, 100, 250, "Squirtle")
                        selection = False
                    elif bulbasaur.rect.collidepoint(mouse_pos):
                        self.player_pokemon = self.pokemon_generation(False, 100, 250, "Bulbasaur")
                        selection = False
            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(charmander.image, charmander.rect)
            self.screen.blit(squirtle.image, squirtle.rect)
            self.screen.blit(bulbasaur.image, bulbasaur.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def pokemon_generation(self, random_spawn, x, y, name=""):
        if random_spawn:
            data = random.choice([x for x in self.pokemon_data if x["name"] != "Mewtwo"])
            generated_pokemon = pokemon(data["name"], data["img"], data["health"], data["attack"],
                                        data["skill1"], data["skill2"], x, y)
        else:
            for data in self.pokemon_data:
                if data["name"] == name:
                    generated_pokemon = pokemon(data["name"], data["img"], data["health"], data["attack"],
                                                data["skill1"], data["skill2"], x, y)
        return generated_pokemon

    def pokemon_battle(self):
        battle = True

        current_health = self.player_pokemon.health
        if self.boss_mode:
            enemies_pokemon = self.pokemon_generation(False, 400, 50, "Mewtwo")
        else:
            enemies_pokemon = self.pokemon_generation(True, 400, 50)
        e_current_health = enemies_pokemon.health
        title = self.font.render('Battle', True, BLACK)
        title_rect = title.get_rect(x=200, y=10)

        p_health = self.font.render('HP: {}/{}'.format(current_health, self.player_pokemon.health), True, BLACK)
        p_health_rect = p_health.get_rect(x=270, y=250)
        p_skill1 = Button(270, 300, 100, 50, WHITE, BLACK, self.player_pokemon.skill1, 30)
        p_skill2 = Button(380, 300, 100, 50, WHITE, BLACK, self.player_pokemon.skill2, 30)

        e_health = self.font.render('HP: {}/{}'.format(e_current_health, enemies_pokemon.health), True, BLACK)
        e_health_rect = e_health.get_rect(x=240, y=50)

        turn = 1

        while battle:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    battle = False
                    self.running = False
                    self.playing = False

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if turn == 1:
                if p_skill1.is_pressed(mouse_pos, mouse_pressed):
                    attack_string = "{} used {}".format(self.player_pokemon.name, self.player_pokemon.skill1)
                    turn, e_current_health, e_health, e_health_rect = self.generate_attack_box(attack_string, e_health,
                                                                                               self.player_pokemon.attack,
                                                                                               e_current_health,
                                                                                               enemies_pokemon.health,
                                                                                               turn)

                if p_skill2.is_pressed(mouse_pos, mouse_pressed):
                    attack_string = "{} used {}".format(self.player_pokemon.name, self.player_pokemon.skill2)
                    turn, e_current_health, e_health, e_health_rect = self.generate_attack_box(attack_string, e_health,
                                                                                               self.player_pokemon.attack,
                                                                                               e_current_health,
                                                                                               enemies_pokemon.health,
                                                                                               turn)

                if e_current_health < 0:
                    # Battle won
                    print("Battle won")
                    battle = self.generate_end_battle("win")
                    battle_result_title = self.font.render("You Win!", True, BLACK)
                    battle_result_rect = battle_result_title.get_rect(x=200, y=400)

                    self.screen.blit(self.intro_background, (0, 0))
                    self.screen.blit(title, title_rect)
                    self.screen.blit(p_health, p_health_rect)
                    self.screen.blit(p_skill1.image, p_skill1.rect)
                    self.screen.blit(p_skill2.image, p_skill2.rect)
                    self.screen.blit(e_health, e_health_rect)
                    self.screen.blit(battle_result_title, battle_result_rect)
                    self.screen.blit(self.player_pokemon.image, self.player_pokemon.rect)
                    self.screen.blit(enemies_pokemon.image, enemies_pokemon.rect)
                    self.clock.tick(FPS)
                    pygame.display.update()
                    pygame.time.wait(1000)

            if turn == 2:
                pass
                # enemy_skill_int = random.randint(1,2)
                # if enemy_skill_int == 1:
                #     enemy_string = "{} used {}".format(enemies_pokemon.name, enemies_pokemon.skill1)
                #     attack_title = self.font.render(enemy_string, True, BLACK)
                #     attack_title_rect = attack_title.get_rect(x=200, y=400)
                #     self.screen.blit(attack_title, attack_title_rect)
                #     pygame.display.update()
                #     current_health -= enemies_pokemon.attack
                #     turn = 1
                #     pygame.display.update()
                # if enemy_skill_int == 2:
                #     enemy_string = "{} used {}".format(enemies_pokemon.name, enemies_pokemon.skill2)
                #     attack_title = self.font.render(enemy_string, True, BLACK)
                #     attack_title_rect = attack_title.get_rect(x=200, y=400)
                #     self.screen.blit(attack_title, attack_title_rect)
                #     pygame.display.update()
                #     current_health -= enemies_pokemon.attack
                #     turn = 1
                #     pygame.display.update()

            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(p_health, p_health_rect)
            self.screen.blit(p_skill1.image, p_skill1.rect)
            self.screen.blit(p_skill2.image, p_skill2.rect)
            self.screen.blit(e_health, e_health_rect)
            self.screen.blit(self.player_pokemon.image, self.player_pokemon.rect)
            self.screen.blit(enemies_pokemon.image, enemies_pokemon.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def generate_attack_box(self, attack_string, health, attack, current_health, total_health, turn):
        attack_title = self.font.render(attack_string, True, BLACK)
        attack_title_rect = attack_title.get_rect(x=200, y=400)
        self.screen.blit(attack_title, attack_title_rect)
        pygame.display.update()
        pygame.time.wait(3000)

        attack_title_rect = attack_title.get_rect(x=1000, y=1000)
        self.screen.blit(attack_title, attack_title_rect)
        pygame.display.update()

        #remove the health box
        health_rect = health.get_rect(x=1000, y=1000)
        self.screen.blit(health, health_rect)
        dmg = attack
        current_health -= dmg
        print("{} from function".format(current_health))
        health = self.font.render('HP: {}/{}'.format(current_health, total_health), True, BLACK)
        health_rect = health.get_rect(x=240, y=50)
        self.screen.blit(health, health_rect)
        pygame.display.update()
        if turn == 1:
            return 2, current_health, health, health_rect
        return 1, current_health, health, health_rect

    def generate_end_battle(self, battle_result):
        battle_result_title = self.font.render("You {}!".format(battle_result), True, BLACK)
        battle_result_rect = battle_result_title.get_rect(x=200, y=400)
        self.screen.blit(battle_result_title, battle_result_rect)
        pygame.display.update()
        print(battle_result)
        if battle_result == 'win':
            self.enemy_counter -= 1
            self.battle_mode = False
            return False
        else:
            self.running = False
            self.game_over()

    def boss_fight(self):
        self.boss_mode = True
        self.new(BOSSMAP)


if __name__ == "__main__":
    g = Game()
    # g.intro_screen()
    g.pokemon_selection()
    g.new(TILEMAP)
    while g.running:
        g.main()
        g.game_over()
    pygame.quit()
    sys.exit()
