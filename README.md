# Goblin Game [name tbd]

This is a game revolving around a goblin that no longer wishes to serve in a dungeon.


## TODO
 - upgrade to python 3.7
 - exit vs stop doing different things
 -  might want to revisit describe inventory flow: might confuse players as it does not tell you what to do after. 
 - "WHAT SHOULD I DO?" command always gives hint?
 - should save every now and then or ppl lose progress on a crash
 - Look into talestreamer alternatives for the main announcer
 - Add ability to reset the game (basically add an options menu)
 - Use packages/folders to start logically grouping these classes.
 - Something to tell you "welcome back" when you restore state from DB. - right now when it comes back it comes back and gives the input_action as LAUNCH so it goes into the else
 - Add ability to describe inventory
 - Things taken in inventory must no longer be there when described again. - Code for this now available, just need to use it.
 - Remove things from inventory when used up, but do not allow them to be-picked up from their original spot - Code for this now available, just need to use it.
 - Do not allow actions is certain events have already taken place/certain things are already in inventory - Code for this now available, just need to use it.
 - Find a better way to do force change state from events (example in keeper trapper)