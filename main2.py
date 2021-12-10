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
                pygame.quit()
                sys.exit()

    def update(self):
        self.all_sprites.update()
        if self.enemy_counter == 0 and self.boss_mode:
            self.game_over()
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
        g.pokemon_selection()
        g.new(TILEMAP)
        while self.playing:
            if self.battle_mode:
                self.pokemon_battle()
            else:
                self.events()
                self.update()
                self.draw()

        self.running = False

    def game_over(self):
        selection = True

        title = self.font.render('Game Over', True, BLACK)
        title_rect = title.get_rect(x=200, y=10)

        play_button = Button(200, 50, 200, 50, WHITE, BLACK, 'New Game', 32)
        quit_button = Button(200, 110, 100, 50, WHITE, BLACK, 'Quit', 32)
        while selection:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    if play_button.rect.collidepoint(mouse_pos):
                        selection = False
                        self.boss_mode = False
                        self.main()
                    elif quit_button.rect.collidepoint(mouse_pos):
                        selection = False
                        pygame.quit()
                        sys.exit()
            self.screen.blit(self.intro_background, (0, 0))
            self.screen.blit(title, title_rect)
            self.screen.blit(play_button.image, play_button.rect)
            self.screen.blit(quit_button.image, quit_button.rect)
            self.clock.tick(FPS)
            pygame.display.update()

    def fade(self):
        fade = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
        fade.fill((0, 0, 0))
        for alpha in range(0, 150):
            fade.set_alpha(alpha)
            self.screen.blit(fade, (0, 0))
            pygame.display.update()
            pygame.time.delay(5)

    def dissolve(self):
        speed = 2
        first = pygame.image.load('img/image_1.jpg').convert_alpha()
        second = pygame.image.load('img/image_2.jpg').convert_alpha()
        x = 1
        y = 255
        diss_1 = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
        diss_1.fill(BLACK)
        diss_2 = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
        diss_2.fill(BLACK)
        diss_1.set_alpha(x)
        diss_2.set_alpha(y)
        diss_1.blit(first, (0, 0))
        diss_2.blit(second, (0, 0))
        while x <= 255:
            diss_1.set_alpha(x)
            diss_2.set_alpha(y)
            self.screen.blit(diss_1, (0, 0))
            self.screen.blit(diss_2, (0, 0))
            pygame.display.flip()
            self.clock.tick(FPS)
            pygame.event.pump()
            x += speed
            y -= speed

    def intro_screen(self):
        intro = True

        title = self.font.render('Pokemon', True, BLACK)
        title_rect = title.get_rect(x=200, y=10)

        play_button = Button(200, 50, 100, 50, WHITE, BLACK, 'Play', 32)
        quit_button = Button(200, 110, 100, 50, WHITE, BLACK, 'Quit', 32)
        while intro:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
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
        self.fade()
        selection = True

        title = self.font.render('Starter Selection', True, BLACK)
        title_rect = title.get_rect(x=200, y=10)

        charmander = StarterButton(235, 60, 150, 150, 'img/charmander.png')
        squirtle = StarterButton(120, 240, 150, 150, 'img/squirtle.png')
        bulbasaur = StarterButton(350, 240, 150, 150, 'img/bulbasaur.png')
        self.pokemon_data = json.load(open("pokemon_data.json"))
        fading = True
        while selection:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
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
        self.fade()

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
        self.dissolve()
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
                    pygame.quit()
                    sys.exit()

            mouse_pos = pygame.mouse.get_pos()
            mouse_pressed = pygame.mouse.get_pressed()

            if turn == 1:
                crit = random.randint(1, 10)
                if p_skill1.is_pressed(mouse_pos, mouse_pressed):
                    attack_string = "{} used {}".format(self.player_pokemon.name, self.player_pokemon.skill1)
                    turn, e_current_health, e_health, e_health_rect = self.generate_attack_box(attack_string, e_health,
                                                                                               self.player_pokemon.attack,
                                                                                               e_current_health,
                                                                                               enemies_pokemon.health,
                                                                                               turn, crit)

                if p_skill2.is_pressed(mouse_pos, mouse_pressed):
                    attack_string = "{} used {}".format(self.player_pokemon.name, self.player_pokemon.skill2)
                    turn, e_current_health, e_health, e_health_rect = self.generate_attack_box(attack_string, e_health,
                                                                                               self.player_pokemon.attack,
                                                                                               e_current_health,
                                                                                               enemies_pokemon.health,
                                                                                               turn, crit)

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

            elif turn == 2:
                enemy_skill_int = random.randint(1, 2)
                if enemy_skill_int == 1:
                    enemy_string = "{} used {}".format(enemies_pokemon.name, enemies_pokemon.skill1)
                    turn, current_health, p_health, p_health_rect = self.generate_attack_box(enemy_string, p_health,
                                                                                             enemies_pokemon.attack,
                                                                                             current_health,
                                                                                             self.player_pokemon.health,
                                                                                             turn, 0, True)

                #     attack_title = self.font.render(enemy_string, True, BLACK)
                #     attack_title_rect = attack_title.get_rect(x=200, y=400)
                #     self.screen.blit(attack_title, attack_title_rect)
                #     pygame.display.update()
                #     current_health -= enemies_pokemon.attack
                #     turn = 1
                #     pygame.display.update()
                if enemy_skill_int == 2:
                    enemy_string = "{} used {}".format(enemies_pokemon.name, enemies_pokemon.skill2)
                    turn, current_health, p_health, p_health_rect = self.generate_attack_box(enemy_string, p_health,
                                                                                             enemies_pokemon.attack,
                                                                                             current_health,
                                                                                             self.player_pokemon.health,
                                                                                             turn, 0, True)
                if current_health < 0:
                    # Battle won
                    print("Battle lost")
                    battle = self.generate_end_battle("lost")
                    battle_result_title = self.font.render("You Lost!", True, BLACK)
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
                    self.fade()
                    self.game_over()

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
        self.fade()

    def generate_attack_box(self, attack_string, health, attack, current_health, total_health, turn, crit=0,
                            enemy=False):
        attack_title = self.font.render(attack_string, True, BLACK)
        attack_title_rect = attack_title.get_rect(x=200, y=400)
        self.screen.blit(attack_title, attack_title_rect)
        pygame.display.update()
        pygame.time.wait(3000)

        attack_title_rect = attack_title.get_rect(x=1000, y=1000)
        self.screen.blit(attack_title, attack_title_rect)
        pygame.display.update()

        # remove the health box
        health_rect = health.get_rect(x=1000, y=1000)
        self.screen.blit(health, health_rect)
        dmg = attack
        if crit == 1:
            dmg *= 2
        current_health -= dmg
        print("{} from function".format(current_health))
        if enemy:
            x_val, y_val = 270, 250
            health_rect = health.get_rect(x=1000, y=1000)
            self.screen.blit(health, health_rect)
            pygame.display.update()
        else:
            x_val, y_val = 240, 50
            health_rect = health.get_rect(x=1000, y=1000)
            self.screen.blit(health, health_rect)
            pygame.display.update()
        health = self.font.render('HP: {}/{}'.format(current_health, total_health), True, BLACK)
        health_rect = health.get_rect(x=x_val, y=y_val)
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
            self.enemy_counter -= 1
            self.running = False
            self.battle_mode = False
            return True

    def boss_fight(self):
        self.boss_mode = True
        self.new(BOSSMAP)

    def render_screen(self, stats=None):
        battle = self.generate_end_battle("win")
        battle_result_title = self.font.render("You Win!", True, BLACK)
        battle_result_rect = battle_result_title.get_rect(x=200, y=400)

        self.screen.blit(self.intro_background, (0, 0))
        self.screen.blit(title, title_rect)
        self.screen.blit(p_health, p_health_rect)
        self.screen.blit(p_skill1.image, p_skill1.rect)
        self.screen.blit(p_skill2.image, p_skill2.rect)
        self.screen.blit(e_health, e_health_rect)
        if stats == "win":
            battle_result_title = self.font.render("You Win!", True, BLACK)
            battle_result_rect = battle_result_title.get_rect(x=200, y=400)
            self.screen.blit(battle_result_title, battle_result_rect)
        if stats == "lose":
            battle_result_title = self.font.render("You Lose!", True, BLACK)
            battle_result_rect = battle_result_title.get_rect(x=200, y=400)
            self.screen.blit(battle_result_title, battle_result_rect)
        self.screen.blit(self.player_pokemon.image, self.player_pokemon.rect)
        self.screen.blit(enemies_pokemon.image, enemies_pokemon.rect)
        self.clock.tick(FPS)
        pygame.display.update()
        pygame.time.wait(1000)


if __name__ == "__main__":
    g = Game()
    while g.running:
        g.intro_screen()
        g.main()
