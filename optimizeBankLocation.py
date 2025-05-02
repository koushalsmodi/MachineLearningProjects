import random

class Space:
    
    def __init__(self, height, width, num_banks):
        """Creates a state space with given dimensions"""
        self.height=height
        self.width=width
        self.num_banks = num_banks
        self.banks = set()
        self.houses = set()
        
    def add_house(self, row, col):
        """Adds a house in a particular location at state space"""
        self.houses.add((row, col))
        
    def available_spaces(self):
        """Returns all cells not currently used by a bank or house"""
        candidates = set(
            (row, col)
            for row in range(self.width)
            for col in range(self.height)
        )
        
        # Remove all banks
        for bank in self.banks:
            if bank in candidates:
                candidates.remove(bank)
            
        # Remove all houses
        for house in self.houses:
            if house in candidates:
                candidates.remove(house)
        
        return candidates
    
    """
    Hill Climbing Algorithm

    function HILL_CLIMB(problem):
        current = initial state of problem
        repeat:
            neighbor = highest valued neighbor of current (generate neighbors and choose best neighbor)
            if neighbor not better than current:
                return current
            current = neighbor 
    """

    def hill_climb(self, maximum=None, image_prefix=None, log=False):
        """Performing hill climbing algorithm to find a solution"""
        count = 0
        
        # Start by initializing banks randomly
        self.banks = set()
        for i in range(self.num_banks):
            self.banks.add(random.choice(list(self.available_spaces())))
            
        if log:
            print("Initial state: cost", self.get_cost(self.banks))
            
        if image_prefix:
            self.output_image(f"{image_prefix}{str(count).zfill(3)}.png")
        
        # Continue until we reach the maximum number of iterations
        while maximum is None or count < maximum:
            count+=1
            best_neighbors = []
            best_neighbor_cost = None
            
            # Consider all banks to move
            
            for bank in self.banks:
                
                # Consider all neighbors for that bank, for eg: (3,5)
                # Returns all valid adjacent cells, which may include (2,5); (4,5); (3,4); (3,6)
                for replacement in self.get_neighbors(*bank):
                    
                    # Generate a neighboring set of banks
                    
                    # Do not touch current setup
                    neighbor = self.banks.copy()
                    
                    # Remove current bank location
                    neighbor.remove(bank)
                    
                    # Add alternative location
                    neighbor.add(replacement)
                    
                    # Check if neighbor is best so far
                    cost = self.get_cost(neighbor)
                    
                    # Assuming current best cost = 10
                    if best_neighbor_cost is None or cost < best_neighbor_cost:
                        # Assuming current best cost = 10
                        best_neighbor_cost = cost 
                        # For neighbor1
                        # If neighbor2 has cost of 7, then best_neighbors = neighbor2
                        best_neighbors = [neighbor]
                    
                    # If neighbor3 has cost of 7 as well, then best_neighbors = neighbor2 and neighbor3 both
                    elif best_neighbor_cost == cost:
                        best_neighbors.append(neighbor)
                        
            # None of the neighbors are better than the current state
            if best_neighbor_cost >= self.get_cost(self.banks):
                return self.banks
            
            # Else: move to a higher valued neighbor
            else:
                if log:
                    print(f"Found better neighbor: cost {best_neighbor_cost}")

                self.banks = random.choice(best_neighbors)
            
            # Generate image:
            if image_prefix:
                self.output_image(f"{image_prefix}{str(count).zfill(3)}.png")
                
    def get_cost(self, banks):
        """Calculates sum of distances from banks to houses"""
        
        # Start with 0 total distance
        cost = 0
        """
        Let's say there are 5 houses and 2 banks
        B1 = (1,2)
        B2 = (4,3)
        
        H1 = (1,1); distance to B1 = |1-1| + |1-2| = |-1| = 1; distance to B2 = |1-4|+|1-3| = |-3|+|-2| = 5; min = 1
        H2 = (1,3); min = 1
        H3 = (3,2); distance to B1 = |3-1| + |2-2| = 2; distance to B2 = |3-4|+|2-3| = |-1|+|-1|= 2; min(2,2) = 2
        H4 = (4,4); min = 1
        H5 = (5,1); min = 3
        sum =  8
        """
        
        for house in self.houses:
            # Check every house
            # Find the distance closest to bank
            closest_distance = min(
                # min(Hx - Bx + Hy - By)
                abs(house[0] - bank[0]) + abs(house[1] - bank[1])
                for bank in banks
            )
            cost += closest_distance
        return cost 

    def get_neighbors(self, row, col):
        """Returns neighbors not already containing a house or bank"""
        # Up, down, left, right of the current bank
        
        candidates = [
            (row-1, col),
            (row+1, col),
            (row, col-1),
            (row, col+1)
        ]
        neighbors = []
        
        for r, c in candidates:
            # Already filled space
            if (r,c) in self.houses or (r,c) in self.banks:
                continue
                
            # Add neighbors
            if 0 <= r < self.height and 0 <= c < self.width:
                neighbors.append((r,c))
        return neighbors
    
    
    def output_image(self, filename):
        """Generates image with all houses and banks."""
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        cost_size = 40
        padding = 10

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size,
             self.height * cell_size + cost_size + padding * 2),
            "white"
        )
        house = Image.open("assets/images/House.png").resize(
            (cell_size, cell_size)
        )
        bank = Image.open("assets/images/Bank.png").resize(
            (cell_size, cell_size)
        )
        #font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 30)
        font = ImageFont.load_default()
        draw = ImageDraw.Draw(img)

        for i in range(self.height):
            for j in range(self.width):

                # Draw cell
                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                draw.rectangle(rect, fill="black")

                if (i, j) in self.houses:
                    #img.paste(house, rect[0], house)
                    img.paste(house, rect[0])
                if (i, j) in self.banks:
                    img.paste(bank, rect[0])

        # Add cost
        draw.rectangle(
            (0, self.height * cell_size, self.width * cell_size,
             self.height * cell_size + cost_size + padding * 2),
            "black"
        )
        draw.text(
            (padding, self.height * cell_size + padding),
            f"Cost: {self.get_cost(self.banks)}",
            fill="white",
            font=font
        )

        img.save(filename)

# Create a new space and add houses randomly
s = Space(height=10, width=20, num_banks = 2)
for i in range(20):
    s.add_house(random.randrange(s.height), random.randrange(s.width))

# Use local search to determine bank placement
banks = s.hill_climb(image_prefix='banks', log=True)
    
    
    