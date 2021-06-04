import pygame, sys
from pygame.locals import *


## Inicialização, define os variaveis iniciais para o funcionamento do jogo

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((800,600)) #Altura e largura da janela
pygame.display.set_caption('Angry cat adventure') # Titulo da janela
background = pygame.Surface(screen.get_size())
background = background.convert() #Converte toda superficie da tela em pixel, serve para ficar mais rapido.
color = (106, 154, 193)
background.fill(color)

# Variáveis de gravidade, pontuação, backup da pontuação, e template da fase 

gravity = 0.75
score = 0
save_score = 0
template = 0 

# Variáveis buleanas onde são definidas condições

moving_right = False
moving_left = False
shoot = False
start_game = False
game_over = False
level_2 = False

add_0 = True
add_1 = True
add_2 = True
add_3 = True

# Variáveis onde são carregads as imagem

font = pygame.font.SysFont('comic sans', 30) # Fonte do jogo

wool_img = pygame.image.load('resources/ball/2.png')
health_item_img = pygame.image.load('resources/items/0.png')
ammo_item_img = pygame.image.load('resources/items/1.png')

# Imagens da fase 1

spr_grass = pygame.image.load('resources/background/spr_grass.png')
spr_grass = pygame.transform.scale(spr_grass, (spr_grass.get_width() * 2, spr_grass.get_height() * 2))
spr_dirt = pygame.image.load('resources/background/spr_dirt.png')
spr_dirt = pygame.transform.scale(spr_dirt, (spr_dirt.get_width() * 2, spr_dirt.get_height() * 2))
spr_plant = pygame.image.load('resources/background/spr_plant.png')
spr_plant = pygame.transform.scale(spr_plant, (spr_plant.get_width() * 2, spr_plant.get_height() * 2))

# Imagens da fase 2

spr_grass_1 = pygame.image.load('resources/background/spr_grass_1.png')
spr_grass_1 = pygame.transform.scale(spr_grass_1, (spr_grass_1.get_width() * 2, spr_grass_1.get_height() * 2))
spr_dirt_1 = pygame.image.load('resources/background/spr_dirt_1.png')
spr_dirt_1 = pygame.transform.scale(spr_dirt_1, (spr_dirt_1.get_width() * 2, spr_dirt_1.get_height() * 2))
spr_plant_1 = pygame.image.load('resources/background/spr_plant_1.png')
spr_plant_1 = pygame.transform.scale(spr_plant_1, (spr_plant_1.get_width() * 2, spr_plant_1.get_height() * 2))

item_boxes = {'health': health_item_img,'ammo': ammo_item_img} #Dic onde contem a imagem da 'vida' e da 'munição'

# Rotina que cria os objetos do fundo 

def obj(x):
    pygame.draw.line(screen, (39, 39, 39), (0,400), (800, 400))
    if x == 0:
        screen.blit(spr_grass, (0,400))
        screen.blit(spr_dirt, (0,432))
        screen.blit(spr_dirt, (0,464))
        screen.blit(spr_dirt, (0,495))
        screen.blit(spr_dirt, (0,527))
        screen.blit(spr_dirt, (0,559))
        screen.blit(spr_dirt, (0,591))
        screen.blit(spr_plant, (0,376))
        screen.blit(spr_plant, (500,376))
        screen.blit(spr_plant, (760,376))
        screen.blit(spr_plant, (320,376))
    if x == 1:
        screen.blit(spr_grass_1, (0,400))
        screen.blit(spr_dirt_1, (0,432))
        screen.blit(spr_dirt_1, (0,464))
        screen.blit(spr_dirt_1, (0,495))
        screen.blit(spr_dirt_1, (0,527))
        screen.blit(spr_dirt_1, (0,559))
        screen.blit(spr_dirt_1, (0,591))
        screen.blit(spr_plant_1, (0,376))
        screen.blit(spr_plant_1, (500,376))
        screen.blit(spr_plant_1, (760,376))
        screen.blit(spr_plant_1, (320,376))

