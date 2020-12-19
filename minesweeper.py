import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count == len(self.cells):
            return self.cells
        else:
            return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1) mark the cell as a move that has been made
        self.moves_made.add(cell)
        # 2) mark the cell as safe
        self.safes.add(cell)
        self.mark_safe(cell)
        # 3) add a sentence with new information about neighbors to knowledge
        neighbor_cells = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ignore the cell itself
                if (i, j) == cell:
                    continue
                # Ignore known safe cells
                if (i,j) in self.safes:
                    continue
                # Ignore known mines and decrement count
                if (i,j) in self.mines:
                    count -= 1
                    continue
                # Add cell to neighbor_cells if it's on the board and untouched
                if 0 <= i < self.height and 0 <= j < self.width and (i,j) not in self.moves_made:
                    neighbor_cells.add((i,j))
        s = Sentence(neighbor_cells, count)
        self.knowledge.append(s)
        # 4) mark any additional cells as safe or as mines
        found_mines = []
        found_safes = []
        for sen in self.knowledge:
            sen_mines = sen.known_mines()
            for sen_mine in sen_mines:
                found_mines.append(sen_mine)
            sen_safes = sen.known_safes()
            for sen_safe in sen_safes:
                found_safes.append(sen_safe)
        for sen_mine in found_mines:
            self.mark_mine(sen_mine)
        for sen_safe in found_safes:
            self.mark_safe(sen_safe)
        # 5) add any new sentences to the AI's knowledge base
        for sen1 in reversed(self.knowledge):  # iterate backwards so we can delete
            for sen2 in reversed(self.knowledge):
                if not sen1.cells:
                    try: self.knowledge.remove(sen1)
                    except: pass
                    continue
                if not sen2.cells:
                    try: self.knowledge.remove(sen2)
                    except: pass
                    continue
                if sen1 == sen2:
                    continue
                elif sen1.cells.issubset(sen2.cells):
                    cells3 = sen2.cells - sen1.cells
                    count3 = sen2.count - sen1.count
                    sen3 = Sentence(cells3, count3)
                    self.knowledge.append(sen3)
                    #remove old sentence if it still exists
                    try: self.knowledge.remove(sen2)
                    except: pass
                elif sen2.cells.issubset(sen1.cells):
                    cells3 = sen1.cells - sen2.cells
                    count3 = sen1.count - sen2.count
                    sen3 = Sentence(cells3, count3)
                    self.knowledge.append(sen3)
                    # remove old sentence if it still exists
                    try: self.knowledge.remove(sen1)
                    except: pass

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # check for known safes
        for known_safe in self.safes:
            if known_safe not in self.moves_made:
                return known_safe
        # check for new safes
        for sen in self.knowledge:
            sen_safes = sen.known_safes()
            if sen_safes:
                for sen_safe in sen_safes:
                    if sen_safe not in self.moves_made:
                        return sen_safe
        # check for new knowledge
        for sen1 in self.knowledge:
            for sen2 in self.knowledge:
                if not sen1.cells or not sen2.cells:
                    continue
                if sen1 != sen2:
                    if sen1.cells.issubset(sen2.cells):
                        cells3 = sen2.cells - sen1.cells
                        count3 = sen2.count - sen1.count
                        sen3 = Sentence(cells3, count3)
                        self.knowledge.append(sen3)
                    elif sen2.cells.issubset(sen1.cells):
                        cells3 = sen1.cells - sen2.cells
                        count3 = sen1.count - sen2.count
                        sen3 = Sentence(cells3, count3)
                        self.knowledge.append(sen3)
        return None  # didn't find anything known to be safe

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        possibles = []
        for i in range(self.height):
            for j in range(self.width):
                if (i,j) not in self.moves_made and (i,j) not in self.mines:
                    possibles.append((i,j))
        if len(possibles):
            move = random.choice(possibles)
            return move
        else:
            return None
