def transform_into_list(lst, invert=False):
    new_string = ''.join((ch if ch in '0123456789-' else ' ') for ch in lst)
    if not invert:
        new_list = [int(i) for i in new_string.split()]
        return new_list
    new_list = [-int(i) for i in new_string.split()]
    return new_list
    

class Simplex:

    def __init__(self, objective_function, constrains, n):
        self.objective_function = objective_function
        self.constrains = constrains
        self.matrix = []
        self.pivot = []
        self.n = n

    def mount_matrix(self):
        # Insert constrains into matrix
        for rule in self.constrains:
            self.matrix.append(transform_into_list(rule))
        
        for index, row in enumerate(self.matrix):
            for i in range(len(self.matrix)):
                if i == index:
                    row.insert(len(row) - 1, 1)
                else:
                    row.insert(len(row) - 1, 0)
            row.insert(len(row) - 1, 0)

        # Insert objective function into matrix
        function = transform_into_list(self.objective_function, True)
        for i in range(len(self.matrix)):
            function.insert(len(function) - 1, 0)
        function.append(0)
        function[-2] *= -1
            
        self.matrix.append(function)


    def find_pivot(self):
        pivot_column = self.matrix[-1].index(min(self.matrix[-1]))

        pivot = [0 , pivot_column]

        smallest_ratio = max(self.matrix[0])

        for i in self.matrix[:-1]:
            if i[pivot_column] != 0:
                if i[-1] / i[pivot_column] < smallest_ratio: 
                    smallest_ratio = i[-1] / i[pivot_column]
                    pivot = [self.matrix.index(i), pivot_column]
    
        self.pivot = pivot

        return self.pivot

    def pivot_row(self):
        # Get the inverse of the pivot element
        multiplier = 1 / self.matrix[self.pivot[0]][self.pivot[1]]

        for index, element in enumerate(self.matrix[self.pivot[0]]):
            self.matrix[self.pivot[0]][index] = element * multiplier
    
    def row_operations(self):
        values = [[-self.matrix[index][self.pivot[1]], index] for index in range(len(self.matrix)) if index != self.pivot[0]]

        for element in values:
            row = element[1]
            multiplier = element[0]
            for index in range(len(self.matrix[row])):
                self.matrix[row][index] = self.matrix[row][index] + self.matrix[self.pivot[0]][index] * multiplier
    
    def verify_if_ended(self):
        for i in self.matrix[-1]:
            if i < 0:
                return False
        return True
    
    def get_result(self):
        result = [[0 for i in range(self.n)]]
        for i in range(self.n):
            count_one = 0
            count_zero = 0
            coordinates = 0
            index = 0
            for j in range(len(self.matrix)):
                if self.matrix[j][i] == 1:
                    count_one += 1
                    coordinates = self.matrix[j][-1]
                    index = i
                elif self.matrix[j][i] == 0:
                    count_zero += 1
                if count_one == 1 and count_zero == len(self.matrix) - 1:
                    result[0][index] = coordinates
        
        result.append(self.matrix[-1][-1])
        return result
                
        
def main():
    #sample = Simplex("8x + 10y + 7z = 1z", ["1x + 3y + 2z <= 10", "1x + 5y + 1z <= 8"], [], [], 3)
    sample = Simplex("180a + 200b = 1z", ["5a + 4b <= 120", "1a + 2b <= 60"], 3)
    sample.mount_matrix()

    while True:
        sample.find_pivot()
        sample.pivot_row()
        sample.row_operations()
        if sample.verify_if_ended():
            break
    
    result = sample.get_result()
    print("\n\n")
    print(f"Maximum value of {result[1]} at {result[0]}")
    print("\n\n")


if __name__ == "__main__":
    main()

