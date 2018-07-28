import curses
from curses import KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT
import random as rand

def game():
    #initialize a window
    curses.initscr()
    curses.noecho()  
    curses.cbreak()
    curses.curs_set(0)

    #create a new window inside the current window with the required dimensions
    length = 25
    width = 60
    win = curses.newwin(length, width, 0, 0)
    win.keypad(True)
    win.nodelay(1)

    #initialize the game with food and snake's initial coordinates and direction
    key = KEY_RIGHT
    food = [10, 20]
    snake = [[4, 10], [4, 9], [4, 8]]
    win.addch(food[0], food[1], '*')
    score = 0

    while key != 27:
        win.border(0)
        win.addstr(0, 2, 'Score : ' + str(score) + ' ')                # Printing 'Score'
        win.addstr(0, 27, ' SNAKE ')
        win.timeout(int(150 - (len(snake)/5 + len(snake)/10)%120))
        prevKey = key

        event = win.getch()
        key = key if event == -1 else event

        if key == ord(' '):                         #if the user clicks spacebar pause the game
            win.addstr(0, 27, ' SNAKE: PAUSED ')
            while True:
                event = win.getch()
                if event == ord(' '):
                    win.addstr(0, 27, ' SNAKE ')
                    key = prevKey
                    break

        #if key press is not a valid input reset key to prevKey
        if key not in [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT, 27]:
            key = prevKey

        #determine the next location of snake's head based on key's value
        snake.insert(0, [snake[0][0] + ((key == KEY_DOWN and 1) or (key == KEY_UP and -1)), snake[0][1] + ((key == KEY_LEFT and -1) or (key == KEY_RIGHT and 1))])

        #if the snake bites itself, GAME OVER!
        if snake[0] in snake[1:]:
            print("Oh no! You bit yourself")
            print("GAME OVER!")
            break

        #if the snake touches the boundary, GAME OVER! Comment out the below code for this functionality
        # if snake[0][0] in [0, length] or snake[0][1] in [0, width]:
        #     print("GAME OVER!")
        #     break 

        #if the snake goes to the boundaries re-enter it from other end
        if snake[0][0] == 0: snake[0][0] = length - 1
        if snake[0][0] == length - 1: snake[0][0] = 1
        if snake[0][1] == 0: snake[0][1] = width - 1
        if snake[0][1] == width - 1: snake[0][1] = 1
        
        if snake[0] == food: #if the snake eats food, create food at some other random location
            score += 1
            food = []
            while food == []:
                food = [rand.randint(2, length - 2), rand.randint(2, width - 2)]
                if food in snake: food = []
            win.addch(food[0], food[1], '*')
        else:
            last = snake.pop() #if the food is not eaten, pop the last block off the snake
            win.addch(last[0], last[1], ' ')
        win.addch(snake[0][0], snake[0][1], '#')
    if key == 27: print('Exited game!')
    print('Score:', score)
    curses.echo()
    curses.nocbreak()
    curses.endwin()

print('starting game....')
game()