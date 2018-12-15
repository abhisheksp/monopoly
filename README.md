# Monopoly Game Implementation

# Tested with Python 3.6

# Contribution Guidelines
* create a new branch and raise a pull request(include Trello Story Link in the PR)
* include story number in commit message, example commit message : #1: add project skeleton
* PEP 8 standards(with few exceptions, use of lambdas)

# Running Tests
run the command on project root: `python -m unittest discover`


# Structure
* unit tests are located in a separate package named `tests` for each python package.
* `game_phases` describe the various game phases which all conform to the game_phase interface(State Pattern)
* each game phase should be self explanatory(refer to respective unit tests for better understanding) and isolate code related to that game phase.


Note to reviewer: our biggest strength here is the well structured and easily readable code with high unit test coverage