import random
class Model:

    def __init__(self):
        self.possible_moves = ['W', 'A', 'D', 'P']
        # Initialise Eval
        self.move = 0

    def get_output(self):

        return self.possible_moves[self.move]

    def get_move(self):
        
        tracker = [self.possible_moves[0], None]
        chosen = None
        curr = 0

        while chosen == None:
            chosen = random.choice(tracker)

            curr += 1
            if curr < len(self.possible_moves) :
                tracker.append(None)
                tracker.append(self.possible_moves[curr])
        
        self.move = self.possible_moves.index(chosen)

        print(self.possible_moves)
        return self.get_output()

    def feedback(self, score):

        if score < 0 and self.move > 0:
           self.switch(self.move, self.move-1) 

        elif self.move < len(self.possible_moves) - 1:
            self.switch(self.move, self.move+1)

    def switch(self, index_1, index_2):
        
        temp = self.possible_moves[index_1]
        self.possible_moves[index_1] = self.possible_moves[index_2]
        self.possible_moves[index_2] = temp
