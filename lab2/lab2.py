# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = False

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph

def pause():
    programPause = raw_input("Press the <ENTER> key to continue...")

def buscar(graph,start,goal,funAgregar,beam_width=0,back=True,exs=True,debug=False):
    agenda = [[start]]  # Un solo camino, que solo tiene al nodo de inicio
    if(exs):
        extended_set = [start]  # Hay que implementar que sea un "SET"

    if (debug):
        print "start= ", start, " - goal= ",goal
        i = 0
    # Tomar el primer camino de la agenda, sacandolo (pop) - Si el camino llega a goal, terminar el algoritmo
    while (True):
        if (debug):
            i+=1
            print "iter(", i, ") -- Agenda: ", agenda

        if(debug and exs):
            print "iter(", i, ") -- Extended: ", extended_set

        if(len(agenda)==0):
            return []
        path = agenda.pop()  # tener en cuenta el caso None

        if (debug):
            print "iter(",i,") -- Path: ",path

        ultimoNodo = path[-1]  # list[-1] es el ultimo elemento
        if (ultimoNodo == goal):
            break

        # Conseguir los nodos conectados al ultimo del camino
        nodosConectados = graph.get_connected_nodes(ultimoNodo)

        if (debug):
            print "iter(", i, ") -- nodosConectados: ", nodosConectados

        # Entre los nodos que no hayan sido extendidos (y no esten en el camino; aunque creo que todos los del camino ya fueron extendidos o son el ultimo) elijo uno, extiendo y agrego el camino resultante a la agenda
        # Agregar el nodo extendido a la lista de extendidos
        # Si el camino no se pudo extender, tomar el siguiente camino y repetir hasta que no queden caminos (Backtracking)
        nodosPosibles = []
        if(exs):
            for n in nodosConectados:
                if (not (n in extended_set)):  #No necesito chequear que no esten en mi propio camino porque todos esos ya fueron extendidos
                    nodosPosibles.append(n)
        else:
            for n in nodosConectados:
                if (not (n in path)): #Ahora solo chequeo que no los haya agregado en el camino (evito loops, por lo menos)
                    nodosPosibles.append(n)

        cantPosibles = len(nodosPosibles)
        if (cantPosibles == 0):
            if(back):
                continue
            else:
                return [] #Si no hay backtracking no quiero probar otros de la agenda que puedan haber quedado
        if ((cantPosibles > 1) and back):  # Backtracking; devuelvo el camino original a la agenda, por las dudas si llego a un dead-end => pruebo con otra opcion
            agenda.append(path)

        if (debug):
            print "iter(", i, ") -- nodosPosibles: ", nodosPosibles
        # Agrego todas las extensiones posibles
        pathsAAgregar = []
        for nodoP in nodosPosibles:
            if(exs):
                extended_set.append(nodoP)

            pathAAgregar = []
            pathAAgregar += path
            pathAAgregar.append(nodoP)
            pathsAAgregar.append(pathAAgregar)

        if (debug):
            print "iter(", i, ") -- pathsAAgregar: ", pathsAAgregar

        funAgregar(agenda,pathsAAgregar,graph,goal,beam_width) #Esto agrega el camino y reordena la agenda, si es necesario (depende del algoritmo que se quiera)

        if(debug):
            pause()
        # Repetir

    return path


## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.
def funAgregarBFS(agenda,pathsAAgregar,graph,goal,beam_width):
    tempAAgregar = []
    for path in pathsAAgregar:
        tempAAgregar.insert(0,path)
    for path in tempAAgregar:
        agenda.insert(0,path)

def bfs(graph, start, goal):
    return buscar(graph,start,goal,funAgregarBFS)


## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def funAgregarDFS(agenda,pathsAAgregar,graph,goal,beam_width):
    tempAAgregar = []
    for path in pathsAAgregar:
        tempAAgregar.insert(0,path)
    for path in tempAAgregar:
        agenda.append(path)

def dfs(graph, start, goal):
    return buscar(graph, start, goal, funAgregarDFS)


## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def funAgregarHillC(agenda,pathsAAgregar,graph,goal,beam_width):
    #print "pathsAAgregar antes de sort: ",pathsAAgregar
    tempAAgregar = sorted(pathsAAgregar,key=lambda x: graph.get_heuristic(x[-1],goal),reverse=True) #Queda el mas chico "a lo ultimo"
    #print "tempAAgregar despues de sort: ", tempAAgregar
    for path in tempAAgregar:
        agenda.append(path)
        #print "Valor Heuristic path ",path," es: ",graph.get_heuristic(path[-1],goal)

def hill_climbing(graph, start, goal):
    return buscar(graph,start,goal,funAgregarHillC,back=True,exs=False,debug=False)

## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def funAgregarBeam(agenda,pathsAAgregar,graph,goal,beam_width):
    tempAAgregar = pathsAAgregar
    tempAAgregar = sorted(tempAAgregar, key=lambda x: graph.get_heuristic(x[-1], goal))  # Queda el mas chico "al principio"

    del agenda[:]
    cantidad = min(len(tempAAgregar),beam_width)

    for i in range(0,cantidad):
        agenda.append(tempAAgregar[i])

def beam_search(graph, start, goal, beam_width):
    agenda = [[start]]  # Un solo camino, que solo tiene al nodo de inicio
    # Tomar el primer camino de la agenda, sacandolo (pop) - Si el camino llega a goal, terminar el algoritmo

    while (True):

        if(len(agenda)==0):
            return []

        pathsAAgregar = []
        for path in agenda:
            ultimoNodo = path[-1]  # list[-1] es el ultimo elemento
            if (ultimoNodo == goal):
                return path

            # Conseguir los nodos conectados al ultimo del camino
            nodosConectados = graph.get_connected_nodes(ultimoNodo)

            # Entre los nodos que no hayan sido extendidos (y no esten en el camino; aunque creo que todos los del camino ya fueron extendidos o son el ultimo) elijo uno, extiendo y agrego el camino resultante a la agenda
            # Agregar el nodo extendido a la lista de extendidos
            # Si el camino no se pudo extender, tomar el siguiente camino y repetir hasta que no queden caminos (Backtracking)
            nodosPosibles = []
            for n in nodosConectados:
                if (not (n in path)): #Ahora solo chequeo que no los haya agregado en el camino (evito loops, por lo menos)
                    nodosPosibles.append(n)

            # Agrego todas las extensiones posibles
            for nodoP in nodosPosibles:
                pathAAgregar = []
                pathAAgregar += path
                pathAAgregar.append(nodoP)
                pathsAAgregar.append(pathAAgregar)

        cantPaths = len(pathsAAgregar)
        if(cantPaths==0):
            return []

        funAgregarBeam(agenda,pathsAAgregar,graph,goal,beam_width) #Esto agrega el camino y reordena la agenda, si es necesario (depende del algoritmo que se quiera)

        # Repetir


    #return buscar(graph, start, goal, funAgregarBeam, beam_width, back=False, exs=False, debug=True)

## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    largo = 0
    for i in range(0,len(node_names)-1):
        edge = graph.get_edge(node_names[i],node_names[i+1])
        largo += edge.length
    return largo

def funAgregarByB(agenda,pathsAAgregar,graph,start):
    tempAAgregar = pathsAAgregar + agenda
    tempAAgregar = sorted(tempAAgregar, key=lambda x: path_length(graph,x))  # Queda el mas chico "al principio"

    del agenda[:]

    for i in range(0,len(tempAAgregar)):
        agenda.append(tempAAgregar[i])


def branch_and_bound(graph, start, goal):
    #print graph
    #print "Branch & Bound: start = ",start," ,goal = ",goal
    agenda = [[start]]  # Un solo camino, que solo tiene al nodo de inicio
    # Tomar el primer camino de la agenda, sacandolo (pop) - Si el camino llega a goal, terminar el algoritmo

    #i = 0
    while (True):
        #i+=1
        #print "iter(",i,")"
        #print "agenda = ",agenda
        #print "largos = ",[path_length(graph,x) for x in agenda]

        if(len(agenda)==0):
            return []

        pathsAAgregar = []
        path = agenda.pop(0)
        ultimoNodo = path[-1]  # list[-1] es el ultimo elemento
        if (ultimoNodo == goal):
            return path

            # Conseguir los nodos conectados al ultimo del camino
        nodosConectados = graph.get_connected_nodes(ultimoNodo)

            # Entre los nodos que no hayan sido extendidos (y no esten en el camino; aunque creo que todos los del camino ya fueron extendidos o son el ultimo) elijo uno, extiendo y agrego el camino resultante a la agenda
            # Agregar el nodo extendido a la lista de extendidos
            # Si el camino no se pudo extender, tomar el siguiente camino y repetir hasta que no queden caminos (Backtracking)
        nodosPosibles = []
        for n in nodosConectados:
            if (not (n in path)): #Ahora solo chequeo que no los haya agregado en el camino (evito loops, por lo menos)
                nodosPosibles.append(n)

            # Agrego todas las extensiones posibles
        for nodoP in nodosPosibles:
            pathAAgregar = []
            pathAAgregar += path
            pathAAgregar.append(nodoP)
            pathsAAgregar.append(pathAAgregar)

        cantPaths = len(pathsAAgregar)
        if(cantPaths==0):
            continue

        funAgregarByB(agenda,pathsAAgregar,graph,start) #Esto agrega el camino y reordena la agenda, si es necesario (depende del algoritmo que se quiera)

        # Repetir


