import random, time

# COMMANDLINE BLACKJACK
# WRITTEN BY BRANDON CROTTY
# 2023-12-20

# TODO:
# Add soft 11 aces
# Add splitting
# Add insurance

# Standard card deck. Key is the card name, value is the card's number value
DECK_TEMPLATE = {"A ♠": 1, "2 ♠": 2, "3 ♠": 3, "4 ♠": 4, "5 ♠": 5, "6 ♠": 6, "7 ♠": 7, # SPADES
                 "8 ♠": 8, "9 ♠": 9, "10♠": 10, "J ♠": 10, "Q ♠": 10, "K ♠": 10,
                 "A ♣": 1, "2 ♣": 2, "3 ♣": 3, "4 ♣": 4, "5 ♣": 5, "6 ♣": 6, "7 ♣": 7, # CLUBS
                 "8 ♣": 8, "9 ♣": 9, "10♣": 10, "J ♣": 10, "Q ♣": 10, "K ♣": 10,
                 "A ♦": 1, "2 ♦": 2, "3 ♦": 3, "4 ♦": 4, "5 ♦": 5, "6 ♦": 6, "7 ♦": 7, # DIAMONDS
                 "8 ♦": 8, "9 ♦": 9, "10♦": 10, "J ♦": 10, "Q ♦": 10, "K ♦": 10,
                 "A ♥": 1, "2 ♥": 2, "3 ♥": 3, "4 ♥": 4, "5 ♥": 5, "6 ♥": 6, "7 ♥": 7, # HEARTS
                 "8 ♥": 8, "9 ♥": 9, "10♥": 10, "J ♥": 10, "Q ♥": 10, "K ♥": 10}

chips = 100 # Starting chips
bet = 0 # Bet amount

# Print hand
def print_hand(hand):
    for x in range(len(hand)):
        print(hand[x][0], end=' ')
    print("\nTOTAL: " + str(countCards(hand)))

# Count cards - returns the total value of cards in the hand
def countCards(hand):
    score = 0
    for x in range(len(hand)): # Add total value of cards
        score += hand[x][1]
    return score

# Draw card - returns a random card from the temp deck as a tuple and removes it
def draw_card():
    time.sleep(0.5) # Add a slight delay for effect
    card = random.choice(list(deck.items())) # Get random card
    del deck[card[0]] # Remove that card from the deck
    return card

# Player's turn - returns their hand value or 0 if bust
def player(dealerFirstCard):
    player_hand = [] # List of card tuples
    global chips
    global bet
    firstTurn = True # Checks if it's the first turn for splits and doubling down
    isSplit = False
    isDouble = False

    # Place starting bet
    while True:
        print("How much would you like to bet?")
        print(f"You have {chips} chips")

        try:
            bet = int(input("> "))
            if bet > chips:
                print("You don't have enough chips")
            else:
                chips -= bet
                break
        except:
            print("Invalid input, try again")
            print()

    # Print first dealer card
    print("The dealer's first card is: ")
    print(dealerFirstCard[0])

    # Starting cards
    print("-- Your cards are: --")
    player_hand.append(draw_card())
    player_hand.append(draw_card())
    print_hand(player_hand)

    # Check for blackjack (doesn't do anything atm as soft 11 aces aren't integrated yet)
    # Show dealer's first card

    # Check for a split
    if (player_hand[0][0][0] == player_hand[1][0][0]):
        isSplit = True

    # Check if the player can double down
    if (bet <= chips):
        isDouble = True

    while True: # Main loop
        if countCards(player_hand) > 21: # Check if bust
            print("Bust!")
            return 0
        
        print("What would you like to do?")
        print("(h)it, (s)tand", end='')
        if isSplit & firstTurn: # Add split option
            print(", s(p)lit", end='')
        if isDouble & firstTurn: # Add double down option
            print(", (d)ouble down", end='')
        print()
        
        selection = input()
        if selection == 'h': # Hit
            player_hand.append(draw_card())
            print_hand(player_hand)
            firstTurn = False

        elif selection == 's': # Stand
            return (countCards(player_hand))
        
        elif (selection == 'p') & isSplit & firstTurn: # Split
            print("Sorry! This feature hasn't been implemented yet")

        elif (selection == 'd') & isDouble & firstTurn: # Double
            chips -= bet
            bet = bet * 2
            player_hand.append(draw_card())
            print_hand(player_hand)
            firstTurn = False
        
        else: # Unavailable / invalid option
            print("Invalid input, please try again")
     
# Dealer's turn: returns their hand value, or zero if bust
def dealer(dealerFirstCard):
    print("-- DEALER'S TURN --")
    dealer_hand = [] # List of card tuples
    dealer_score = 0
    dealer_hand.append(dealerFirstCard)

    while dealer_score < 17: # Draw cards until 17 or bust
        dealer_hand.append(draw_card())
        print_hand(dealer_hand)
        dealer_score = countCards(dealer_hand)

        if dealer_score > 21: # Bust
            print("Dealer's gone bust!")
            return 0
        
    return dealer_score

# New game
def new_game():
    global chips
    global bet
    global deck # Make a new deck for modification
    deck = DECK_TEMPLATE.copy()
    dealerFirstCard = draw_card() # First card for the dealer

    player_score =  player(dealerFirstCard)
    if player_score == 0: # Player went bust
        return
    
    dealer_score = dealer(dealerFirstCard)
    if dealer_score > player_score: # Lost to dealer
        print("Sorry, the dealer won :(")
    elif dealer_score == player_score: # Push
        print("Push! Your bet has been returned")
        chips += bet
    else:
        print(f"You won {bet} chips!")
        chips += bet * 2

print("#####################")
print("Welcome to the casino")
print("#####################")

# Main game loop
while True:
    if chips == 0: # Out of chips
        print("You've gone bust my good man")
        print("Thanks for playing")
        break
    
    else: 
        print("Enter 'n' to start a new game")
        print("Enter '0' to exit")

        selection = input()
        if selection == "0":
            break
        elif selection == "n":
            new_game()
        else:
            print("Invalid input, try again")