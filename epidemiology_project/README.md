This Python project, completed in Winter 2017, uses matplotlib 
to simulate a viral outbreak on the island of manhattan. It is heavily simplified,
compared to actual models, since in real life there are more parameters than just 
"mortality".

This is meant to work on Spyder, a IDE provided by Anaconda.

Here are the directions to run the simulation:
On the python console, type:
	m = read_map('nyc_map.csv')
	m.display()
this should dusplay a map of nyc, all in green.
Every point in the map represents a Cell. Each cell is either
-green, for being susceptible to disease
-gray, for being immune
-Red for infected

To infect a cell, type this on Pythin consose
	m.cells[(39, 82)].infect()
In the place of (39, 82), you can type any (y coordinate, x coordinate)

After 1, or any amount of cells are set to be infected, we type
	m.time_step()
This sumulates that time has passed, and wil display the nyc map after the 
infection spreads. 
repeating
	m.time_step()
will keep allowing the disease to spread, intil immunity happens, or all of manhattan is infected

