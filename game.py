import pygame
import random
import sys

pygame.init()

pygame.mixer.init()

#Cargar la música de fondo
pygame.mixer.music.load("Sound/Soundtrack.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1) #Reproducir en bucle infinitamente

#Configrar pantalla
WIDTH, HEIGHT = 1366, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Prisioner Escape")

#Color letras
WHITE = (255, 255, 255)

score_max = 0

fuente = pygame.font.Font(None, 40)

#Reloj para FPS
reloj = pygame.time.Clock()

#imagenes de fondo y menus
imagen_fondo = pygame.transform.scale(pygame.image.load("images/Fondo/Fondo_Nivel.jpg"), (WIDTH, HEIGHT)).convert()
fondo_menuinicial = pygame.transform.scale(pygame.image.load("images/Menus/Menu_Principal.png"), (WIDTH, HEIGHT)).convert()
fondo_menupausa = pygame.transform.scale(pygame.image.load("images/Menus/Menu_Pausa.png"), (WIDTH, HEIGHT)).convert()
fondo_gameover = pygame.transform.scale(pygame.image.load("images/Menus/Menu_GameOver.png"), (WIDTH, HEIGHT)).convert()
fondo_victoria = pygame.transform.scale(pygame.image.load("images/Menus/Menu_Victoria.png"), (WIDTH, HEIGHT)).convert()


#Cargar las imagenes de los enemigos y escalar el tamaño de alto y ancho
imagenes_enemigo = [
    pygame.transform.scale(pygame.image.load("images/Enemigos/Patrulla.png").convert_alpha(), (140, 85)),
    pygame.transform.scale(pygame.image.load("images/Enemigos/Automovil_1.png").convert_alpha(), (140, 85)),
    pygame.transform.scale(pygame.image.load("images/Enemigos/Automovil_2.png").convert_alpha(), (140, 85)),
    pygame.transform.scale(pygame.image.load("images/Enemigos/Automovil_3.png").convert_alpha(), (140, 85))
]

#Cargar las imagenes del prisionero (diferentes direcciones) escalando el tamaño
imagenes_prisionero = {
    "arriba": pygame.transform.scale(pygame.image.load("images/Prisionero/Mover_Arriba.png").convert_alpha(), (30, 50)),
    "abajo": pygame.transform.scale(pygame.image.load("images/Prisionero/Mover_Abajo.png").convert_alpha(), (30, 50)),
    "izquierda": pygame.transform.scale(pygame.image.load("images/Prisionero/Mover_Izquierda.png").convert_alpha(), (30, 50)),
    "derecha": pygame.transform.scale(pygame.image.load("images/Prisionero/Mover_Derecha.png").convert_alpha(), (30, 50)),
}

#Clase Prisionero
class Prisionero(pygame.sprite.Sprite):
    def __init__(self, images):
        super().__init__()
        self.images = images
        self.image = self.images["arriba"]  # Imagen por defecto
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)
        self.speed = 40
    
    #Función para mover prisionero
    def mover(self, dirección):
        if dirección == "arriba" and self.rect.top > 0:
            self.rect.y -= self.speed
            self.image = self.images["arriba"]
        elif dirección == "abajo" and self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
            self.image = self.images["abajo"]
        elif dirección == "izquierda" and self.rect.left > 0:
            self.rect.x -= self.speed
            self.image = self.images["izquierda"]
        elif dirección == "derecha" and self.rect.right < WIDTH:
            self.rect.x += self.speed
            self.image = self.images["derecha"]

#Clase de los Enemigos
class Enemigos(pygame.sprite.Sprite):
    def __init__(self, x, y, velocidad, image):
        super().__init__()
        self.speed = velocidad

        #Voltear la imagen si el enemigo se mueve hacia la izquierda
        if self.speed > 0:
            self.image = pygame.transform.flip(image, True, False)  # Voltear horizontalmente
        else:
            self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    #Función para actualizar enemigos
    def update(self, *args):
        self.rect.x += self.speed
        if self.speed > 0 and self.rect.left > WIDTH:
            self.rect.right = 0
        elif self.speed < 0 and self.rect.right < 0:
            self.rect.left = WIDTH

