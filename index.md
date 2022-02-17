# Sokoban Puzzle Solver
---
## AI based puzzle solver
Sokoban is a crate pushing puzzle game with an objective to push the crates onto the designated goal areas without creating deadlock states. You can play the [game online](https://www.mathsisfun.com/games/sokoban.html) to quickly understand it. I implemented several AI agents based on Evolutionary search, Monte Carlo Tree Search, A Star search, and simple Breadth First & Depth First search to illustrate the effectiveness of these algorithms in finding a solution. You can see the solution play out as an animation by following the installation guide below.
## Preview
Here is the preview of one of the solutions found by the AI agent.<br/>
![gif of agent finding a solution](https://github.com/dhyani15/Sokoban-Agent/blob/main/assets/graphics/sokoban%20preview.gif)
## Installation guide
Requires Python 3.8 to run
##### Install libraries
`$ pip install -r requirements.txt`
## Run the Game

##### Solve as a human
`$ python3 game.py --play`
`$ python3 game.py --agent Human`
##### Solve with an agent
`$ python3 game.py --agent [AGENT-NAME-HERE]`

`$ python3 game.py --agent BFS #run game with BFS agent`

`$ python3 game.py --agent AStar --no_render #run game with AStar agent without rendering`

##### Solve with fast_game.py
`$ python3 game.py --agent [AGENT-NAME-HERE]`

`$ python3 fast_game.py --agent BFS #run all 100 levels with BFS agent`

`$ python3 fast_game.py --agent HillClimber -trials 3 #run all 100 levels 3 times with HillClimber agent`

## Parameters
`--play` - run the game as a human player

`--no_render` - run the AI solver without showing the game screen 

`--agent [NAME]`  - the type of agent to use [Human, DoNothing, Random, BFS, DFS, AStar, HillClimber, Genetic, MCTS]

`--level [#]` - which level to test (0-99) or 'random' for a randomly selected level that an agent can solve in at most 2000 iterations. These levels can be found in the 'assets/gen_levels/' folder (default=0)

`--iterations [#]` - how many iterations to allow the agent to search for (default=3000)

`--solve_speed [#]` - how fast (in ms) to show each step of the solution being executed on the game screen 

`--trials [#]` - number of repeated trials to run the levels for _(used only in fast_game.py)_ (default=1)

## Agent Types

#### Agent_py
* **Agent()** - base class for the Agents
* **RandomAgent()** - agent that returns list of 20 random directions
* **DoNothingAgent()** - agent that makes no movement for 20 steps

* **BFSAgent()** - agent that solves the level using Breadth First Search
* **DFSAgent()** - agent that solves the level using Depth First Search
* **AStarAgent()** - agent that solves the level using A* Search
* **HillClimberAgent()** - agent that solves the level using HillClimber Search algorithm
* **GeneticAgent()** - agent that solves the level using Genetic Search algorithm
* **MCTSAgent()** - agent that solves the level using Monte Carlo Tree Search algorithm
