# PokeQuiz
This quiz will iterate through a randomly shuffled list of pokemon for the user to guess on.
Incorrect answers are put into a folder labeled `guesses` with text above the pokemon for what the guess was.


## Operation
Launching the quiz will start with asking if you want to clear the contents of `guesses` if it exists, then will ask you to choose starting and ending dex numbers, these can be anything within bounds.

## Post quiz
At the end of the quiz a matplot graph will be displayed showing each dex number along with the time in seconds taken to guess

## Other Things to know
`Nidoran♀` and `Nidoran♂` are labeled NiroranF and NidoranM respectively. The Quiz is not case sensitive, however it does not modify whitespace so having an extra space will result in wrong answer

## To Do
Implement continuing and potentially pausing