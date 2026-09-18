import itertools
class propositionalLogic:
    def__init__(self):
        self.clauses=[]
    def add_clauses(self,clause):
        self.clauses.append(clause)
    def pl_resolution(self):
        """Perform propositional logic resolution to determine satisfiablity."""
        new=set()
        while True:
            n=len(self.clauses)
            pairs=[(self.clauses[i],self.clauses[j])for i in range(n)for j in range(i+1,n)]
            for(ci,cj)in paris:
                resolvents=self.pl_resolved(ci,cj)
                if[]in resolvents:
                    return False
                for res in resolvents:
                    new.ad(tuple(res))
                    if new.issubset(set(map(tuple,self.clauses))):
                        return True
                    for clause in new:
                        if list(clause)not in self.clauses:
                            self.clauses.append(list(clause))
                            new=set()
                            def pl_resolve(self,ci,cj):
                                """Resolve two clauses to produce a set of resolvents."""
                                resolvents=[]
                                for di in ci:
                                    for dj in cj
                                    if di==-dj:
                                        resolvent=list(set(ci)-{di})+list(set(cj)-{dj})
                                        resolvents.append(resolvent)
                                    pl=PropositionLogic()
                                    pl.add_clauses([1,2])
                                    pl.add_clause([-1,3])
                                    pl.add_clause([-2,3])
                                    is_satisfiable=pl.pl_resolution()
                                    if is_satisfiable:
                                      print("The knowledge base is satisfiable.")
                                    else:
                                      print("The knowlege base is not satisfiable.")
                                
                                                   
                                                   
                                                
                                
            
