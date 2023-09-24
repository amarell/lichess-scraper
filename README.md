# Data collector

This data collector is responsible for collecting wide amounts of data from Lichess.

More specifically, it is used to collect data about games played by random users on Lichess, which will be used by a machine learning prediction model.

## User traversal algorithm

1. Inputs:
   - `n` - number of wanted games
   - `start_user` - the first user from which to start the traversal (selected randomly)
   - `history_offset` - number of games to keep in history
   - `max_elo_treshold` - maximum ELO rating after which it should start decreasing
   - `min_elo_treshold` - minimum ELO rating after which it should start increasing
2. Start at a `start_user`
3. If their rating is crossing the `max_elo_treshold`:
   - Go to the player that they had the worst defeat against
4. If their rating is crossing the `min_elo_treshold`:
   - Go the the player that they had the best victory against
5. If neither, then it will go in the current direction. By default, the first direction is upwards.
6. Repeat the steps for the next player until the number of collected games reaches `n`

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