## load sprite do player
player_animation = {}

def load_animation(char_type, file, scale, x):
    global player_animation
    temp_list = list()
    for n in range(x):
        img = pygame.image.load(f'resources/{char_type}/{file}/{n}.png')
        img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
        temp_list.append(img)
    player_animation[file] = temp_list
     
## Classe do Player

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed , char_type, ammo): #Aqui são as variáveis iniciais da classe
        self.alive = True
        self.x = x
        self.y = y
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.shoot_cooldown = 0
        self.ammo = ammo
        self.Start_ammo = ammo
        self.health = 100
        self.max_health = self.health
        self.direction = 1
        self.speed_y = 0
        self.flip = False
        self.jump = False
        self.in_ar = False
        load_animation(char_type, 'idle', scale, 5)
        load_animation(char_type, 'run', scale, 8)
        self.animation_list = player_animation
        self.frame_index = 0
        self.action = 'idle'
        self.update_time = pygame.time.get_ticks()
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

    def update(self): # Aqui a rotina update faz update das animaçoes, checa se o player está vivo e controlo o tempo que o personagem atira
        self.update_animation()
        self.check_alive()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1
       
    def move(self, moving_right, moving_left): # Essa rotina serve para fazer o boneco se movimentar
        dx = 0
        dy = 0
        
        # aqui definimos se ele se movimenta para direita ou esquerda
        
        if moving_right: 
            dx = self.speed # velocidade que se move
            self.flip = False # Se flipa a imagem do jogador para a direção desejada
            self.direction = 1 # Direção onde o 'tiro' do jogador sai
        if moving_left:
            dx = -self.speed
            self.flip = True
            self.direction = -1

        # Aqui definimos o pulo do personagem
            
        if (self.jump == True) and (self.in_ar == False):
            self.speed_y = -15
            self.jump = False
            self.in_ar = True

        self.speed_y += gravity
        dy += self.speed_y

        # Aqui é a colisão do player com o chão
        
        if self.rect.bottom + dy > 400:
            dy = 400 - self.rect.bottom
            self.in_ar = False
        
        self.rect.x += dx # Movimentação eixo x
        self.rect.y += dy # Movimentação eixo y
        
    def update_animation(self): # Aqui faz o update dos sprite
        if (moving_right == False)and(moving_left == False): # Quando parado faz o movimento de 'IDLE'
            if self.frame_index >= 5:
                self.frame_index = 0 
            self.action = 'idle'
        else:
            self.action = 'run' # Se estar se movendo faz a animação de 'RUN'
            
        if self.frame_index >= len(self.animation_list[self.action]): # Aqui é onde faz o loop das imagens
            self.frame_index = 0
            
        speed_animation = 200 ## Velocidade que as imagens são trocadas
        self.image = self.animation_list[self.action][self.frame_index] # Aqui é o Sprite que aparecerá na tela, onde fica trocando.
        
        if pygame.time.get_ticks() - self.update_time > speed_animation: # Loop onde troca os sprite da lista ao decorer do tempo passado
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
            
    def shoot(self): # Aqui define quando atiramos
        if self.shoot_cooldown == 0 and self.ammo > 0:
            self.shoot_cooldown = 15 # O tempo que necessita para atirar de novo
            bullet = Bullet(self.rect.centerx + (0.8*self.rect.size[0]*self.direction), self.rect.centery, self.direction) # Onde o objeto 'Bala' é criado
            bullet_group.add(bullet) # Adiciona o objeto 'bala'
            self.ammo -= 1 # Diminui a quantidade de bala que o player tem

    def check_alive(self): # Checa se o player está vivo
        if self.health <= 0:
            self.health = 0
            self.alive = False # Se ele tem 0 de vida, define que o player morreu
            
    def respawn(self): # Quando o player morre e reinicia
        self.health = 100
        self.ammo = self.Start_ammo
        self.rect.x = self.x
        self.rect.y = self.y
        self.alive = True
            
    def draw(self): # Desenha o objeto player na tela
        screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

