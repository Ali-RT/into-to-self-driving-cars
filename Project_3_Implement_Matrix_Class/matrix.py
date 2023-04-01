import math
from math import sqrt
import numbers

def zeroes(height, width):
        """
        Creates a matrix of zeroes.
        """
        g = [[0.0 for _ in range(width)] for __ in range(height)]
        return Matrix(g)

def identity(n):
        """
        Creates a n x n identity matrix.
        """
        I = zeroes(n, n)
        for i in range(n):
            I.g[i][i] = 1.0
        return I

def dot_product(vectorA, vectorB):
    result = 0
    
    for i in range(len(vectorA)):
        result += vectorA[i] * vectorB[i]
        
    return result
    
class Matrix(object):

    # Constructor
    def __init__(self, grid):
        self.g = grid
        self.h = len(grid)
        self.w = len(grid[0])

    #
    # Primary matrix math methods
    #############################
 
    def determinant(self):
        """
        Calculates the determinant of a 1x1 or 2x2 matrix.
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate determinant of non-square matrix.")
        if self.h > 2:
            raise(NotImplementedError, "Calculating determinant not implemented for matrices largerer than 2x2.")
        
        if self.h == 1:
            return self.g[0][0]
        
        a = self[0][0]
        b = self[0][1]
        c = self[1][0]
        d = self[1][1]

        return (a * d - b * c)


    def trace(self):
        """
        Calculates the trace of a matrix (sum of diagonal entries).
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate the trace of a non-square matrix.")

        trace = 0
        
        for i in range(self.h):
            trace += self[i][i]
            
        return trace

    def inverse(self):
        """
        Calculates the inverse of a 1x1 or 2x2 Matrix.
        """
        if not self.is_square():
            raise(ValueError, "Non-square Matrix does not have an inverse.")
        if self.h > 2:
            raise(NotImplementedError, "inversion not implemented for matrices larger than 2x2.")

        inverse = []
        det = self.determinant()
        
        if det == 0:
            raise ValueError('The matrix is not invertible.')
            
        if self.h == 1:
            inverse = [[1/det]]
            return Matrix(inverse)
        

        factor = 1 / (det)
        I = identity(self.h)
        
        inverse = factor * (self.trace() * I - self)
 
        return inverse

    def T(self):
        """
        Returns a transposed copy of this Matrix.
        """
        matrix_transpose = []
        # Loop through columns on outside loop
        for c in range(self.w):
            new_row = []
            # Loop through rows on inner loop
            for r in range(self.h):
                # Column values will be filled by what were each row before
                new_row.append(self.g[r][c])
            matrix_transpose.append(new_row)
        
        return Matrix(matrix_transpose)

    def is_square(self):
        return self.h == self.w

    #
    # Begin Operator Overloading
    ############################
    def __getitem__(self,idx):
        """
        Defines the behavior of using square brackets [] on instances
        of this class.

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix[0]
          [1, 2]

        > my_matrix[0][0]
          1
        """
        return self.g[idx]

    def __repr__(self):
        """
        Defines the behavior of calling print on an instance of this class.
        """
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"
        return s

    def __add__(self,other):
        """
        Defines the behavior of the + operator
        """
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be added if the dimensions are the same") 
        
        new_grid = []
        for i in range(self.h):
            new_row = []
            for j in range(self.w):
                new_row.append(self.g[i][j] + other[i][j])
            new_grid.append(new_row)
        
        return Matrix(new_grid)


    def __neg__(self):
        """
        Defines the behavior of - operator (NOT subtraction)

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > negative  = -my_matrix
        > print(negative)
          -1.0  -2.0
          -3.0  -4.0
        """
        new_grid = []
        for i in range(self.h):
            new_row = []
            for j in range(self.w):
                new_row.append(-self.g[i][j])
            new_grid.append(new_row)
        
        return Matrix(new_grid)

   

    def __sub__(self, other):
        """
        Defines the behavior of - operator (as subtraction)
        """
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be added if the dimensions are the same") 
        
        new_grid = []
        for i in range(self.h):
            new_row = []
            for j in range(self.w):
                new_row.append(self.g[i][j] - other[i][j])
            new_grid.append(new_row)
        
        return Matrix(new_grid)

    def __mul__(self, other):
        """
        Defines the behavior of * operator (matrix multiplication)
        """
        if self.w != other.h:
            raise(ValueError, "dimensions are mismatched") 
        
  
        product = []

        # Take the transpose of matrixB and store the result
        other_T = other.T()

        # Use a nested for loop to iterate through the rows
        # of matrix A and the rows of the tranpose of matrix B
        for i in range(self.h):
            new_row = []
            for j in range(other_T.h):
                # Calculate the dot product between each row of matrix A
                # with each row in the transpose of matrix B
                dp = dot_product(self.g[i], other_T[j])
                new_row.append(dp)
            # Store the results in the product variable
            product.append(new_row)
            
        return Matrix(product)

    def __rmul__(self, other):
        """
        Called when the thing on the left of the * is not a matrix.

        Example:

        > identity = Matrix([ [1,0], [0,1] ])
        > doubled  = 2 * identity
        > print(doubled)
          2.0  0.0
          0.0  2.0
        """
        if isinstance(other, numbers.Number):
            new_matrix = []
            for i in range(self.h):
                row = []
                for j in range(self.w):
                    row.append(other*self[i][j])
                new_matrix.append(row)
            return Matrix(new_matrix)