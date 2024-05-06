import matplotlib.pyplot as plt
import random

class Crossword:
    def __init__(self, size, variables, wordpool):
        self.size = size
        self.variables = variables
        self.wordpool = []
        for word in wordpool:
            if len(word) == size:
                self.wordpool.append(word)
        self.domains = {}
        for var in self.variables:
            self.domains[var] = self.wordpool[:]
        self.grid = []
        for _ in range(size):
            row = []
            for _ in range(size):
                row.append('')
            self.grid.append(row)
        self.solutions = 0

    def solve(self):
        if self.dfs(0):
            self.display()
            print("Solution found.")
        else:
            print("No solution found.")
        return self.solutions
    
    def grid_print(self):
        for row in self.grid:
            line = ""
            for cell in row:
                if cell == '':
                    line += '_'
                else:
                    line += cell
            print(line)
        print()
    def restore(self, index):
        for var in self.variables[index:]:
            self.domains[var] = self.wordpool[:]
    def filterdomain(self, var):
        row, col, direction = var
        new_domain = []
        for word in self.domains[var]:
            if self.check_place(word, row, col, direction):
                new_domain.append(word)
        self.domains[var] = new_domain

    def forwardcheck(self):
        for var in self.variables:
            if not self.domains[var]:
                return False
            self.filterdomain(var)
        return True
    
    def dfs(self, index):
        if index == len(self.variables):
            self.solutions += 1
            return True

        var = self.variables[index]
        row, col, direction = var

        random.shuffle(self.domains[var])
        domain = self.domains[var][:]

        for word in domain:
            print(f"Trying to place '{word}' at {(row, col)} {direction}")
            if self.check_place(word, row, col, direction):
                self.place(word, row, col, direction)
                self.grid_print()  
                if self.forwardcheck():
                    if self.dfs(index + 1):
                        return True
                self.remove(word, row, col, direction)
                self.grid_print() 
                self.restore(index)

        return False


    

    def check_place(self, word, row, col, direction):
        if direction == 'horizontal':
            if col + len(word) > self.size:
                return False
            for i in range(len(word)):
                r, c = row, col + i
                if self.grid[r][c] and self.grid[r][c] != word[i]:
                    return False
        elif direction == 'vertical':
            if row + len(word) > self.size:
                return False
            for i in range(len(word)):
                r, c = row + i, col
                if self.grid[r][c] and self.grid[r][c] != word[i]:
                    return False
        return True

    def place(self, word, row, col, direction):
        for i in range(len(word)):
            if direction == 'horizontal':
                r, c = row, col + i
            else:  
                r, c = row + i, col
            self.grid[r][c] = word[i]

    def remove(self, word, row, col, direction):
        for i in range(len(word)):
            if direction == 'horizontal':
                r, c = row, col + i
            else:  
                r, c = row + i, col
            self.grid[r][c] = ''

    def display(self):
        fig, ax = plt.subplots(figsize=(self.size, self.size))
        ax.axis('tight')
        ax.axis('off')
        tb = ax.table(cellText=self.grid, cellLoc='center', loc='center', cellColours=[['w']*self.size]*self.size)
        tb.auto_set_font_size(False)
        tb.set_fontsize(14)
        tb.scale(1, 1.5)
        plt.show()

# Example usage

if __name__ == "__main__":
    size = 5
    variables = [(0, 0, 'horizontal'), (0, 0, 'vertical'), (2, 0, 'horizontal'), (1, 0, 'horizontal'),(3, 0, 'horizontal'),(4, 0, 'horizontal')]
    wordpool = [
        "apple", "banjo", "charm", "dream", "eagle", "flute", "globe", "honey", "ivory", "joker",
        "kayak", "lemon", "mango", "nylon", "ocean", "piano", "quilt", "robot", "sugar", "tiger",
        "umbra", "vapor", "wheat", "xenon", "yacht", "zebra", "quiet", "watch", "video", "ultra",
        "table", "spoon", "ranch", "query", "prize", "opera", "night", "mirth", "lodge", "kneel",
        "jelly", "issue", "hotel", "grape", "focal", "event", "dutch", "crate", "brave", "asset"
    ]
    crossword = Crossword(size, variables, wordpool)
    results = crossword.solve()

    print(f"Total results found: {results}")