# Classe do inimigo

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, scale, speed , char_type,damage , cooldown): # Variável iniciais do inimigo
        self.x = x
        self.y = y
        self.speed = speed
        self.health = 100
        self.max_health = 100
        self.char_type = char_type
        self.scale = scale
        self.enemy_animation = {}
        self.frame_index = 0
        self.speed_y = 0
        self.action = 'idle'
        self.frame_index = 0
        self.direction = 1
        self.update_time = pygame.time.get_ticks()
        self.enemy_animation = {}
        self.moving_right = False
        self.moving_left = False
        self.alive = True
        self.flip = False
        self.enemy_load_animation('run')
        self.animation_list = self.enemy_animation
        self.enemy_load_animation('idle')
        self.animation_list = self.enemy_animation
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (self.x,self.y)
        self.hit_cooldown = 0
        self.cooldown = cooldown
        self.cooldown_respawn = cooldown
        self.damage = damage
        self.difficulty = 1 

    def enemy_load_animation(self, file): # Carrega as animaçoes do inimigo
        temp_list = list()
        for n in range(6):
            img = pygame.image.load(f'resources/{self.char_type}/{file}/{n}.png')
            img = pygame.transform.scale(img, (img.get_width() * self.scale, img.get_height() * self.scale))
            temp_list.append(img)
        self.enemy_animation[file] = temp_list
        
    def update(self):
        if self.health > 0: # Checa se o inimigo stá vivo
            self.update_animation()
            self.move()
            self.draw()
            self.health_bar = HealthBar(self.rect.x -15, self.rect.y-20, self.health, self.max_health) # Cria a barra de vida do inimigo
            self.health_bar.draw(self.health, 75, 10)
            if self.hit_cooldown > 0: # Diminui o cooldown do ataque
                self.hit_cooldown -= 1
            if (pygame.Rect.colliderect(self.rect, player.rect)) and(player.alive == True): # Checa a colisão com o player
                if self.hit_cooldown == 0:
                    self.hit_cooldown = 20 
                    player.health -= self.damage # Diminui a vida do player
        else:
            self.alive = False

    def respawn(self): # Rotina de renascimento do inimigo
        self.cooldown_respawn -= 1
        if self.cooldown_respawn == 0:
            self.health = 100
            self.alive = True
            self.rect.x = self.x
            self.rect.y = self.y
            # o self.difficulty faz com que na fase 2 eles renascam mais rapido
            self.cooldown_respawn = self.cooldown/self.difficulty 
            
        
    def update_animation(self): # Faz o update das animações do inimigo
        if (self.moving_right == False)and(self.moving_left == False):
            if self.frame_index >= 5:
                self.frame_index = 0 
            self.action = 'idle'
        else:
            self.action = 'run'
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
    
        speed_animation = 150
        self.image = self.animation_list[self.action][self.frame_index]
        if pygame.time.get_ticks() - self.update_time > speed_animation:
            self.update_time = pygame.time.get_ticks()
            self.frame_index += 1
        
    def move(self): # Rotina de movimento do inimigo
        dy = 0
        self.speed_y += gravity
        dy += self.speed_y

        # Faz com que o inimigo sempre esteja perseguindo o player
        
        if self.rect.x - 35 < player.rect.x:
            self.moving_right = True
            self.flip = False
            self.rect.x += self.speed
            self.direction = 1
        
        if self.rect.x + 30 > player.rect.x:
            self.moving_left = True
            self.flip = True
            self.rect.x -= self.speed
            self.direction = -1

        # Se o inimigo estiver proximo, ele fica em 'idle'
        
        if (self.rect.x + 30 >= player.rect.x)and(self.rect.x - 35 <= player.rect.x):
            self.moving_left = False
            self.moving_right = False
        
        # Colisão do inimigo com o chão
        
        if self.rect.bottom + dy > 400:
            dy = 400 - self.rect.bottom
        
        self.rect.y += dy # Movimento no eixo y

    def draw(self): # Desenha o inimo na tela se ele estiver vivo
        if self.alive:
            screen.blit(pygame.transform.flip(self.image, self.flip, False), self.rect)

