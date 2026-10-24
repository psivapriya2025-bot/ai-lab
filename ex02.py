import random
class NQueensCSO:
    def__init__(self,N):
        self.N=N
        self.domains=list(range(N))
        def conflicts(self,assignment):
            """Retuns the number of conflicts in the current assignment."""
            count=0
            for i in range (self.N):
                for j in range(i+1,self.N):
                    if assignment[i]==assignment[j]or abs(assignment[i]-assignment[j])==j-i:
                        count+=1
                     return count
                    def min_conflicts(self,max_steps=1000):
                        """Min-conflicts algorithm solve the N-Queens program."""
                        assignment=[random.choice(self.domains)for_in range(self.N]
                        for_in range(max_steps):
                          if self.conflicts(assignment)==0:
                             return assignmt
                           conflicted_vars=[i for i in range(self.N)if self.conflicts(assignment)>0]
                           var=random.choice(conflicted_vars)
                           min_conflict_value=min(self.domains,key=lambda val:self.conflicts(assignmet[:var]+[val]+assignment[var+1:]))
                           assignment[var]=min_conflicts_value
                         return None
                       #Example usage
                        N=8
                        nqueens=NQueensCsP(N)
                        solution=nqueen.min_conflicts()
                        if solution:
                            print("Solution found:",solution)
                        else:
                            print("No solution found within the maximum number of steps")
                                 
                                
                        
