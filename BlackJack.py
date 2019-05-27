import random
import os
clear = lambda: os.system('cls')

class Error(Exception):
	pass

class card:
	
	def __init__(self, suit, num):
		self.suit = suit
		self.num = num
		self.value = self.valuecalc()
	def valuecalc(self):
		if self.num == 'Jack' or self.num == 'Queen' or self.num == 'King':
			return 10
		elif self.num == 'Ace':
			return 1
		else:
			return int(self.num)
	def __str__(self):
		return self.num+' of '+self.suit

class deck:
	deckvalue = 0
	def __init__(self, list = []):
		self.decklist = list
	def add(self, card):
		self.decklist.append(card)
	def shuffledeck(self):
		random.shuffle(self.decklist)
	def deal(self):
		if len(self.decklist) == 0:
			print("No more cards are left in the deck!")
		else:
			return self.decklist.pop()
	def value_printer(self):
		self.value_printer_helper_sum()
		return self.deckvalue
	def value_printer_helper_sum(self):
		acecount = 0
		self.deckvalue = 0
		for item in self.decklist:
			self.deckvalue += item.value
			if item.num == 'Ace':
				acecount += 1
		while self.deckvalue <= 11 and acecount > 0:
			self.deckvalue += 10
	def hit(self,card):
		self.add(card)
	def stay(self):
		pass
	def dealer_print(self):
		mylist = []
		print("Dealer's Cards are: ",end='')
		for i in range(0,len(self.decklist)-1):
			mylist.append(str(self.decklist[i]))
		mylist.append('Flipped Down')
		print(', '.join(mylist))
	def player_print(self):
		mylist = []
		print("Player's Cards are: ",end='')
		for item in self.decklist:
			mylist.append(str(item))
		print(', '.join(mylist))
	def dealer_chance_print(self):
		mylist = []
		print("Dealer's Cards are: ",end='')
		for item in self.decklist:
			mylist.append(str(item))
		print(', '.join(mylist))
class Negative_Error(Error):
	pass

class bank:
	def __init__(self,balance):
		self.bet = 0
		self.balance = balance
	def betplacer(self):
		amt =0
		while True:
			try:
				amt = int(input("\nPls enter your bet amount: ")) 
				if amt<= self.balance:
					self.balance -= amt
					self.bet = amt
					break
				raise Negative_Error
			except:
				print("Bet amount greater than balance, Pls try again!")
				continue
	def win(self,amt):
		self.balance += amt
	def reset_bet(self):
		self.bet = 0


def doubledown(pdeck,ddeck,bank):
	pdeck.hit(ddeck.deal())


def split(deck):
	deck1 = deck([deck.decklist[0]])
	deck2 = deck([deck.decklist[1]])
	return deck1,deck2
def hit_or_stand():
	global playing
	print('\nChoices:\nEnter 1 to Hit\nEnter 2 to Stand\n')
	while True:
		try:
			choice = int(input("Your choice is: "))
			if choice not in [1,2]:
				raise Negative_Error
			if choice == 2:
				playing = False
			return choice
			break
		except:
			print("\nInvalid choice! Pls try again!")
			continue
while True:
		try:
			pinput = int(input('Enter the intial balance of the player: '))
			if pinput == 0:
				player_bank = bank(1000)
				break
			elif pinput > 0:
				player_bank = bank(pinput)
				break
			elif pinput < 0:
				raise Negative_Error
		except:
			print('Invalid Input, Pls try again!')
			continue