# Classe do 'Tiro' do player

class Bullet(pygame.sprite.Sprite): 
    def __init__(self, x, y, direction): # Variáveis do tiro
        pygame.sprite.Sprite.__init__(self)
        self.speed = 10
        self.image = wool_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.direction = direction
        
    def update(self): # Update do 'tiro' na tela
        global score

        # Velocidade do tiro na direção onde o player está olhando
        self.rect.x += (self.direction * self.speed)
        
        if self.rect.right < 0 or self.rect.left > 800: # Se o 'tiro' passar da tela do jogo faz ele se destruir 
            self.kill()

        # Se o 'tiro' colidir com os inimigos
        
        if pygame.sprite.spritecollide(enemy_0, bullet_group, False):  # se a 'tiro' colidir com o enemy_0
            if enemy_0.alive:
                enemy_0.health -= 25 # O dano que o inimigo leva
                if enemy_0.health <= 0: # Se o inimigo morre o score aumenta
                    score += 10
                self.kill() # Se a bala colidir ela é destruida

        if pygame.sprite.spritecollide(enemy_1, bullet_group, False):
            if enemy_1.alive:
                enemy_1.health -= 25
                if enemy_1.health <= 0:
                    score += 10
                self.kill()
                
        if pygame.sprite.spritecollide(enemy_2, bullet_group, False):
            if enemy_2.alive:
                enemy_2.health -= 10
                if enemy_2.health <= 0:
                    score += 25
                self.kill()
                
        if pygame.sprite.spritecollide(enemy_3, bullet_group, False):
            if enemy_3.alive:
                enemy_3.health -= 10
                if enemy_3.health <= 0:
                    score += 25
                self.kill()

# Classe do item de vida e de minição

