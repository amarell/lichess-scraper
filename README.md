# Data collector

This data collector is responsible for collecting wide amounts of data from Lichess.

More specifically, it is used to collect data about games played by random users on Lichess, which will be used by a machine learning prediction model.

## User traversal algorithm

<del>
1. Start at a random user
2. Get their biggest loss
   - Repeat steps for their opponent
3. Get their biggest win
   - Repeat steps for their opponent
</del>

1. Start at a random user
2. If their rating is crossing the max threshold:
   - Go to the player that they had the worst defeat against
3. If their rating is crossing the min threshold:
   - Go the the player that they had the best victory against

This way we are ensuring a diverse dataset that contains games played at all levels.

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
