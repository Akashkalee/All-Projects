# Snake Game

A classic Snake game built with Python and Pygame.

## Description

This is a simple implementation of the classic Snake game where the player controls a snake that grows in length as it eats food. The game ends if the snake collides with the walls or itself.

## Features

- Snake movement in four directions
- Food spawning at random locations
- Score tracking
- Game over screen with restart option
- Start menu with play and quit buttons
- Pause functionality
- Distinct snake head visualization
- Game border display
- Multiple difficulty levels (Easy, Medium, Hard)
- Interactive buttons for game navigation

## Requirements

- Python 3.x
- Pygame library

## Installation

1. Make sure you have Python installed on your system.
2. Install the Pygame library:

```bash
pip install pygame
```

## How to Play

1. Run the game:

```bash
python snake_game.py
```

2. Start Menu:
   - Click the "Play" button or press 'S' to go to difficulty selection
   - Click the "Quit" button or press 'Q' to quit

3. Difficulty Selection:
   - Easy: Slower snake speed (beginner-friendly)
   - Medium: Default snake speed
   - Hard: Faster snake speed (challenging)

4. Controls:
   - Use the arrow keys (↑, ↓, ←, →) to control the direction of the snake
   - Press 'P' to pause the game
   - Eat the red food to grow the snake and increase your score
   - Avoid hitting the walls or the snake's own body

5. Pause Menu:
   - Press 'C' to continue
   - Press 'Q' to quit

6. Game Over:
   - Click "Play Again" to select difficulty and play again
   - Click "Quit" to exit the game

## Game Rules

- The snake starts with a length of 1
- Each time the snake eats food, it grows by one segment
- The game ends when the snake hits the wall or itself
- The score is equal to the number of food items eaten 