class Items(pygame.sprite.Sprite): 
    def __init__(self, item_type, x, y): # Variáveis de inicio do objeto item
        pygame.sprite.Sprite.__init__(self)
        self.item_type = item_type
        self.image = item_boxes[self.item_type]
        self.image = pygame.transform.scale(self.image, (self.image.get_width() * 2, self.image.get_height() * 2))
        self.rect = self.image.get_rect()
        self.rect.midtop = (x + 40//2, y + (40 - self.image.get_height()))

    def update(self): # Faz o update do item quando é colidido com o player
        if pygame.sprite.collide_rect(self, player): # Item de vida
            if self.item_type == 'health':
                player.health += 25
                if player.health > player.max_health:
                    player.health = player.max_health
            elif self.item_type == 'ammo': # item de munição
                player.ammo += 55
            self.kill() # Elimina o item da tela

# Classe da barra de vida

class HealthBar(): 
    def __init__(self, x, y, health, max_health): # Variáveis iniciais da barra de vida
        self.x = x
        self.y = y
        self.health = health
        self.max_health = max_health
        self.size_x = 150
        self.size_y = 20

    def draw(self, health, size_x, size_y): # Define como desenha a barra de vida na tela
        self.health = health # igula a vida do objeto que me refirir
        self.size_x = size_x
        self.size_y = size_y
        ratio = self.health / self.max_health
        pygame.draw.rect(screen, (0, 0, 0), (self.x - 2, self.y - 2, size_x + 4, size_y + 4)) 
        pygame.draw.rect(screen, (142, 13, 24), (self.x, self.y, size_x, size_y))
        
        # Barra da vida verde que diminui de acordo com a vida do player ou inimigo
        pygame.draw.rect(screen, (35, 141, 48), (self.x, self.y, size_x*ratio, size_y)) 

def add_item(): # Rotina que adiciona item na tela
    item_box_group.add(item_box_h)
    item_box_group.add(item_box_a)

def draw_text(text, font, color, x, y): # Rotina que adiciona texto na tela
    # redenriza texto em imagem
    img = font.render(text, True, color)
    # renderiza imagem na tela
    screen.blit(img, (x, y)) 

# Cria um grupo de objetos

bullet_group = pygame.sprite.Group() # Grupo de 'bala'
item_box_group = pygame.sprite.Group() # Grupo de 'item'


# Adiciona o objeto dentro do grupo

item_box_a = Items('health', 100, 360) 
item_box_h = Items('ammo', 700, 360)

# Definição os parametros ao objeto para criar ele
        
player = Player(200, 200, 3, 5, 'player', 70)
health_bar = HealthBar(10, 10, player.health, player.max_health) # Adiciona a barra de vida para o personagem

# Inimigo verde mais rapido, porem mais fraco

enemy_0 = Enemy(900, 300, 4, 2, 'enemy_0', 5, 300) # Surge da direita
enemy_1 = Enemy(-300, 300, 4, 2, 'enemy_0', 5, 300) # Surge da esquerda

# Inimigo Roxo ele é mais forte, poré mais lento

enemy_2 = Enemy(2000, 300, 6, 1, 'enemy_1', 10, 450) # Surge da direita
enemy_3 = Enemy(-1500, 300, 6, 1, 'enemy_1', 10, 450) # Surge da esquerda

# Aqui é quando o jogo está rodando

while True:
    clock.tick(60) # O FPS do jogo

    if start_game == False: # Tela de inicio do jogo

        screen.fill((51, 51, 204))

        # Texto que apareceram na tela
        
        draw_text('Angry cat adventure', font, (0,0,0), 320,100)
        draw_text('Aperte ESPAÇO ou P para iniciar', font, (0,0,0), 250,450)
        draw_text('Utilize as setas para se movimentar', font, (0,0,0), 250,300)
        draw_text('Aperte a tecla X para jogar bolas de lã', font, (0,0,0), 250,325)
        draw_text('Aperte a tecla ESC ou Q para sair do jogo', font, (0,0,0), 235,350)

         # Se o player morrer aparecerá outras coisas na tela
        if game_over == True:
            draw_text('Game Over', font, (26, 0, 51), 350, 200)
            draw_text(f'Seu score: {save_score}', font, (0,0,0), 350, 225)
            
    
    else:

        screen.blit(background, (0, 0)) # Carrega a tela de fundo do jogo, atualizando ela sempre

        # Se o jogador chegar a pontuação de 500 vai pra fase 2
        
        if score >= 50 and level_2 == False:
            color = (24, 38, 65) # muda a cor do fundo
            time_text = pygame.time.get_ticks() + 6000
            time_item = pygame.time.get_ticks() + 35000
            
            # Reinicia os inimigos
            
            enemy_0.alive = False
            enemy_1.alive = False
            enemy_2.alive = False
            enemy_3.alive = False

            # Diminui a velocidade com que eles aparecem no jogo
            
            enemy_0.difficulty = 2
            enemy_1.difficulty = 2
            enemy_2.difficulty = 2
            enemy_3.difficulty = 2

            # Muda o visual do backgraund para de noite
            
            template = 1
            level_2 = True
        
        if level_2 == True:
            screen.fill(color) # muda a cor de fundo
            if pygame.time.get_ticks() < time_text: 
                draw_text('Fase 2', font, (26, 0, 51), 350, 200) # Mostra que está na fase 2
                
            # Faz com que os item apareçam no jogo ao decorre de 35 segundos
            if pygame.time.get_ticks() > time_item: 
                add_item()
                time_item = pygame.time.get_ticks() + 35000

        if level_2 == False: # Reseta o level caso o player morra no level 2
            screen.fill((106, 154, 193))
            template = 0

        # carrega o cenario de fundo
        obj(template)

        # Desenha na tela
        health_bar.draw(player.health, 150, 20) # Barra de vida do player
        draw_text(f'Bola de lã: {player.ammo}', font, (0, 0, 0), 10, 35) # A quantidade de minição
        draw_text(f'Score: {score}', font, (0, 0, 0), 10,55) # A pontuação

        # Faz o update dos grupos

        # Das bolas de lã
        bullet_group.update()
        bullet_group.draw(screen) # Desenha na tela

        # Dos itens 
        item_box_group.update()
        item_box_group.draw(screen) # Desenha na tela

        # Adiciona itens no jogo a partir de um determinado score
        
        if score >= 100 and add_0 == True:
            add_item()
            add_0 = False
        if score >= 225 and add_1 == True:
            add_item()
            add_1 = False
        if score >= 325 and add_2 == True:
            add_item()
            add_2 = False
        if score >= 425 and add_3 == True:
            add_item()
            add_3 = False

        # Ações dos objetos
        
        if player.alive:
            if shoot:
                player.shoot() # Se o player está vivo pode atirar
                
            # se estiver vivo pode se mover, fazer update no player e desenhar na tela
            player.move(moving_right, moving_left)
            player.update()
            player.draw()
        else: # Se estiver morto
            game_over = True # faz com que apareça que morreu no menu
            player.respawn() # Retorna a sua posição inicial
            save_score = score # Salva a pontuação obtida
            score = 0 # Zera a pontuação global
            start_game = False # Vai pra tela de menu

            # Se o player morrer mata todos os inimigos para reiniciar eles
            enemy_0.alive= False
            enemy_1.alive= False
            enemy_2.alive= False
            enemy_3.alive= False

            add_0 = True
            add_1 = True
            add_2 = True
            add_3 = True

            enemy_0.difficulty = 1
            enemy_1.difficulty = 1
            enemy_2.difficulty = 1
            enemy_3.difficulty = 1

            level_2 = False
            

        # Checa se os inimigos estão vivos
        
        if enemy_0.alive:
            enemy_0.update()
        else: # se não faz com que eles apareçam de novo
            enemy_0.respawn()
            
        if enemy_1.alive:
            enemy_1.update()
        else:
            enemy_1.respawn()
            
        if enemy_2.alive:
            enemy_2.update()
        else:
            enemy_2.respawn()
            
        if enemy_3.alive:
            enemy_3.update()
        else:
            enemy_3.respawn()

    # Para cada ação que o jogador fizer execulta uma ação
    for event in pygame.event.get():

        # Se pressionar no x da janela
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        # Se pressionar a tecla
        if event.type == pygame.KEYDOWN:

            # Se pressionar Esc ou q, fecha o jogo
            if event.key == pygame.K_ESCAPE:
                pygame.quit() # Fecha o canvas
                sys.exit() # Para de execultar a programação
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

            if event.key == pygame.K_RIGHT: # Seta direita
                moving_right = True # movimenta para direira
            if event.key == pygame.K_LEFT: # Seta esquerda
                moving_left = True # Movimenta para esquerda
            if event.key == pygame.K_UP: # Seta cima
                player.jump = True # Pula
            if event.key == pygame.K_x: # Tecla x
                shoot = True  # 'Atira'

            # Quando estiver no menu
            if (start_game == False)and(event.key == pygame.K_p): # Tecla P
                start_game = True # Inicia o jogo
            if (start_game == False)and(event.key == pygame.K_SPACE): # Tecla spaço
                start_game = True # Inicia o jogo

        # Se soltar a tecla para a ação
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                moving_right = False
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_UP:
                player.jump = False
            if event.key == pygame.K_x:
                shoot = False

                    
    pygame.display.update() # Atualiza a tela
    