#Función para mostrar texto en pantalla
def draw_text(surface, text, fuente, color, x, y):
    text_surface = fuente.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

#Función para verificar colisiones
def verificar_colisiones(frog, enemies):
    return pygame.sprite.spritecollideany(frog, enemies)

#Función para spawn de enemigos
def spawn_enemigos(enemigos, all_sprites, nivel):
    num_rows = 5
    enemies_per_row = 1 + nivel  #Aumenta la cantidad de enmigos segun el nivel
    row_directions = [-1, 1, -1, 1, -1]

    ENEMY_WIDTH = 120

    #Distancia minima entre los enemigos
    distancia_minima = ENEMY_WIDTH + 20

    for i in range(num_rows):
        y = 100 + i * 100
        if i == num_rows - 1:
            continue

        speed_direction = row_directions[i]
        velocidad = speed_direction * (3 + nivel)

        x_positions = []  #Guardar las posiciones para no superponer

        for _ in range(enemies_per_row):
            intentos = 0 
            while True:
                x = random.randint(0, WIDTH - ENEMY_WIDTH)
                too_close = any(abs(x - other_x) < distancia_minima for other_x in x_positions)
                if not too_close:
                    x_positions.append(x)
                    break
                intentos += 1
                if intentos > 50:
                    break

            imagen_enemigo = imagenes_enemigo[random.randint(0, len(imagenes_enemigo) - 1)]
            enemigo = Enemigos(x, y, velocidad, imagen_enemigo)
            enemigos.add(enemigo)
            all_sprites.add(enemigo)

