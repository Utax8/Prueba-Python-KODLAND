# 🎮Prisoner Escape

**Prisoner Escape** es un videojuego tipo *arcade* con 3 niveles de dificultad desarrollado con Python y la biblioteca Pygame. Inspirado en el clásico "Frogger" de 1981. El objetivo del juego es ayudar a un prisionero a escapar de la prisión esquivando patrullas y autos en movimiento. ¡Cuantos más niveles completes, mayor será tu puntuación!

## 🕹️Juego
El jugador controla a un prisionero que debe cruzar carreteras llenas de vehículos en movimiento. Cada vez que logra llegar a la parte superior de la pantalla ganas puntos y avanzas de nivel. A medida que avanzas de nivel la dificultad aumenta con más enemigos y mayor velocidad.

### Características principales

- 🎨 Gráficos con sprites personalizados
- 🎵 Música de fondo
- 🛑 Menú de pausa interactivo
- 💀 Pantalla de "Game Over" al perder
- 🏆 Pantalla de victoria al ganar
- 📈 Sistema de puntuación y 3 niveles de dificultad

## 🎮 Controles
- **SPACE / ESPACIO:** Iniciar el juego
- **Flechas ⬆️⬇️⬅️➡️  / WASD:** Mover al prisionero
- **P:** Pausar el juego
- **R:** Reiniciar (en pantalla de Game Over o Victoria)
- **ESC / Q:** Salir del juego

## 🧱 Clases
- **Prisionero:** Esta clase maneja los sprites del prisionero, además contiene la función que permite moverse en las 4 direcciones principales (arriba, abajo, izquierda, derecha).
- **Enemigos:** Esta clase se encarga del spawn de los enemigos, Representa a los vehículos enemigos en las distintas filas, además contiene la función de actualización que se mueve a los enemigos continuamente en pantalla y los reinicia al salir del borde.

## 🧠 Funciones
- **mover:** Esta función se encarga del movimiento del personaje en las distintas direcciones (arriba, abajo, izquierda, derecha).
- **update:** Esta función dentro de la clase de enemigos se encarga de mover a los enemigos continuamente en pantalla.
- **spawn_enemigos:** Esta función se encarga de generar enemigos aleatorios en filas específicas según el nivel que se este jugando.
- **draw_text:** Esta función es la encarga de mostrar los mensajes que aparecen en la pantalla.
- **draw_button:** Dibuja botones interactivos en el menú de pausa.
- **check_collision:** Esta función detecta las colisiones entre el prisionero y los enemigos.
- **juego:** Contiene el bucle principal del juego, además de gestionar el movimiento, colisiones y niveles.

## 🖥️ Menús / Pantallas:
- **Menú Principal**: Contiene la imagen principal del juego permitiendo iniciarlo con la tecla `SPACE` ó salir con la tecla `ESC`.
- **Menú Pausa**: Se activa oprimiendo la tecla  `P` eincluye opciones para:
  - Reanudar juego
  - Activar/desactivar música
  - Reiniciar partida
  - Salir del juego
- **Pantalla de Game Over**: Contiene la puntuación final y permite reiniciar con el juego oprimiendo la tecla `R`.
- **Pantalla de Victoria**: Muestra la puntuación final tras superar todos los niveles y permite ya sea salir del juego con la tecla `R` o volver a al menu principal con la tecla `R`.

## ⚙️ Requisitos

- Python 3
- La libreria de Pygame
En caso de no tener la libreria de Pygame se puede instalar ejecutando:

```bash
pip install pygame
```

## Cómo ejecutar
1. **Clonar este repositorio**
2. Instalar las dependencias necesarias.
3. Ejecutar el codigo desde un editor de codigo como Visual Studio Code o abrir la terminal en la dirección en la que se encuentra el archivo y ejecutarlo con el comando `python game.py`.
