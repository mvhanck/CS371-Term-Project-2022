from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
import re

sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

# From https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/queries/examples#Cats
sparql.setQuery("""
SELECT ?itemLabel ?genreLabel ?writerLabel ?dateLabel ?influenceLabel
WHERE
{
    ?item wdt:P31 wd:Q7366 .
    ?item wdt:P136 ?genre .
    ?item wdt:P676 ?writer .
    ?item wdt:P577 ?date .
    ?writer wdt:P737 ?influence .
    SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
}
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

results_df = pd.json_normalize(results['results']['bindings'])
# print(results_df.info)
# print(results_df[['item.value', 'itemLabel.value']].head())
songDict = {}
musicianDict = {}
genreDict = {}
yearDict = {}
for row in results_df.itertuples():
    title = row[3]
    genre = row[6]
    lyricist = row[9]
    date = row[11]
    influencingArtist = row[14]

    date = re.sub('[^A-Za-z0-9]+', '', date)
    year = date[0:4]

    if year not in yearDict:
        yearDict[year] = 1

    if genre not in genreDict:
        genreDict[genre] = 1
    if lyricist not in musicianDict:
        musicianDict[lyricist] = []
    if influencingArtist not in musicianDict:
        musicianDict[influencingArtist] = []

    if influencingArtist not in musicianDict[lyricist]:
        musicianDict[lyricist].append(influencingArtist)

    
    if title in songDict:
        if genre not in songDict[title]["genres"]:
            songDict[title]["genres"].append(genre)
        if lyricist not in songDict[title]["lyricists"]:
            songDict[title]["lyricists"].append(lyricist)
    else:
        songDict[title] = {
            "genres" : [genre],
            "lyricists" : [lyricist],
            "date": year
        }

print(songDict)


file1 = open("MyFile.krf","a", encoding="utf-8")
for genre in genreDict.keys():
    genreNew =  re.sub('[^A-Za-z0-9]+', '', genre)
    file1.write("(isa %s Genre) \n" %genreNew)

for year in yearDict.keys():
    file1.write("(isa %s Year) \n" %year)

print(musicianDict)
for musician in musicianDict.keys():
    musicianNew = re.sub('[^A-Za-z0-9]+', '', musician)
    file1.write("(isa %s Musician) \n" % musicianNew)
    for influencer in musicianDict[musician]:
        influencerNew = re.sub('[^A-Za-z0-9]+', '', influencer)
        file1.write("(influencedBy %s %s) \n" %(musicianNew, influencerNew))

for title in songDict.keys():

    date = songDict[title]["date"]
    titleNew = re.sub('[^A-Za-z0-9]+', '', title)

    file1.write(";;; " + title + "\n")
    file1.write("(isa %s Song) \n"%titleNew)

    for genre in songDict[title]["genres"]:
        genreNew = re.sub('[^A-Za-z0-9]+', '', genre)
        file1.write("(inGenre %s %s) \n" % (titleNew, genreNew))
    for lyricist in songDict[title]["lyricists"]:
        lyricistNew = re.sub('[^A-Za-z0-9]+', '', lyricist)
        file1.write("(isWrittenBy %s %s) \n" % (titleNew, lyricistNew))

    file1.write("(hasPublishYear %s %s) \n" %(titleNew, date))


    file1.write(";;; \n")
    file1.write("\n")

file1.close()
