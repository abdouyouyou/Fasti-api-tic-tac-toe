# Play TicTacToe!... <sub>Through Fast Api</sub>
In short you play TicTacToe through an API.

## the /start path :
Creates a game instances for the client and return the game_id for the client to attach in any further requests.

## the /playmove path : 
Expects an Argument in the form of a JSON paylod containing the game_id the xposition and yposition on the grid

## the background cleanup : 
the couroutine cleanup handles the control of idle games in order to make sure that only active games are kept, the couroutine is contained in a task which is created and destroyed in the lifespan couroutine of the FastApi app.

