#########################################
#                                       #
#                                       #
#  ==  SOKOBAN AGENT CODE  ==   #
#                                       #
#      Written by: Naren Dhyani         #
#                                       #
#                                       #
#########################################


# SOLVER CLASSES WHERE AGENT CODES GO
from helper import *
import random
import math


# Base class of agent (DO NOT TOUCH!)
class Agent:
    def getSolution(self, state, maxIterations):

        '''
        EXAMPLE USE FOR TREE SEARCH AGENT:


        #expand the tree until the iterations runs out or a solution sequence is found
        while (iterations < maxIterations or maxIterations <= 0) and len(queue) > 0:
            iterations += 1

            [ POP NODE OFF OF QUEUE ]

            [ EVALUATE NODE AS WIN STATE]
                [ IF WIN STATE: BREAK AND RETURN NODE'S ACTION SEQUENCE]

            [ GET NODE'S CHILDREN ]

            [ ADD VALID CHILDREN TO QUEUE ]

            [ SAVE CURRENT BEST NODE ]


        '''


        '''
        EXAMPLE USE FOR EVOLUTION BASED AGENT:
        #expand the tree until the iterations runs out or a solution sequence is found
        while (iterations < maxIterations or maxIterations <= 0) and len(queue) > 0:
            iterations += 1

            [ MUTATE ]

            [ EVALUATE ]
                [ IF WIN STATE: BREAK AND RETURN ]

            [ SAVE CURRENT BEST ]

        '''


        return []       # set of actions



# Do Nothing Agent code - the laziest of the agents
class DoNothingAgent(Agent):
    def getSolution(self, state, maxIterations):
        if maxIterations == -1:     # RIP your machine if you remove this block
            return []

        #make idle action set
        nothActionSet = []
        for i in range(20):
            nothActionSet.append({"x":0,"y":0})

        return nothActionSet

# Random Agent code - completes random actions
class RandomAgent(Agent):
    def getSolution(self, state, maxIterations):

        #make random action set
        randActionSet = []
        for i in range(20):
            randActionSet.append(random.choice(directions))

        return randActionSet





# BFS Agent code
class BFSAgent(Agent):
    def getSolution(self, state, maxIterations=-1):
        intializeDeadlocks(state)
        iterations = 0
        bestNode = None
        queue = [Node(state.clone(), None, None)]
        visited = []

        #expand the tree until the iterations runs out or a solution sequence is found
        while (iterations < maxIterations or maxIterations <= 0) and len(queue) > 0:
            iterations += 1
        
            
            currentNode = queue.pop(0) # pop first node
            
            # check if node not in visited
            if currentNode.parent is None:
                visited.append(currentNode.getHash()) # setting up visited list for the first iteration
            elif currentNode.getHash() in visited:
                continue
            else:
                visited.append(currentNode.getHash()) # adding the popped node to visited list
            
            #setting up the BFS for first iteration
            if bestNode == None:
                bestNode = currentNode

            #check winning condition
            if currentNode.checkWin():
                bestNode = currentNode
                break
            
            #keeping track of best node
            if bestNode.getHeuristic()>currentNode.getHeuristic():
                bestNode = currentNode
            
            #expanding the tree
            children = currentNode.getChildren()
            for child in children:
                if child.getHash() not in visited:# and child.getHash() not in list(map((lambda a: a.getHash()),queue)):
                    queue.append(child)

            
            
        

        return bestNode.getActions()   #returning the sequence of the best node



# DFS Agent Code
class DFSAgent(Agent):
    def getSolution(self, state, maxIterations=-1):
        intializeDeadlocks(state)
        iterations = 0
        bestNode = None
        queue = [Node(state.clone(), None, None)]
        visited = []
        
        #expand the tree until the iterations runs out or a solution sequence is found
        while (iterations < maxIterations or maxIterations <= 0) and len(queue) > 0:
            iterations += 1

            currentNode = queue.pop()

            # check if node not in visited
            if currentNode.parent is None:
                visited.append(currentNode.getHash()) # setting up visited list for the first iteration
            elif currentNode.getHash() in visited:
                continue
            else:
                visited.append(currentNode.getHash()) # adding the popped node to visited list

            #setting up the DFS for first iteration
            if bestNode == None:
                bestNode = currentNode  

            # checking winning condition on current node
            if currentNode.checkWin():
                bestNode = currentNode
                break
            
            #keeping track of best node
            if bestNode.getHeuristic()>currentNode.getHeuristic():
                bestNode = currentNode
            

            #expanding the tree
            children = currentNode.getChildren()
            for child in children:
                if child.getHash() not in visited: #and child.getHash() not in list(map((lambda a: a.getHash()),queue)):
                    queue.append(child)


        return bestNode.getActions()   #returning the sequence of best node



