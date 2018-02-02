A simple word guessing game implemented in python.

Guess_game.py contains python code, words.txt contains words for game.

Allows the user to play the given hand, as follows:

1. The hand is displayed.
2. The user may input a word.
3. When any word is entered (valid or invalid), it uses up letters
   from the hand.
4. An invalid word is rejected, and a message is displayed asking
   the user to choose another word.
5. After every valid word: the score for that word is displayed,
   the remaining letters in the hand are displayed, and the user
   is asked to input another word.
6. The sum of the word scores is displayed when the hand finishes.
7. The hand finishes when there are no more unused letters.
8. The user can also finish playing the hand by inputing two 
   exclamation points (the string '!!') instead of a word.
   
Example gameplay:

Loading word list from file...
   83667 words loaded.

Enter n to deal a new hand, r to replay the last hand or e to end the game: n
o o t p l w * 

Enter a word or "!!" to indicate you are finished: pool
Score for pool : 168 .
Total Score is 168
t w * 

Enter a word or "!!" to indicate you are finished: w*t
Score for w*t : 105 .
Total Score is 273
Thankyou for playing, Your total score is 273

Enter n to deal a new hand, r to replay the last hand or e to end the game: r
o o t p l w * 

Enter a word or "!!" to indicate you are finished: !!
Thankyou for playing, Your total score is 0

Enter n to deal a new hand, r to replay the last hand or e to end the game: e
