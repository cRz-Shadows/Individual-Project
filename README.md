# Pokémon Simulator Environment

Here we have an environment for running many Pokémon simulations in the command line. The Pokémon-showdown directory contains a modified version of https://github.com/smogon/pokemon-showdown, whose modifications are detailed below. In the Data directory, you can find various python files which can be used to build teams from predefined text files of builds written in Pokémon Showdown output format, run large sets of multithreaded simulations, and parse and analyse the results of battles, producing a variety of graphs. Additionally, some predefined inputs for various formats can be found in Data/Inputs. See manual.md for instructions on how to use the python files.



## .gitignore

All of the output files have been put in the gitignore. This is because these files are hundreds of gigabytes and cannot reasonably be uploaded to github. They also can be created by running the set of simulations yourself! Additionally the JSON files containing the battles to run have also been ignored, since these can be easily produced using the python files and also take up tens of gigabytes. I have uploaded the output matrices, meaning my results can still be seen and used for analysing. Additionally the graphs folder has been gitignored, since analyseOutputMatrix.py produces all of these graphs anyway.



## Modifications to Pokémon Showdown

* The code for our heuristics based bot can be found in "Individual-Project/pokemon-showdown/sim/examples/Simulation-test-1.ts".

* In the file "Individual-Project/pokemon-showdown/sim/pokemon.ts," the "getSwitchRequestData()" function has been modified to include additional information for each Pokémon in each request message sent through the battle stream. Specifically, the modifications added information on the Pokémon's current boost table, its position on the battlefield, its maximum possible HP, and any status effects applied to it.

* In the file "Individual-Project/pokemon-showdown/sim/side.ts," the "getRequestData()" function has been modified to include information on any current side conditions on the battlefield, such as tailwind or trick room. Additionally, information on the foe has been added.

* In the file "Individual-Project/pokemon-showdown/sim/dex-moves.ts," line 505 has been modified to allow for checking how many times a multi-hit move hits.

* In the file "Individual-Project/pokemon-showdown/sim/tools/random-player-ai.ts," modifications have been made to take into account the "_should_dynamax()" function rather than just dynamaxing if possible. All calls to "chooseMove()," "chooseSwitch()," "choosePokemon()," and "chooseTeamPreview()" have also been modified to pass in requests so that the bot can use that data when selecting what to do.