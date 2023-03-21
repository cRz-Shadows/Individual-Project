The code for our heuristics based bot can be found in "Individual-Project/pokemon-showdown/sim/examples/Simulation-test-1.ts".

In the file "Individual-Project/pokemon-showdown/sim/pokemon.ts," the "getSwitchRequestData()" function has been modified to include additional information for each Pokémon in each request message sent through the battle stream. Specifically, the modifications added information on the Pokemon's current boost table, its position on the battlefield, its maximum possible HP, and any status effects applied to it.

In the file "Individual-Project/pokemon-showdown/sim/side.ts," the "getRequestData()" function has been modified to include information on any current side conditions on the battlefield, such as tailwind or trick room. Additionally, information on the foe has been added.

In the file "Individual-Project/pokemon-showdown/sim/dex-moves.ts," line 505 has been modified to allow for checking how many times a multi-hit move hits.

In the file "Individual-Project/pokemon-showdown/sim/tools/random-player-ai.ts," modifications have been made to take into account the "_should_dynamax()" function rather than just dynamaxing if possible. All calls to "chooseMove()," "chooseSwitch()," "choosePokemon()," and "chooseTeamPreview()" have also been modified to pass in requests so that the bot can use that data when selecting what to do.