def draw_button(surface, text, fuente, x, y, w, h):
    button_rect = pygame.Rect(x, y, w, h)
    pygame.draw.rect(surface, WHITE, (x, y, w, h), 2)
    text_surface = fuente.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=(x + w// 2, y + h // 2))
    surface.blit(text_surface, text_rect)
    return button_rect


#Función con el menu principal
def menu_principal():
    
    while True:
        screen.blit(fondo_menuinicial, (0, 0)) 
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if (evento.key == pygame.K_ESCAPE or evento.key == pygame.K_q):
                    pygame.quit()
                    sys.exit()
                if evento.key == pygame.K_SPACE:
                    return
            

#Funcion con el menu de pausa
def menu_pausa():
    pausa = True
    while pausa:
        screen.blit(fondo_menupausa, (0, 0))
        draw_text(screen, "Juego Pausado", fuente, WHITE, WIDTH // 2, HEIGHT // 6)

        boton_reanudar = draw_button(screen, "Reanudar", fuente, WIDTH // 2 - 100, HEIGHT // 3, 200, 50)
        boton_musica = draw_button(screen, "Música: ON/OFF", fuente, WIDTH // 2 - 125, HEIGHT // 2 - 20, 250, 50)
        boton_reiniciar = draw_button(screen, "Reiniciar", fuente, WIDTH // 2 - 100, HEIGHT // 2 + 60, 200, 50)
        quit_button = draw_button(screen, "Salir", fuente, WIDTH // 2 - 100, HEIGHT // 2 + 140, 200, 50)

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_reanudar.collidepoint(evento.pos):
                    pausa = False
                elif boton_musica.collidepoint(evento.pos):
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                elif boton_reiniciar.collidepoint(evento.pos):
                    juego()
                    return
                elif quit_button.collidepoint(evento.pos):
                    pygame.quit()
                    sys.exit()


#Funcion con la pantalla de game over
def game_over(score):
    while True:
        screen.blit(fondo_gameover, (0, 0))
        draw_text(screen, f"Puntuación Final: {score}", fuente, WHITE, WIDTH // 2, HEIGHT // 3)
        draw_text(screen, f"Puntuación Mas Alta: {score_max}", fuente, WHITE, WIDTH // 2, HEIGHT // 2)
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    juego()
                if (evento.key == pygame.K_ESCAPE or evento.key == pygame.K_q):
                    pygame.quit()
                    sys.exit()

#Funcion con la pantalla de victoria
def pantalla_victoria(score):
    while True:
        screen.blit(fondo_victoria, (0, 0))
        draw_text(screen, f"Puntuación Final: {score}", fuente, WHITE, WIDTH // 2, HEIGHT // 2)
        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    menu_principal()
                    return
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

#Función principal del juego
def juego():
    global score_max
    # Grupos de sprites
    all_sprites = pygame.sprite.Group()
    enemigos = pygame.sprite.Group()

    #Crear al prisionero
    prisionero = Prisionero(imagenes_prisionero)
    all_sprites.add(prisionero)
    nivel = 1
    score = 0
    iniciar_ticks = pygame.time.get_ticks()

    #Generar los enemigos
    spawn_enemigos(enemigos, all_sprites, nivel)

    running = True
    while running:

        #Control de los FPS
        reloj.tick(60)

        #Eventos dentro del juego
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if evento.type == pygame.KEYDOWN:
                if (evento.key == pygame.K_ESCAPE or evento.key == pygame.K_q):
                    pygame.quit()
                    sys.exit()
                if evento.key == pygame.K_p: #Pausar
                    menu_pausa()
                if (evento.key == pygame.K_UP or evento.key == pygame.K_w) and prisionero.rect.top > 0:
                    prisionero.rect.y -= prisionero.speed
                    prisionero.image = imagenes_prisionero['arriba']
                if (evento.key == pygame.K_DOWN or evento.key == pygame.K_s) and prisionero.rect.bottom < HEIGHT:
                    prisionero.rect.y += prisionero.speed
                    prisionero.image = imagenes_prisionero['abajo']
                if (evento.key == pygame.K_LEFT or evento.key == pygame.K_a) and prisionero.rect.left > 0:
                    prisionero.rect.x -= prisionero.speed
                    prisionero.image = imagenes_prisionero['izquierda']
                if (evento.key == pygame.K_RIGHT or evento.key == pygame.K_d) and prisionero.rect.right < WIDTH:
                    prisionero.rect.x += prisionero.speed
                    prisionero.image = imagenes_prisionero['derecha']

        #Obtener teclas presionadas
        keys = pygame.key.get_pressed()

        #Actualizar
        all_sprites.update(keys)
        if score > score_max:
            score_max = score

        # Verificar colisiones
        if verificar_colisiones(prisionero, enemigos):
            game_over(score)

        #Verificar si el prisionaero llega al final
        if prisionero.rect.top <= 0:
            prisionero.rect.center = (WIDTH // 2, HEIGHT - 50)  #Restaurar posición prisionero
            score += 10
            nivel += 1
            if nivel > 3:
                if score > score_max:
                    score_max = score
                pantalla_victoria(score)
                score = 0
                nivel = 1
            else:
                tiempo_transcurrido = (pygame.time.get_ticks() - iniciar_ticks) // 1000
                draw_text(screen, f"Tiempo: {tiempo_transcurrido}s", fuente, WHITE, 100, 10)
                score += max(0, 10 - tiempo_transcurrido)
                enemigos.empty()
                all_sprites.empty()
                all_sprites.add(prisionero)
                spawn_enemigos(enemigos, all_sprites, nivel)

        #Colocar la imagen de fondo de los niveles
        screen.blit(imagen_fondo, (0, 0))
        all_sprites.draw(screen)
        draw_text(screen, f"Puntuación: {score} | Nivel: {nivel}", fuente, WHITE, WIDTH // 2, 10)
        pygame.display.flip()


#Ejecutar el juego
if __name__ == "__main__":
    menu_principal()
    juego()