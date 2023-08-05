# plants_and_animals
a game emulates the life and surviving of defferent creatures  

there are 3 types (species) of animals: *prey, predator* and *omni*:
- *preys* are herbivorous, they can eat only *plants*
- *predators* are carnivorous, they can eat only other animals
- *omni* are omnivorous, they can eat both animals and plants.

plant can be poison, and an animal that tries to eat it will die.  

by default, there would be 

all creatures have such attributes as *coordinates, age, mass, max age* and *aggression*.  
animals have special attributes: *health, hunger* and *power*, which are important for fighting.

if two creatures are in the same spot, they fight. predators and omnis attack only if they are hungry or angry. the one with higher lever of _power_ wins.  
critical levels of aggression and hunger are at the beggining of the code.

every day every creature gets older. if it is too old, it dies.  
if animal is too hungry, it dies.

when everybody dies, game is over (happy end!)

# running
to run the game:  
```
$ python3 main.py
```
then you would need to specify the size of the spawn field and number of creatures. (every spiece is a quarter of total number)  
every action, such as fight or death, would be in the log:
` omni 303 ate prey 41  
predator 808 ate prey 113  
predator 392 ate prey 137  
423 unsuccessful attacked 193  
`
as you can see, every creature is reffered by its species and number

---
that's it. good luck.
