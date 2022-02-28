from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

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
for row in results_df.itertuples():
    title = row[3]
    genre = row[6]
    lyricist = row[9]
    date = row[11]
    influencingArtist = row[14]

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
            "date": date
        }

print(songDict)


file1 = open("MyFile.krf","a", encoding="utf-8")
for genre in genreDict.keys():
    file1.write("(isa %s genre) \n" % genre.replace(" ", ""))


print(musicianDict)
for musician in musicianDict.keys():
    file1.write("(isa %s musician) \n" % musician.replace(" ", ""))
    for influencer in musicianDict[musician]:
        file1.write("(influencedBy %s %s) \n" % (musician.replace(" ", ""), influencer.replace(" ","")))

for title in songDict.keys():
    date = songDict[title]["date"].replace(" ", "")

    file1.write(";;; " + title + "\n")
    file1.write("(isa %s song) \n"%title.replace(" ", ""))
    file1.write("(isa %s date) \n" %date)
    for genre in songDict[title]["genres"]:
        file1.write("(inGenre %s %s) \n" % (title.replace(" ", ""), genre.replace(" ", "")))
    for lyricist in songDict[title]["lyricists"]:
        file1.write("(isWrittenBy %s %s) \n" % (title.replace(" ", ""), lyricist.replace(" ", "")))

    file1.write("(hasPublishDate %s %s) \n" %(title.replace(" ", ""), date))


    file1.write(";;; \n")
    file1.write("\n")

file1.close()
