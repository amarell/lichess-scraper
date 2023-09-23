# Data collector

This data collector is responsible for collecting wide amounts of data from Lichess.

More specifically, it is used to collect data about games played by random users on Lichess, which will be used by a machine learning prediction model.

## User traversal algorithm

This simple algorithm is used to collect games from players of all levels.

1. Start at a random user
2. Get their biggest loss
   - Repeat steps for their opponent
3. Get their biggest win
   - Repeat steps for their opponent
  
> Currently using a different algorithm, as I'm not sure I can get this info through Lichess API.

## Output

The data should be collected in a .CSV format.

One CSV record essentially represents the features of the game that was played and should contain the following fields:

1. White ELO
2. Black ELO
3. PGN (with time annotations)
4. ...

# IDEAS

- Real time prediction using Lichess streaming API
- Feeding real time data into a prediction algorithm
