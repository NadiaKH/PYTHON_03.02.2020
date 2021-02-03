import os
import sys 

                    
class DirReader:
    
    def __init__(self, dir_name):
        self.dir_name = dir_name
        self.tree = os.walk(dir_name)
        
    def __enter__(self):
        return [name for name in self.generator()]
        
        
    def __exit__(self, _type, value, traceback):
        return 1
    
    def __iter__(self):
        return self.generator()
    
    
    def generator(self):
        for address, dirs, files in self.tree:
            for file in files:
                filename, file_extension = os.path.splitext(file)
                if file_extension == ".txt":
                    yield address + '/' + file 
                    
                    
def getNamesFromFile(f):
    
    names = set()
    
    f.readline()
    for line in f:
        tokens = [token.strip() for token in line.split('\t')]
        if isSeq(tokens[-1]):
            for token in tokens:
                if (isName(token)):
                    names.add(token)
    return names


def isName(string):
    if len(string.split(' ')) != 2:
        return False
    
    nm, snm = string.split(' ')
    return True
    

def isSeq(string):
    return set(string).issubset(set("ATGCU"))



def getUniqueNames(dirname):
    names = set()
    with DirReader(dirname) as file_names:
        for fn in file_names:
            f = open(fn, 'r')
            names_from_f = getNamesFromFile(f)
            names.update(names_from_f)
            
    return names 


def buildGraphHelper(graph, f):
    
    f.readline()
    for line in f:
        tokens = [token.strip() for token in line.split('\t')]
        if isSeq(tokens[-1]):
            names = [token for token in tokens if isName(token)]
            
            for i in range(len(names)):
                for j in range(len(names)):
                    graph[names[i]].append(names[j])
    return graph
                    

def buildGraph(graph, dirname):
    with DirReader(dirname) as file_names:
        for fn in file_names:
            f = open(fn, 'r')
            buildGraphHelper(graph, f)
    
    return graph
    
    
    


def print_iter(giter = None, *, stream=sys.stdout):
    
    if giter is None:
        return lambda giter: print_iter(giter, stream=stream)
    
    def inner(*args, **kwargs):
        for r in giter(*args, **kwargs):
            print(r, file=stream)
            yield r
    return inner
        

        
@print_iter(stream = sys.stderr)
class GraphIterator:
    def __init__(self, G):
        self.G = G
        self.weights = [(sum(key == name for name in G[key]), key) for key in G]

        
        
    def __iter__(self):
        return self.generator()
    
    
    def generator(self):
        ws = sorted(self.weights)
        ws.reverse()
        
        for w, key in ws:
            yield key, w
        
        

#if __name__ == '__main__':

#    names = getUniqueNames('data')
    
#    graph = dict(key_val for key_val in [(name, []) for name in names])
    
#    buildGraph(graph, 'data')
        
    
#    for g in GraphIterator(graph):
#        pass




