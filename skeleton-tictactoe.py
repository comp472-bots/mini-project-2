# based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python

import time
import random
import sys

class Game:
	MINIMAX = 0
	ALPHABETA = 1
	HUMAN = 2
	AI = 3

	INFINITY = 10**14
	MAX = 10**12
	MIN = -10**12
	
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
					self.current_state[px][py] = '*'
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
		self.generate_chance_matrix()
		self.last_move = (None, None)
		self.total_moves = 0
		self.heuristic_score = 0
		print(self.current_state)
		# Player X always plays first
		self.player_turn = 'X'

	def draw_board(self):
		
		print(F'(move #{self.total_moves})')

		print("   ", end=" ")
		for x in range(1, self.board_size+1):
			print(chr(x + 64),"", end="")

		print("\n  + ",end="")
		for x in range(0, self.board_size):
			print("-","", end="")

		print()
		for x in range(0, self.board_size):
			print(x, "|", end=" ")
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

		possible_moves = (self.board_size * self.board_size) - self.bloc_amount
		if possible_moves == self.total_moves:
			return "."

		return None

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

	def e1(self, max):
		if self.last_move == (None, None):
			return None

		row, col = self.last_move
		item = self.current_state[row][col]
		rows = self.board_size
		cols = self.board_size

		score = 0
		for delta_row, delta_col in [(1, 0), (0, 1), (1, 1), (1, -1)]:
			consecutive_items = 1
			open_positions = 0
			stop = False
			for delta in (1, -1):
				delta_row *= delta
				delta_col *= delta
				next_row = row + delta_row
				next_col = col + delta_col

				while (0 <= next_row < rows) and (0 <= next_col < cols) and (not stop):
					if self.current_state[next_row][next_col] == item:
						consecutive_items += 1
					elif self.current_state[next_row][next_col] == '.':
						open_positions += 1
					else:
						break
					if (consecutive_items + open_positions) == self.lineup_size:
						# score += 1
						score += consecutive_items**6
						stop = True
						break
					next_row += delta_row
					next_col += delta_col

				if stop:
					break

		return score if max else -score

	def e2(self, max):

		rows = self.board_size
		cols = self.board_size

		score = 0

		for row in range(rows):
			for col in range(cols):
				item = self.current_state[row][col]
				if item == 'X' or item == 'O':
					for delta_row, delta_col in [(1, 0), (0, 1), (1, 1), (1, -1)]:
						consecutive_items = 1
						open_positions = 0
						stop = False
						for delta in (1, -1):
							delta_row *= delta
							delta_col *= delta
							next_row = row + delta_row
							next_col = col + delta_col

							while (0 <= next_row < rows) and (0 <= next_col < cols) and (not stop):
								if self.current_state[next_row][next_col] == item:
									consecutive_items += 1
								elif self.current_state[next_row][next_col] == '.':
									open_positions += 1
								else:
									break
								if (consecutive_items + open_positions) == self.lineup_size:
									if (item == 'X'):
										score -= 1
									elif (item == 'O'):
										score += 1
									
									stop = True
									break
								next_row += delta_row
								next_col += delta_col

							if stop:
								break

		return score

	def e3(self, max):

		rows = self.board_size
		cols = self.board_size

		score = 0

		for row in range(rows):
			for col in range(cols):
				item = self.current_state[row][col]
				if item == 'X' or item == 'O':
					for delta_row, delta_col in [(1, 0), (0, 1), (1, 1), (1, -1)]:
						consecutive_items = 1
						open_positions = 0
						stop = False
						for delta in (1, -1):
							delta_row *= delta
							delta_col *= delta
							next_row = row + delta_row
							next_col = col + delta_col

							while (0 <= next_row < rows) and (0 <= next_col < cols) and (not stop):
								if self.current_state[next_row][next_col] == item:
									consecutive_items += 1
								elif self.current_state[next_row][next_col] == '.':
									open_positions += 1
								else:
									break
								if (consecutive_items + open_positions) == self.lineup_size:
									if (item == 'X'):
										score -= 10**(consecutive_items)
									elif (item == 'O'):
										score += 10**(consecutive_items)
									
									stop = True
									break
								next_row += delta_row
								next_col += delta_col

							if stop:
								break

		return score

	def generate_chance_matrix(self):

		rows = self.board_size
		cols = self.board_size

		self.chance_matrix = [[None for i in range(self.board_size)] for i in range(self.board_size)]

		for row in range(rows):
			for col in range(cols):
				
				row_diff =  abs(((rows-1)/2) - row)
				col_diff = abs(((cols-1)/2) - col)

				max_value = 1/(max(row_diff,col_diff)+1)
				self.chance_matrix[row][col] = int(max_value*100)
				
		print()
		for row in range(rows):
			for col in range(cols):
				print(F'{self.chance_matrix[row][col]}', end=" ")
			print()
		print()
		
	
	#def e2(self):

		#for i in range(0, self.board_size):
		
		#score = 0




		#for i in range(0,4):
		#	score += 1

		#print(score)


	def increment_depth_dict(self, depth_dict, depth):
		if depth in depth_dict:
			depth_dict[depth] += 1
		else:
			depth_dict[depth] = 1

	def minimax(self, max=False, max_depth=6, depth=0, max_time=0, algo=1, depth_dict=dict()):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		value = self.INFINITY
		if max:
			value = -self.INFINITY
		x = None
		y = None
		result = self.is_end()
		if result == 'X':
			self.increment_depth_dict(depth_dict, depth)
			return (self.MIN, x, y, depth_dict, depth)
		elif result == 'O':
			self.increment_depth_dict(depth_dict, depth)
			return (self.MAX, x, y, depth_dict, depth)
		elif result == '.':
			self.increment_depth_dict(depth_dict, depth)
			return (0, x, y, depth_dict, depth)
		
		# If we're approaching the maximum allowed time, make a decision!
		elif ((time.time() + 0.1 * self.max_allowed_time) > max_time):
			self.increment_depth_dict(depth_dict, depth)
			heuristic = self.heuristic_score if algo == 1 else self.e3(max=max)
			return (heuristic, x, y, depth_dict, depth)
		
		# If we reach (depth == max_depth) --> calcualte heuristic + and return
		elif depth == max_depth:
			self.increment_depth_dict(depth_dict, depth)
			heuristic = self.heuristic_score if algo == 1 else self.e3(max=max)
			return (heuristic, x, y, depth_dict, depth)

		# Otherwise, generate game tree
		sum_children_ard = 0
		num_children = 0

		for i in range(0, self.board_size):
			for j in range(0, self.board_size):
				if self.current_state[i][j] == '.':

					temp_last_move = self.last_move
					temp_total_moves = self.total_moves
					temp_heuristic_score = self.heuristic_score
					self.last_move = (i, j)
					self.total_moves += 1

					if max:
						self.current_state[i][j] = 'O'
						self.heuristic_score += self.chance_matrix[i][j]
						(v, _, _, _, ard) = self.minimax(max=False, max_depth=max_depth, depth=(depth+1), max_time=max_time, algo=algo, depth_dict=depth_dict)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						self.heuristic_score -= self.chance_matrix[i][j]
						(v, _, _, _, ard) = self.minimax(max=True, max_depth=max_depth, depth=(depth+1), max_time=max_time, algo=algo, depth_dict=depth_dict)
						if v < value:
							value = v
							x = i
							y = j

					# Update metrics for average recusion depth
					sum_children_ard += ard
					num_children += 1

					# Restore game state!
					self.current_state[i][j] = '.'
					self.last_move = temp_last_move
					self.total_moves = temp_total_moves
					self.heuristic_score = temp_heuristic_score

		ard = sum_children_ard / num_children 
		return (value, x, y, depth_dict, ard)

	def alphabeta(self, alpha=-sys.maxsize, beta=sys.maxsize, max=False, max_depth=6, depth=0, max_time=0, algo=1, depth_dict=dict()):
		# Minimizing for 'X' and maximizing for 'O'
		# Possible values are:
		# -1 - win for 'X'
		# 0  - a tie
		# 1  - loss for 'X'
		# We're initially setting it to 2 or -2 as worse than the worst case:
		value = self.INFINITY
		if max:
			value = -self.INFINITY
		x = None
		y = None
		result = self.is_end()
		if result == 'X':
			self.increment_depth_dict(depth_dict, depth)
			return (self.MIN, x, y, depth_dict, depth)
		elif result == 'O':
			self.increment_depth_dict(depth_dict, depth)
			return (self.MAX, x, y, depth_dict, depth)
		elif result == '.':
			self.increment_depth_dict(depth_dict, depth)
			return (0, x, y, depth_dict, depth)

		# If we're approaching the maximum allowed time, make a decision!
		elif ((time.time() + 0.1 * self.max_allowed_time) > max_time):
			self.increment_depth_dict(depth_dict, depth)
			heuristic = self.heuristic_score if algo == 1 else self.e3(max=max)
			return (heuristic, x, y, depth_dict, depth)
		
		# If we reach (depth == max_depth) --> calcualte heuristic + and return
		elif depth == max_depth:
			self.increment_depth_dict(depth_dict, depth)
			heuristic = self.heuristic_score if algo == 1 else self.e3(max=max)
			return (heuristic, x, y, depth_dict, depth)

		# Otherwise, generate game tree
		sum_children_ard = 0
		num_children = 0
		for i in range(0, self.board_size):
			for j in range(0, self.board_size):
				if self.current_state[i][j] == '.':

					temp_last_move = self.last_move
					temp_total_moves = self.total_moves
					temp_heuristic_score = self.heuristic_score
					self.last_move = (i, j)
					self.total_moves += 1

					if max:
						self.current_state[i][j] = 'O'
						self.heuristic_score += self.chance_matrix[i][j]
						(v, _, _, _, ard) = self.alphabeta(alpha, beta, max=False, max_depth=max_depth, depth=(depth+1), max_time=max_time, algo=algo, depth_dict=depth_dict)
						if v > value:
							value = v
							x = i
							y = j
					else:
						self.current_state[i][j] = 'X'
						self.heuristic_score -= self.chance_matrix[i][j]
						(v, _, _, _, ard) = self.alphabeta(alpha, beta, max=True, max_depth=max_depth, depth=(depth+1), max_time=max_time, algo=algo, depth_dict=depth_dict)
						if v < value:
							value = v
							x = i
							y = j
					
					# Update metrics for average recusion depth
					sum_children_ard += ard
					num_children += 1

					# Restore game state!
					self.current_state[i][j] = '.'
					self.last_move = temp_last_move
					self.total_moves = temp_total_moves
					self.heuristic_score = temp_heuristic_score

					if max: 
						if value >= beta:
							return (value, x, y, depth_dict, depth)
						if value > alpha:
							alpha = value
					else:
						if value <= alpha:
							return (value, x, y, depth_dict, depth)
						if value < beta:
							beta = value

		ard = sum_children_ard / num_children
		return (value, x, y, depth_dict, ard)
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

	def calclulate_avg_per_move_depth(self, depth_dict):
		numerator = 0
		denominator = sum(depth_dict.values())
		for depth in depth_dict:
			numerator += depth * depth_dict[depth]
		return numerator/denominator

	def merge_depth_dicts(self, depths):
		new_depths = dict()
		for depth_dict in depths:
			for depth in depth_dict:
				if depth in new_depths:
					new_depths[depth] += depth_dict[depth]
				else:
					new_depths[depth] = depth_dict[depth]
		return new_depths

	def calculate_game_averages(self, time_list, depths, ard_list, num_moves):
		"""
		time_list: list of evaluation times
		depths: list of dictionaries. e.g. [{1: 23, 2: 80, 6: 900}, {1: 43, 2: 80, 3: 120}]
		ard_list: list of average recursion depth (ARD). e.g. [1.02, 5.22, ...]
		num_moves: total number of moves
		"""
		#(i) Average evaluation time
		average_eval_time = sum(time_list)/len(time_list)

		#(ii) Total heuristic evaluations
		total_depths = self.merge_depth_dicts(depths)
		total_heuristic_evaluations = sum(total_depths.values())

		#(iii) Evaluations by depth --> total_depths

		# (iv) Average evaluation depth
		average_eval_depth = self.calclulate_avg_per_move_depth(total_depths)

		# (v) Average recursion depth
		average_ard = sum(ard_list) / len(ard_list)

		# Total Moves --> num_moves

		print("Average evaluation time: ", average_eval_time)
		print("Total heuristic evaluations: ", total_heuristic_evaluations)
		print("Evaluations by depth: ", total_depths)
		print("Average evaluation depth: ", average_eval_depth)
		print("Average recursion depth: ", average_ard)
		return (average_eval_time, total_heuristic_evaluations, total_depths, average_eval_depth, average_ard, num_moves)
		


	def play(self):
		
		depth_list = []
		time_list = []
		ard_list = []

		while True:
			self.draw_board()
			if self.check_end():
				self.calculate_game_averages(time_list, depth_list, ard_list, self.total_moves)
				return
			start = time.time()
			cutoff_time = start + self.max_allowed_time
			depth_dict = dict()
			if self.search_type == self.MINIMAX:
				if self.player_turn == 'X':
					(_, x, y, depth_dict, ard) = self.minimax(max=False, max_time=cutoff_time, algo=1, max_depth=self.max_depth_p1, depth_dict=depth_dict)
				else:
					(_, x, y, depth_dict, ard) = self.minimax(max=True, max_time=cutoff_time, algo=2, max_depth=self.max_depth_p2, depth_dict=depth_dict)
			else: # search_type == self.ALPHABETA
				if self.player_turn == 'X':
					(m, x, y, depth_dict, ard) = self.alphabeta(max=False, max_time=cutoff_time, algo=1, max_depth=self.max_depth_p1, depth_dict=depth_dict)
				else:
					(m, x, y, depth_dict, ard) = self.alphabeta(max=True, max_time=cutoff_time, algo=2, max_depth=self.max_depth_p2, depth_dict=depth_dict)
			end = time.time()
			if (self.player_turn == 'X' and self.player_x == self.HUMAN) or (self.player_turn == 'O' and self.player_o == self.HUMAN):
					if self.recommend:
						print(F'Evaluation time: {round(end - start, 7)}s')
						print(F'Recommended move: x = {x}, y = {y}')
					(x,y) = self.input_move()
			if (self.player_turn == 'X' and self.player_x == self.AI) or (self.player_turn == 'O' and self.player_o == self.AI):
						print(F'Evaluation time: {round(end - start, 7)}s')
						#print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
						print(F'Player {self.player_turn} under AI control plays: {chr(y + 65)}{x}')
			if self.player_turn == 'X':
				self.heuristic_score -= self.chance_matrix[x][y]
			else:
				self.heuristic_score += self.chance_matrix[x][y]
			self.current_state[x][y] = self.player_turn
			self.last_move = (x, y)
			self.total_moves += 1
			self.switch_player()

			print("Total heuristic evaluations: ", sum(depth_dict.values()))
			print("Evaluations by depth: ", depth_dict)
			print("Average evaluation depth:", self.calclulate_avg_per_move_depth(depth_dict))
			print("Average recursion depth: ", ard)

			depth_list.append(depth_dict)
			time_list.append(round(end - start, 7))
			ard_list.append(round(ard, 2))

def main():
	
	g = Game(recommend=False)
	g.play()
	# g.play(player_x=Game.AI,player_o=Game.HUMAN)

if __name__ == "__main__":
	main()

