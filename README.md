I made this game for a school project, and decided to publish it because I think it's pretty cool. 
You can find the latest version <a href="[url](https://github.com/yorifant/Type_Pong/releases)">here</a>.
Follow the download instructions, and the game will be ready to play!

How to play the game:

    when the ball is coming towards you, there is a word on your left and right
    by repeating the first letter of the word on your left or right, you can move left / right.
        by typing the full word before the ball arrives at you, you hit the ball.
        -> however, once you started typing 1 word, you can't start the other one.
              if your pallet isn't in the right position, you miss the ball.
              if you didn't type the full word in time, you miss the ball.
    -> you gain 1 point if you hit the ball.
          you gain 2 points if you type the last letter between a narrow time window.
          -> this is indicated by the red exclamation mark
    -> you lose 1 HP if you miss the ball.

Some info about the game:
- It's written entirely in python.
- It uses the pygame engine.
- In total, it's about 550 lines (including the debug code, i could probably get it down to around 350 if i optimize it a bit, might do that in the future).
- It's entirely 2D, and uses a lot of math to get a 3D look.
- I used blender to get different angles of the pallet.
- No AI was used in any way to make the game.
- Made by Yoran Feys, aka yorifant.
