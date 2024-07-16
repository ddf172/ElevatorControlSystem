Elevator Control System for systems with some n number of Floors, and m number of Elevators and c Capacity of the elevator in real life systems.
Main purpose is to create a working in real time system that finds optimal or close to optimal solution to elevator movement.

This program uses a Evolutionary Algorithm and some features from Tabu Search to find heuristic solution in a short peroid of time that asserts good quality of solution
and meets the assumptions of a problem.

Last working version: GUI VERSION (commit name)
Currently in procces of restructurizing and rebuilding of a program

New idea:
  - Use distinct Tabu Search to generate and repair elvator paths
  - Do a benchmark of several crossovers to find the best one
  - Move all settings to distinct class responsible for configuration
  - Make a better structure
  - Change system simulation so it runs more real life like than turn-based:
      Divide each second into sectros depending on system requirements
      Treat each sector like submove in which algorithm can get recalculated if new person apperas or state of systems changes to find better solution
      Preserve the integrity of algorithm and elevator movment and not allow to change move mid-travel in those submove sectors