del pinput
ini = player_bank.balance
while True:
	#Print Opening Statement
	flag = True
	flag_res = True
	playing = True
	suitslist = ['Diamonds','Hearts','Spades','Clubs']
	valuelist = ['Ace','2','3','4','5','6','7','8','9','10','Jack','Queen','King']
	inputlist = []
	for suits in suitslist:
		for item in valuelist:
			inputlist.append(card(suits,item))
	dealdeck = deck(inputlist)	
	dealdeck.shuffledeck()
	# Enter the intial information about BlackJack
	
	dealer_bank = bank(1000000)
	print("Player's current balance is: $"+str(player_bank.balance))
	print("Player's current bet is: $"+str(player_bank.bet))
	player_bank.betplacer()
	clear()
	print("Player's current balance is: $"+str(player_bank.balance))
	print("Player's current bet is: $"+str(player_bank.bet))
	
	dealer_deck = deck([dealdeck.deal(),dealdeck.deal()])
	player_deck = deck([dealdeck.deal(),dealdeck.deal()])
	print()
	dealer_deck.dealer_print()
	print()
	player_deck.player_print()
	print("The value of player's deck is "+str(player_deck.value_printer()))
	while playing:
		if player_deck.value_printer() == 21:
				print("\nDealer has lost, The Player has won the bet!")
				flag = False
				player_bank.balance+=2*(player_bank.bet)
				player_bank.reset_bet()
				break
		choice = hit_or_stand()
		clear()
		if choice == 1:
			player_deck.hit(dealdeck.deal())
			dealer_deck.dealer_print()
			print()
			player_deck.player_print()
			print("The value of player's deck is "+str(player_deck.value_printer()))
			if player_deck.value_printer() == 21:
				print("\nDealer has lost, The Player has won the bet!")
				flag = False
				player_bank.balance+=2*(player_bank.bet)
				player_bank.reset_bet()
				break
			if player_deck.value_printer()>21:
				print('\nPlayer is busted, The Dealer has won the bet!')
				player_bank.reset_bet()
				flag = False
				break
	while dealer_deck.value_printer()<17 and flag:
		flag_res = False
		dealer_deck.hit(dealdeck.deal())
		print('The Dealer chose to hit')
		print()
		dealer_deck.dealer_chance_print()
		print("The value of dealer's deck is "+str(dealer_deck.value_printer())+'\n')
		player_deck.player_print()
		print("The value of player's deck is "+str(player_deck.value_printer()))
		if dealer_deck.value_printer()>21:
				print('\nDealer is busted, The Player has won the bet!')
				player_bank.balance+=2*(player_bank.bet)
				player_bank.reset_bet()
				break
		print()
	if flag_res and flag:
		dealer_deck.dealer_chance_print()
		print("The value of dealer's deck is "+str(dealer_deck.value_printer())+'\n')
		player_deck.player_print()
		print("The value of player's deck is "+str(player_deck.value_printer()))

		
	if (21 - dealer_deck.value_printer() < 21 - player_deck.value_printer()) and (dealer_deck.value_printer()<22 and player_deck.value_printer()<22) and flag:
		print('Player has lost, The Dealer has won the bet!')
		player_bank.reset_bet()
	elif (21 - dealer_deck.value_printer() > 21 - player_deck.value_printer()) and (dealer_deck.value_printer()<22 and player_deck.value_printer()<22) and flag:
		print('Dealer has lost, The Player has won the bet!')
		player_bank.balance+=2*(player_bank.bet)
		player_bank.reset_bet()
	elif (21 - dealer_deck.value_printer() == 21 - player_deck.value_printer()) and (dealer_deck.value_printer()<22 and player_deck.value_printer()<22) and flag:
		print("It's a push! No one won the bet!")
		player_bank.balance+=player_bank.bet
		player_bank.reset_bet()
	print("\nPlayer's current balance is: $"+str(player_bank.balance))
	if player_bank.balance == 0:
		print('Game Over! You are bankrupt!')
		break
	play_again = input("\nDo you want to play again? Yes or No: ")
	if play_again.lower() == 'no':
		if ini>player_bank.balance:
			print(f'\nYou have lost ${ini - player_bank.balance}!')
		elif ini<player_bank.balance:
			print(f'\nYou have won ${player_bank.balance - ini}!')
		else:
			print('\nYou have broke even!')
		break
	clear()
