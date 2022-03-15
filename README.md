# CS371-Term-Project-2022
Knowledge-based approach to a song recommendation system. Designed as a final term project for CS 371 Knowledge Representation and Reasoning at Northwestern University in Winter 2022. 

## Source Knowledge
The knowledge used in this system is sourced from Wikidata. 

## Encoded Knowledge
The data from Wikidata was transformed into krf format to allow for use of Companions and FIRE querying. The transformed knowledge can be found in songDetails.krf.

## Microtheory Files
There are three files that makeup the MusicRecommenderMt microtheory: songDetails.krf, songPreds.krf, and hornclauses.krf.

`songDetails.krf` contains the knowledge from Wikidata.
`songPreds.krf` defines the predicates that our team used to define attributes of songs.
`hornclauses.krf` contains the horn clauses that our team used to reason with the knowledge and ultimately recommend a song.

## Horn Clauses
