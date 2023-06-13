import time
import pygame
import numpy as np

COLOR_BG = (10, 10, 10)  # Very Dark Grey
COLOR_GRID = (40, 40, 40)  # Dark Grey
COLOR_FOOD = (223, 27, 27)  # Red
COLOR_SNAKE = (255, 255, 255)  # Pure White
NEW_BLOCK = (27, 223, 27)  # Green

cells = np.zeros((60, 60))
foodPos = np.array([45, 35])


def buildSnake(Length):
    strt = 20
    snake = np.array([(strt, 10, 'U')], dtype='object')
    while(Length > 0):
        strt = strt + 1
        block = np.array([(strt, 10, 'U')], dtype='object')
        snake = np.append(snake, block, 0)
        Length = Length - 1
    return snake

def checkKeyPress(event, defMoveDirection,  running):
    moveDirection = defMoveDirection
    if event.key == pygame.K_SPACE:
        running = not running
    elif event.key == pygame.K_LEFT:
        moveDirection = 'L'
    elif event.key == pygame.K_UP:
        moveDirection = 'U'
    elif event.key == pygame.K_RIGHT:
        moveDirection = 'R'
    elif event.key == pygame.K_DOWN:
        moveDirection = 'D'
    return (moveDirection, running)

def generateFoodPos(snake):
    while(1):
        randPos = np.random.randint(60, size=(2))
        overlap = False
        for idx in range(0, len(snake)):
            if (randPos[0] == snake[idx, 0] and randPos[1] == snake[idx, 1]):
                overlap = True
                break
        if overlap == False:
            foodPos[0] = randPos[0]
            foodPos[1] = randPos[1]
            break
def update(screen, size, moveDirection, origSnake):
    updated_snake = np.copy(origSnake)

    # Valid new Move Direction
    if (moveDirection == 'R' and origSnake[0][2] == 'L') or (moveDirection == 'D' and origSnake[0][2] == 'U') or (
            moveDirection == 'L' and origSnake[0][2] == 'R') or (moveDirection == 'U' and origSnake[0][2] == 'D'):
        moveDirection = origSnake[0, 2]

    # Update for the head of the snake
    if moveDirection == 'L':
        updated_snake[0, 1] = (updated_snake[0, 1] - 1) if updated_snake[0, 1] > 0 else (cells.shape[1] - 1)
    elif moveDirection == 'U':
        updated_snake[0, 0] = (updated_snake[0, 0] - 1) if int(updated_snake[0, 0]) > 0 else (cells.shape[0] - 1)
    elif moveDirection == 'R':
        updated_snake[0, 1] = (updated_snake[0, 1] + 1) if updated_snake[0, 1] < cells.shape[1] else 0
    elif moveDirection == 'D':
        updated_snake[0, 0] = (updated_snake[0, 0] + 1) if updated_snake[0, 0] < cells.shape[0] else 0

    updated_snake[0, 2] = moveDirection

    # check if the snake has bitten itself
    for idx in range(1, len(origSnake)):
        if (updated_snake[0, 0] == origSnake[idx, 0]) and (updated_snake[0, 1] == origSnake[idx, 1]):
            updated_snake = np.delete(updated_snake, [range(idx, len(origSnake))], 0)
            break

    # update for the rest of the body of the snake (except for the head block)
    for idx in range(1, len(updated_snake)):
        if origSnake[idx-1, 2] == 'L':
            updated_snake[idx, 1] = (updated_snake[idx, 1] - 1) if updated_snake[idx, 1] > 0 else (cells.shape[1] - 1)
        elif origSnake[idx-1, 2] == 'U':
            updated_snake[idx, 0] = (updated_snake[idx, 0] - 1) if updated_snake[idx, 0] > 0 else (cells.shape[0] - 1)
        elif origSnake[idx-1, 2] == 'R':
            updated_snake[idx, 1] = (updated_snake[idx, 1] + 1) if updated_snake[idx, 1] < cells.shape[1] else 0
        elif origSnake[idx-1, 2] == 'D':
            updated_snake[idx, 0] = (updated_snake[idx, 0] + 1) if updated_snake[idx, 0] < cells.shape[0] else 0
        updated_snake[idx, 2] = origSnake[idx-1, 2]

    # Check if the food has been eaten
    ateFood = False
    if (updated_snake[0, 0] == foodPos[0]) and (updated_snake[0, 1] == foodPos[1]):
        lastBlockIdx = len(updated_snake) - 1
        lastBlockDir = updated_snake[lastBlockIdx, 2]
        rowNew = 0
        colNew = 0
        if lastBlockDir == 'L':
            rowNew = updated_snake[lastBlockIdx, 0]
            colNew = (updated_snake[lastBlockIdx, 1] + 1) if updated_snake[lastBlockIdx, 1] < cells.shape[1] else (cells.shape[1] - 1)
        elif lastBlockDir == 'U':
            rowNew = (updated_snake[lastBlockIdx, 0] + 1) if updated_snake[lastBlockIdx, 0] < cells.shape[0] else (cells.shape[0] - 1)
            colNew = updated_snake[lastBlockIdx, 1]
        elif lastBlockDir == 'R':
            rowNew = updated_snake[lastBlockIdx, 0]
            colNew = (updated_snake[lastBlockIdx, 1] - 1) if updated_snake[lastBlockIdx, 1] > 0 else 0
        elif lastBlockDir == 'D':
            rowNew = (updated_snake[lastBlockIdx, 0] - 1) if updated_snake[lastBlockIdx, 0] > 0 else 0
            colNew = updated_snake[lastBlockIdx, 1]

        addBlock = np.array([(rowNew, colNew, lastBlockDir)], dtype='object')
        updated_snake = np.append(updated_snake, addBlock, 0)
        generateFoodPos(updated_snake)
        ateFood = True

    # Fill the grid
    for row, col in np.ndindex(cells.shape):
        color = COLOR_BG
        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))

    # Fill the Snake
    for idx in range(len(updated_snake)):
        color = COLOR_SNAKE
        if idx == len(updated_snake) - 1 and ateFood == True:
            color = NEW_BLOCK
        row = updated_snake[idx, 0]
        col = updated_snake[idx, 1]
        pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))

    #Fill the Food
    color = COLOR_FOOD
    row = foodPos[0]
    col = foodPos[1]
    pygame.draw.rect(screen, color, (col * size, row * size, size - 1, size - 1))

    return updated_snake


def main():
    size = 15
    screen = pygame.display.set_mode((60 * size, 60 * size))
    moveDirection = 'U'
    snake = buildSnake(10)
    screen.fill(COLOR_GRID)
    snake = update(screen, size, moveDirection, snake)
    pygame.display.flip()
    pygame.display.update()

    running = True

    while True:
        screen.fill(COLOR_GRID)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            elif event.type == pygame.KEYDOWN:
                (moveDirection, running) = checkKeyPress(event, moveDirection, running)
        if running:
            snake = update(screen, size, moveDirection, snake)
            pygame.display.update()

        time.sleep(0.05)


if __name__ == '__main__':
    main()
