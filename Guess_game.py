import math
import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
   '*': 0, 'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}


WORDLIST_FILENAME = "words.txt"

def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.append(line.strip().lower())
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def get_frequency_dict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq
	

def get_word_score(word, n):
    """
    Returns the score for a word. Assumes the word is a
    valid word.

    You may assume that the input word is always either a string of letters, 
    or the empty string "". You may not assume that the string will only contain 
    lowercase letters, so you will have to handle uppercase and mixed case strings 
    appropriately. 

	The score for a word is the product of two components:

	The first component is the sum of the points for letters in the word.
	The second component is the larger of:
            1, or
            7*wordlen - 3*(n-wordlen), where wordlen is the length of the word
            and n is the hand length when the word was played

	Letters are scored as in Scrabble; A is worth 1, B is
	worth 3, C is worth 3, D is worth 2, E is worth 1, and so on.

    word: string
    n: int >= 0
    returns: int >= 0
    """
    word=word.lower()
    comp1=0
    for ch in word:
        comp1+=SCRABBLE_LETTER_VALUES[ch]
    comp2=1
    t=7*len(word)-3*(n-len(word))
    if(t>comp2):
        comp2=t
    return comp1*comp2
    
    
def display_hand(hand):
    """
    Displays the letters currently in the hand.

    For example:
       display_hand({'a':1, 'x':2, 'l':3, 'e':1})
    Should print out something like:
       a x x l l l e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    
    for letter in hand.keys():
        for j in range(hand[letter]):
             print(letter, end=' ')      # print all on the same line
    print()                              # print an empty line

def deal_hand(n):
    """
    Returns a random hand containing n lowercase letters.
    ceil(n/3) letters in the hand should be VOWELS (note,
    ceil(n/3) means the smallest integer not less than n/3).

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    
    hand={}
    num_vowels = int(math.ceil(n / 3))
    for i in range(num_vowels):
        x = random.choice(VOWELS)
        hand[x] = hand.get(x, 0) + 1
    
    for i in range(num_vowels, n):    
        x = random.choice(CONSONANTS)
        hand[x] = hand.get(x, 0) + 1
        
    c=0
    for ch in VOWELS:
        for x in hand:
            if ch==x:
                hand[x] = hand.get(x)-1
                if hand[x] < 0:
                    hand[x] = 0
                hand['*'] = hand.get('*',0)+1
                c=1
                break
        if c==1:
            break
    
    return hand

def update_hand(hand, word):
    """
    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    
    new_hand=hand.copy()
    word=word.lower()
    for letter in word:
        for key in new_hand:
            if letter is key:
                new_hand[key]=new_hand.get(letter) -1
                if new_hand[key] < 0:
                    new_hand[key]=0
    return new_hand


def is_valid_word(word, hand, word_list):
    """
    Returns True if word is in the word_list and is entirely
    composed of letters in the hand. Otherwise, returns False.
    Does not mutate hand or word_list.
   
    word: string
    hand: dictionary (string -> int)
    word_list: list of lowercase strings
    returns: boolean
    """
    
    word_copy=word.lower()
    hand_copy=hand.copy()
    s = word_copy.find('*')
    if s!=-1:
        word_pos=[]
        for x in VOWELS:
            wrd = word_copy[:s] + x + word_copy[s+1:len(word_copy)]
            word_pos.append(wrd)
    else:
        word_pos=[word_copy]
    #word_pos=[word_copy]  
    
    for word_lst in word_list:
        word_lst=word_lst.lower()
        for wrd in word_pos:
            if wrd==word_lst:
                for ch in wrd:
                    hand_copy[ch] = hand_copy.get(ch,0) -1
                    if hand_copy[ch] < 0 and ch in VOWELS and s!=-1:
                        continue
                    elif hand_copy[ch] < 0:
                        return False
                return True
            
            
def calculate_handlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    c=0
    for x in hand:
        c+=hand.get(x)
    
    return c  

def play_hand(hand, word_list):

    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    
    * The user may input a word.

    * When any word is entered (valid or invalid), it uses up letters
      from the hand.

    * An invalid word is rejected, and a message is displayed asking
      the user to choose another word.

    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.

    * The sum of the word scores is displayed when the hand finishes.

    * The hand finishes when there are no more unused letters.
      The user can also finish playing the hand by inputing two 
      exclamation points (the string '!!') instead of a word.

      hand: dictionary (string -> int)
      word_list: list of lowercase strings
      returns: the total score for the hand
      
    """
    # Keep track of the total score
    score=0
    # As long as there are still letters left in the hand:
    while calculate_handlen(hand)>1:
        
        display_hand(hand)
        # Display the hand
        
        user_input = str(input('Enter a word or "!!" to indicate you are finished: '))
        # Ask user for input
        
        if user_input=="!!":
        # If the input is two exclamation points:
            break
            # End the game (break out of the loop)

        else:
        # Otherwise (the input is not two exclamation points):
            if is_valid_word(user_input, hand, word_list):
            # If the word is valid:
                n=len(user_input)
                cur_score=get_word_score(user_input, n)
                score+=cur_score
                print('Score for', user_input, ':',cur_score, '.\nTotal Score is',score)
                # Tell the user how many points the word earned,
                # and the updated total score
                
            if not is_valid_word(user_input, hand, word_list):
                
                print ("Invalid word, please try again.")
            # Otherwise (the word is not valid):
                # Reject invalid word (print a message)
                
            hand=update_hand(hand, user_input)
            # update the user's hand by removing the letters of their inputted word
            
    print('Thankyou for playing, Your total score is', score)
    
def play_game(word_list):
    """
    Allow the user to play a series of hands

    * Asks the user to input a total number of hands

    * Accumulates the score for each hand into a total score for the 
      entire series
 
    * For each hand, ask the user if they would like to replay the hand.
      
    * Returns the total score for the series of hands

    word_list: list of lowercase strings
    """
    
    user_input=''
    stored_hand=None
    
    while True:
        user_input = input('Enter n to deal a new hand, r to replay the last hand or e to end the game: ')
        
        if user_input == 'n':
            stored_hand=deal_hand(HAND_SIZE)
            play_hand(stored_hand,word_list)
        elif user_input=='r':
            if stored_hand == None:
                print("You haven't played a hand yet!  Please play a new hand first.")
            else:
                play_hand(stored_hand, word_list)
        elif user_input=='e':
            break
        else:
            print('Invalid Input')
if __name__ == '__main__':
    word_list = load_words()
    play_game(word_list)
