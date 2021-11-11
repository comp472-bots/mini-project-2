# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python

import time

class Game:
	MINIMAX = 0
	ALPHABETA = 1
	HUMAN = 2
	AI = 3
	
	def __init__(self, recommend = True):
		
		self.initialize_game()
		self.get_parameters()
		self.recommend = recommend
	
	def get_board_size(self):
		while True: 
			try:
				self.board_size = int(input("Enter size of board in range 3-10: "))
			except ValueError: 
				print ("That's not a number!")
				continue
			else:
				
				if  3 <= self.board_size <= 10:
					return
				else:
					print ("Out of range... Try again!")
	
	def get_bloc_amount(self):
		while True: 
			try:
				self.bloc_amount = int(input(("Enter number of blocs in range 0-{range}: ").format(range = 2 * self.board_size)))
			except ValueError: 
				print ("That's not a number!")
				continue
			else:
				if  0 <= self.bloc_amount <= 2 * self.board_size:
					return
				else:
					print ("Out of range... Try again!")
	
	def is_valid(self, px, py):
		if px < 0 or px > self.board_size-1 or py < 0 or py > self.board_size-1:
			return False
		elif self.current_state[px][py] != '.':
			return False
		else:
			return True
	
	def get_bloc_positions(self):
		for i in range(self.bloc_amount):
			
			while True:

				px = int(input(F'enter the row number of bloc {i} (0-{self.board_size-1}) : '))
				py = ord(input(F'enter the column letter of bloc {i} (A-{chr(self.board_size + 64)}) : ')) - 65

				if self.is_valid(px, py):
					self.current_state[px][py] = '+'
					break
				else:
					print('The position is not valid! Try again.')
			
					
	def get_lineup_size(self):
		while True: 
			try:
				self.lineup_size = int(input(("Enter winning line-up size in range 3-{range}: ").format(range = self.board_size)))
			except ValueError: 
				print ("That's not a number!")
				continue
			else:
				if  3 <= self.lineup_size <= self.board_size:
					return
				else:
					print ("Out of range... Try again!")

	def get_max_depth_p1(self):
		while True: 
			try:
				self.max_depth_p1 = int(input("Enter maximum depth of adversarial search for player 1: "))
			except ValueError: 
				print ("That's not a number!")
				continue
			else:
				if  1 <= self.max_depth_p1:
					return
				else:
					print ("Out of range... Try again!")
	
	def get_max_depth_p2(self):
		while True: 
			try:
				self.max_depth_p2 = int(input("Enter maximum depth of adversarial search for player 2: "))
			except ValueError: 
				print ("That's not a number!")
				continue
			else:
				if  1 <= self.max_depth_p2:
					return
				else:
					print ("Out of range... Try again!")
	
	def get_max_allowed_time(self):
		while True: 
			try:
				self.max_allowed_time = int(input("Enter maximum allowed time for program to make a move: "))
			except ValueError: 
				print ("That's not a number!")
				continue
			else:
				if  1 <= self.max_allowed_time:
					return
				else:
					print ("Out of range... Try again!")
	
	def get_search_type(self):
		while True: 
			try:
				self.search_type = int(input("Enter (1) to use alphabeta, enter (0) to use minimax: "))
			except ValueError: 
				print ("That's not a number!")
				continue
			else:
				if  (self.search_type == 0) or (self.search_type == 1):
					return
				else:
					print ("Incorrect value... Try again!")
	
	def get_play_mode(self):
		while True:
			try:
				self.play_mode = int(input("Enter (1) to use H-H, \n enter (2) to use H-AI, \n enter (3) to use AI-H, \n enter (4) to use AI-AI: "))
			except ValueError: 
				print ("That's not a number!")
				continue
			else:
				if  self.play_mode == 1:
					self.player_x = self.HUMAN
					self.player_o = self.HUMAN
					return
				elif self.play_mode == 2:
					self.player_x = self.HUMAN
					self.player_o = self.AI
					return
				elif self.play_mode == 3:
					self.player_x = self.AI
					self.player_o = self.HUMAN
					return
				elif self.play_mode == 4:
					self.player_x = self.AI
					self.player_o = self.AI
					return
				else:
					print ("Incorrect value... Try again!")
	

	def get_parameters(self):
		
		self.get_bloc_amount()
		self.get_bloc_positions()
		self.get_lineup_size()
		self.get_max_depth_p1()
		self.get_max_depth_p2()
		self.get_max_allowed_time()
		self.get_search_type()
		self.get_play_mode()
		
		
	def initialize_game(self):
		
		self.get_board_size()
		self.current_state = [["." for i in range(self.board_size)] for i in range(self.board_size)]
		self.last_move = (None, None)
		print(self.current_state)
		# Player X always plays first
		self.player_turn = 'X'

	def draw_board(self):
		print()
		for x in range(0, self.board_size):
			for y in range(0, self.board_size):
				print(F'{self.current_state[x][y]}', end=" ")
			print()
		print()

	def is_end(self):
		if self.last_move == (None, None):
			return None

		row, col = self.last_move
		item = self.current_state[row][col]
		rows = len(self.current_state)
		cols = len(self.current_state[0])

		for delta_row, delta_col in [(1, 0), (0, 1), (1, 1), (1, -1)]:
			consecutive_items = 1
			for delta in (1, -1):
				delta_row *= delta
				delta_col *= delta
				next_row = row + delta_row
				next_col = col + delta_col

				while 0 <= next_row < rows and 0 <= next_col < cols:
					if self.current_state[next_row][next_col] == item:
						consecutive_items += 1
					else:
						break
					if consecutive_items == self.lineup_size:
						return self.current_state[next_row][next_col]
					next_row += delta_row
					next_col += delta_col

		# Is whole board full?
		for i in range(0, rows):
			for j in range(0, cols):
				# There's an empty field, we continue the game
				if (self.current_state[i][j] == '.'):
					return None

		# It's a tie!
		return '.'

	def check_end(self):
		self.result = self.is_end()
		# Printing the appropriate message if the game has ended
		if self.result != None:
			if self.result == 'X':
				print('The winner is X!')
			elif self.result == 'O':
				print('The winner is O!')
			elif self.result == '.':
				print("It's a tie!")
			self.initialize_game()
		return self.result

	def input_move(self):
		while True:
			print(F'Player {self.player_turn}, enter your move:')
			# px = int(input('enter the x coordinate: '))
			# py = int(input('enter the y coordinate: '))

			px = int(input(F'enter the row number (0-{self.board_size-1}) : '))
			py = ord(input(F'enter the column letter (A-{chr(self.board_size + 64)}) : ')) - 65
			print(py)

			if self.is_valid(px, py):
				return (px,py)
			else:
				print('The move is not valid! Try again.')

	def switch_player(self):
		if self.player_turn == 'X':
			self.player_turn = 'O'
		elif self.player_turn == 'O':
			self.player_turn = 'X'
		return self.player_turn

	def minimax(self, max=False):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		value = 2
		if max:
			value = -2
		x = None
		y = None
		result = self.is_end()
		if result == 'X':
			return (-1, x, y)
		elif result == 'O':
			return (1, x, y)
		elif result == '.':
			return (0, x, y)
		# if time > alloted
		# return
		for i in range(0, 3):
			for j in range(0, 3):
				temp = self.last_move
				self.last_move = (i, j)
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						(v, _, _) = self.minimax(max=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						(v, _, _) = self.minimax(max=True)
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
					self.last_move = temp
		return (value, x, y)

	def alphabeta(self, alpha=-2, beta=2, max=False):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		value = 2
		if max:
			value = -2
		x = None
		y = None
		result = self.is_end()
		if result == 'X':
			return (-1, x, y)
		elif result == 'O':
			return (1, x, y)
		elif result == '.':
			return (0, x, y)
		for i in range(0, 3):
			for j in range(0, 3):
				if self.current_state[i][j] == '.':
					if max:
						self.current_state[i][j] = 'O'
						(v, _, _) = self.alphabeta(alpha, beta, max=False)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						(v, _, _) = self.alphabeta(alpha, beta, max=True)
						if v < value:
							value = v
							x = i
							y = j
					self.current_state[i][j] = '.'
					if max: 
						if value >= beta:
							return (value, x, y)
						if value > alpha:
							alpha = value
					else:
						if value <= alpha:
							return (value, x, y)
						if value < beta:
							beta = value
		return (value, x, y)
	'''
	def play(self,algo=None,player_x=None,player_o=None):
		if algo == None:
			algo = self.ALPHABETA
		if player_x == None:
			player_x = self.HUMAN
		if player_o == None:
			player_o = self.HUMAN
		while True:
			self.draw_board()
			if self.check_end():
				return
			start = time.time()
			if algo == self.MINIMAX:
				if self.player_turn == 'X':
					(_, x, y) = self.minimax(max=False)
				else:
					(_, x, y) = self.minimax(max=True)
			else: # algo == self.ALPHABETA
				if self.player_turn == 'X':
					(m, x, y) = self.alphabeta(max=False)
				else:
					(m, x, y) = self.alphabeta(max=True)
			end = time.time()
			if (self.player_turn == 'X' and player_x == self.HUMAN) or (self.player_turn == 'O' and player_o == self.HUMAN):
					if self.recommend:
						print(F'Evaluation time: {round(end - start, 7)}s')
						print(F'Recommended move: x = {x}, y = {y}')
					(x,y) = self.input_move()
			if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
						print(F'Evaluation time: {round(end - start, 7)}s')
						print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
			self.current_state[x][y] = self.player_turn
			self.switch_player()
	'''	

	def play(self):
		
		while True:
			self.draw_board()
			if self.check_end():
				return
			start = time.time()
			if self.search_type == self.MINIMAX:
				if self.player_turn == 'X':
					(_, x, y) = self.minimax(max=False)
				else:
					(_, x, y) = self.minimax(max=True)
			else: # search_type == self.ALPHABETA
				if self.player_turn == 'X':
					(m, x, y) = self.alphabeta(max=False)
				else:
					(m, x, y) = self.alphabeta(max=True)
			end = time.time()
			if (self.player_turn == 'X' and self.player_x == self.HUMAN) or (self.player_turn == 'O' and self.player_o == self.HUMAN):
					if self.recommend:
						print(F'Evaluation time: {round(end - start, 7)}s')
						print(F'Recommended move: x = {x}, y = {y}')
					(x,y) = self.input_move()
			if (self.player_turn == 'X' and self.player_x == self.AI) or (self.player_turn == 'O' and self.player_o == self.AI):
						print(F'Evaluation time: {round(end - start, 7)}s')
						print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
			self.current_state[x][y] = self.player_turn
			self.last_move = (x, y)
			print(self.last_move)
			self.switch_player()

def main():
	g = Game(recommend=False)
	g.play()
	# g.play(player_x=Game.AI,player_o=Game.HUMAN)

if __name__ == "__main__":
	main()