# AStar Agent Code
class AStarAgent(Agent):
    def getSolution(self, state, maxIterations=-1):
        #setup
        intializeDeadlocks(state)
        iterations = 0
        bestNode = None

        #initialize priority queue
        queue = PriorityQueue()
        queue.put(Node(state.clone(), None, None))
        visited = []

        while (iterations < maxIterations or maxIterations <= 0) and queue.qsize() > 0:
            iterations += 1

            if queue.empty():
                break

            n = queue.get() #getting the highest priority node
            
            if n.parent == None: # setting up the AStar for first iteration
                bestNode = n
                visited.append(n.getHash())
            elif n.getHash() in visited: # checking if current node in visited
                continue
            else:
                if bestNode.getHeuristic() > n.getHeuristic(): #keeping track of bestnode
                    bestNode = n 
                visited.append(n.getHash()) # adding the popped node into visited list
            
            # checkwin condition for the current node
            if n.checkWin():
                bestNode = n
                break

            # expanding the tree
            for child in n.getChildren():
                if child.getHash() in visited:
                    continue
                
                q = []
                flag = False
                while not queue.empty(): # updating the parent node of child if it is present in open list and new cost is less than it's previous cost
                    ele = queue.get()
                    if child.getHash() == ele.getHash():
                        flag = True
                        if child.getCost()< ele.getCost():
                            ele.parent = n 
                    q.append(ele)
                
                for items in q:
                    queue.put(items)
                if not flag:
                    queue.put(child) # adding the child to the priority queue
                        
                    




        return bestNode.getActions()   # returning the sequence of bestnode



# Hill Climber Agent code
class HillClimberAgent(Agent):
    def getSolution(self, state, maxIterations=-1):
        #setup
        intializeDeadlocks(state)
        iterations = 0
        
        seqLen = 50            # maximum length of the sequences generated
        coinFlip = 0.5          # chance to mutate

        #initialize the first sequence (random movements)
        bestSeq = []
        for i in range(seqLen):
            bestSeq.append(random.choice(directions))

        #mutate the best sequence until the iterations runs out or a solution sequence is found
        while (iterations < maxIterations):
            iterations += 1
            

            # Use best sequence to generate the final state
            neighbourSeq = bestSeq
            neigbourstate = state.clone()
            currentstate = state.clone()
            # create a neighbour seq
            for i in range(seqLen):
                if random.random() < coinFlip:
                    neighbourSeq[i] = random.choice(directions)
                else:
                    continue
            #  og sequence
            for s in bestSeq:
                currentstate.update(s["x"],s["y"])

            if (currentstate.checkWin()):
                return bestSeq
            # neighbour state
            for s in neighbourSeq:
                neigbourstate.update(s['x'],s['y'])
            
            # if heuristic cost lower than current then keep
            
            if getHeuristic(neigbourstate) < getHeuristic(currentstate):
                bestSeq = neighbourSeq
            

                



        #return the best sequence found
        return bestSeq  



# Genetic Algorithm code
class GeneticAgent(Agent):
    def getSolution(self, state, maxIterations=-1):
        #setup
        intializeDeadlocks(state)

        iterations = 0
        seqLen = 50             # maximum length of the sequences generated
        popSize = 10            # size of the population to sample from
        parentRand = 0.5        # chance to select action from parent 1 (50/50)
        mutRand = 0.3           # chance to mutate offspring action

        bestSeq = []            #best sequence to use in case iterations max out

        #initialize the population with sequences of POP_SIZE actions (random movements)
        population = []
        for p in range(popSize):
            bestSeq = []
            for i in range(seqLen):
                bestSeq.append(random.choice(directions))
            population.append(bestSeq)

        #mutate until the iterations runs out or a solution sequence is found
        while (iterations < maxIterations):
            iterations += 1

            #1. evaluate the population
            rankList = []
            for i in range(popSize):
                newState = state.clone()
                for s in population[i]:
                    newState.update(s['x'],s['y'])
                h = getHeuristic(newState)
                rankList.append((h,i))
            
            




            #2. sort the population by fitness (low to high)
            rankList.sort()
            sortedPopulation = []
            for i in range(popSize):
                sortedPopulation.append(population[rankList[i][1]])
            

            #2.1 save bestSeq from best evaluated sequence
            bestSeq = sortedPopulation[0]



            #3. generate probabilities for parent selection based on fitness
            sumTot = popSize*(popSize+1)/2
            probability = []
            for i in range(popSize):
                probability.append((popSize-i)/sumTot)




            #4. populate by crossover and mutation
            new_pop = []
            for i in range(int(popSize/2)):
                #4.1 select 2 parents sequences based on probabilities generated
                par1 = []
                par2 = []
                par1,par2 = random.choices(sortedPopulation, weights = probability, k =2)





                #4.2 make a child from the crossover of the two parent sequences
                offspring = []
                for i in range(seqLen):
                    if random.random() < parentRand:
                        offspring.append(par1[i]) 
                    else:
                        offspring.append(par2[i]) 

                



                #4.3 mutate the child's actions
                for i in range(seqLen):
                    if random.random() < mutRand:
                        offspring[i] = random.choice(directions)
                    else:
                        continue



                #4.4 add the child to the new population
                new_pop.append(list(offspring))


            #5. add top half from last population (mu + lambda)
            for i in range(int(popSize/2)):
                new_pop.append(sortedPopulation[i])


            #6. replace the old population with the new one
            population = list(new_pop)

        #return the best found sequence 
        return bestSeq