def funAgregarAStar(agenda,pathsAAgregar,graph,goal):
    tempAAgregar = sorted(agenda+pathsAAgregar, key=lambda x: path_length(graph,x) + graph.get_heuristic(x[-1], goal))  # Queda el mas chico "al principio"

    del agenda[:]

    for i in range(0,len(tempAAgregar)):
        agenda.append(tempAAgregar[i])
        #path = tempAAgregar[i]
        #print "camino: ",path,"-> ",path_length(graph,path) + graph.get_heuristic(path[-1], goal)


def a_star(graph, start, goal):
    #print "start= ",start," goal= ",goal
    #print graph

    agenda = [[start]]  # Un solo camino, que solo tiene al nodo de inicio
    # Tomar el primer camino de la agenda, sacandolo (pop) - Si el camino llega a goal, terminar el algoritmo
    extendidos = []

    while (True):
        #print "agenda = ",agenda

        if(len(agenda)==0):
            return []

        pathsAAgregar = []
        path = agenda.pop(0)

        ultimoNodo = path[-1]  # list[-1] es el ultimo elemento
        if (ultimoNodo == goal):
            return path

        # Conseguir los nodos conectados al ultimo del camino
        nodosConectados = graph.get_connected_nodes(ultimoNodo)

            # Entre los nodos que no hayan sido extendidos (y no esten en el camino; aunque creo que todos los del camino ya fueron extendidos o son el ultimo) elijo uno, extiendo y agrego el camino resultante a la agenda
            # Agregar el nodo extendido a la lista de extendidos
            # Si el camino no se pudo extender, tomar el siguiente camino y repetir hasta que no queden caminos (Backtracking)
        nodosPosibles = []
        for n in nodosConectados:
            if(not (n in extendidos)): #Chequeo que no haya sido extendido previamente
                nodosPosibles.append(n)

            # Agrego todas las extensiones posibles
        for nodoP in nodosPosibles:
            pathAAgregar = []
            pathAAgregar += path
            pathAAgregar.append(nodoP)
            pathsAAgregar.append(pathAAgregar)

        cantPaths = len(pathsAAgregar)
        if(cantPaths==0):
            continue
        if(cantPaths>=1):
            extendidos.append(ultimoNodo)

        funAgregarAStar(agenda,pathsAAgregar,graph,goal) #Esto agrega el camino y reordena la agenda, si es necesario (depende del algoritmo que se quiera)

        # Repetir

## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
    admisible = True
    for node in graph.nodes:
        #Encontrar el camino optimo con B&B
        optimPath = branch_and_bound(graph,node,goal)
        if(graph.get_heuristic(node,goal)>path_length(graph,optimPath)):
            admisible = False
    return admisible


def is_consistent(graph, goal):
    admisible = True
    for node1 in graph.nodes:
        for node2 in graph.nodes:
            #Encontrar el camino optimo con B&B
            optimPath = branch_and_bound(graph,node1,node2)
            if(abs(graph.get_heuristic(node1,goal)-graph.get_heuristic(node2,goal))>path_length(graph,optimPath)):
                admisible = False
    return admisible

HOW_MANY_HOURS_THIS_PSET_TOOK = '8'
WHAT_I_FOUND_INTERESTING = 'Everything'
WHAT_I_FOUND_BORING = 'Nothing'
