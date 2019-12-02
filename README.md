# ONSA - Python representation of ogame player state

*Defending Our Empire. Securing the Future.*
* * * 

oGame is an  massive multiplayer online game (MMO) intially written in PHP.
The style is comparable to Command and Conquer series if you cut out the fun.
This code base tries to serve as a basis for other projects.


## other projects
A quick search on github reveals that most other projects are written either in JavaScript or PHP.
My weapon of choice is Python.

|  |  |
|----|----|
|[alaingilbert/pyogame](https://github.com/alaingilbert/pyogame) | python3, focus on API interaction in-game usage is sanctioned. code parts and ideas of his work are used here |
|[esp1337/ogame-testing](https://github.com/esp1337/ogame-testing) | python2, undocumented|


## stellar objects

 - universe
   - galaxy
     - solar system
       - planet
         - moon

## planet specific objects
 - facilities
 - buildings
 - ships
 - defence
 
## player specific objects 
 - research


## constants
Supports a mapping between values returned by public API endpoints
and objects within the game. Thanks to the work of Alain Gilbert (@alain_gilbert) from which 
the values were taken.