# MCTS Specific node to keep track of rollout and score
class MCTSNode(Node):
    def __init__(self, state, parent, action, maxDist):
        super().__init__(state,parent,action)
        self.children = []  #keep track of child nodes
        self.n = 0          #visits
        self.q = 0          #score
        self.maxDist = maxDist      #starting distance from the goal (heurstic score of initNode)

    #update get children for the MCTS
    def getChildren(self,visited):
        #if the children have already been made use them
        if(len(self.children) > 0):
            return self.children

        children = []

        #check every possible movement direction to create another child
        for d in directions:
            childState = self.state.clone()
            crateMove = childState.update(d["x"], d["y"])

            #if the node is the same spot as the parent, skip
            if childState.player["x"] == self.state.player["x"] and childState.player["y"] == self.state.player["y"]:
                continue

            #if this node causes the game to be unsolvable (i.e. putting crate in a corner), skip
            if crateMove and checkDeadlock(childState):
                continue

            #if this node has already been visited (same placement of player and crates as another seen node), skip
            if getHash(childState) in visited:
                continue

            #otherwise add the node as a child
            children.append(MCTSNode(childState, self, d, self.maxDist))

        self.children = list(children)    #save node children to generated child

        return children

    #calculates the score the distance from the starting point to the ending point (closer = better = larger number)
    def calcEvalScore(self,state):
        return self.maxDist - getHeuristic(state)

    #compares the score of 2 mcts nodes
    def __lt__(self, other):
        return self.q < other.q

    #print the score, node depth, and actions leading to it
    #for use with debugging
    def __str__(self):
        return str(self.q) + ", " + str(self.n) + ' - ' + str(self.getActions())


# Monte Carlo Tree Search Algorithm code
class MCTSAgent(Agent):
    def getSolution(self, state, maxIterations=-1):
        #setup
        intializeDeadlocks(state)
        iterations = 0
        bestNode = None
        initNode = MCTSNode(state.clone(), None, None, getHeuristic(state))

        while(iterations < maxIterations):
            #print("\n\n---------------- ITERATION " + str(iterations+1) + " ----------------------\n\n")
            iterations += 1

            #mcts algorithm
            rollNode = self.treePolicy(initNode)
            score = self.rollout(rollNode)
            self.backpropogation(rollNode, score)

            #if in a win state, return the sequence
            if(rollNode.checkWin()):
                return rollNode.getActions()

            #set current best node
            bestNode = self.bestChildUCT(initNode)

            #if in a win state, return the sequence
            if(bestNode and bestNode.checkWin()):
                return bestNode.getActions()


        #return solution of highest scoring descendent for best node
        #if this line was reached, that means the iterations timed out before a solution was found
        return self.bestActions(bestNode)
        

    #returns the descendent with the best action sequence based
    def bestActions(self, node):
        #no node given - return nothing
        if node == None:
            return []

        bestActionSeq = []
        while(len(node.children) > 0):
            node = self.bestChildUCT(node)

        return node.getActions()


    ####  MCTS SPECIFIC FUNCTIONS BELOW  ####

    #determines which node to expand next
    def treePolicy(self, rootNode):
        curNode = rootNode
        visited = []

        while not curNode.checkWin():
            curNode.getChildren([])
            for c in curNode.children:
                if c.n ==0:
                    return c
            curNode = self.bestChildUCT(curNode)

        return curNode



    # uses the exploitation/exploration algorithm
    def bestChildUCT(self, node):
        c = 1               #c value in the exploration/exploitation equation
        bestChild = None

        children = node.getChildren([])
        uctlist = []
        for child in children:
            if child.n !=0:
                UCT = child.q/child.n +c*(2*math.log(node.n)/child.n)**0.5
                uctlist.append((UCT,child))
            else:
                continue

        uctlist.sort()
        bestChild = uctlist[-1][1]
        return bestChild



     #simulates a score based on random actions taken
    def rollout(self,node):
        numRolls = 7        #number of times to rollout to

        newState = node.state.clone()
        for i in range(numRolls):
            if newState.checkWin():
                return node.calcEvalScore(newState)
            action = random.choice(directions)
            newState.update(action['x'],action['y'])
        
        return node.calcEvalScore(newState)



     #updates the score all the way up to the root node
    def backpropogation(self, node, score):
        
        while node is not None:
            node.q+=score
            node.n+=1
            node = node.parent

        return 0