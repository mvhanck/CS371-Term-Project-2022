# CS371-Term-Project-2022
Knowledge-based approach to a song recommendation system. Designed as a final term project for CS 371 Knowledge Representation and Reasoning at Northwestern University in Winter 2022. 

## Source Knowledge
The knowledge used in this system is sourced from Wikidata. 

## Encoded Knowledge
The data from Wikidata was transformed into krf format to allow for use of Companions and FIRE querying. The transformed knowledge can be found in songDetails.krf.

## Microtheory Files
There are three files that makeup the MusicRecommenderMt microtheory: songDetails.krf, songPreds.krf, and hornclauses.krf.

`songDetails.krf` contains the knowledge from Wikidata. <br /
`songPreds.krf` defines the predicates that our team used to define attributes of songs.
`hornclauses.krf` contains the horn clauses that our team used to reason with the knowledge and ultimately recommend a song.

## Horn Clauses

### Sameness
**(sameGenre ?song1 ?song2)** finds songs of the same genre as **song1**.
**(sameYear ?song1 ?song2)** finds songs published in the same year as **song1**.
**(sameMusician ?song1 ?song2)** finds songs performed by the same musician as **song1**.
**(sameInfluence ?song1 ?song2)** finds songs who are sung by musicians who share the same musical influence.

### Similarity
**(similarSongGeneral ?inputsong ?outputsong)** finds songs that are in the same genre and whose musicians share a musical influence. 
**(similarSongOnAlbum ?inputsong ?outputsong)** finds songs that are performed by the same musician and published in the same year, indicating that they are probably on the same album.

### Recommendation
**(recommendSimilarSong ?inputsong ?outputsong)** finds songs that are either **similarSongGeneral** or **similarSongOnAlbum**. 
