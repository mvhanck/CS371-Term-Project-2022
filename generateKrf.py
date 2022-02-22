from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd

sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

# From https://www.wikidata.org/wiki/Wikidata:SPARQL_query_service/queries/examples#Cats
sparql.setQuery("""
SELECT ?itemLabel ?genreLabel ?writerLabel ?dateLabel ?langLabel
WHERE
{
    ?item wdt:P31 wd:Q7366 .
    ?item wdt:P136 ?genre .
    ?item wdt:P676 ?writer .
    ?item wdt:P577 ?date .
    ?item wdt:P407 ?lang .
    SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
}
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()

results_df = pd.json_normalize(results['results']['bindings'])
# print(results_df.info)
# print(results_df[['item.value', 'itemLabel.value']].head())
songDict = {}
for row in results_df.itertuples():
    title = row[3]
    genre = row[6]
    lyricist = row[9]
    date = row[11]
    lang = row[14]

    if title in songDict:
        if genre not in songDict[title]["genres"]:
            songDict[title]["genres"].append(genre)
        if lyricist not in songDict[title]["lyricists"]:
            songDict[title]["lyricists"].append(lyricist)
    else:
        songDict[title] = {
            "genres" : [genre],
            "lyricists" : [lyricist],
            "date": date,
            "language": lang
        }

print(songDict)


file1 = open("MyFile.txt","a", encoding="utf-8")
for title in songDict.keys():
    date = songDict[title]["date"].replace(" ", "")
    lang = songDict[title]["language"].replace(" ", "")

    file1.write(";;; " + title + "\n")
    file1.write("(isa %s song) \n"%title.replace(" ", ""))
    file1.write("(isa %s date) \n" %date)
    file1.write("(isa %s language) \n" %lang)
    for genre in songDict[title]["genres"]:
        file1.write("(isa %s genre) \n" %genre.replace(" ", ""))
        file1.write("(inGenre %s %s) \n" % (title.replace(" ", ""), genre.replace(" ", "")))
    for lyricist in songDict[title]["lyricists"]:
        file1.write("(isa %s lyricist) \n" %lyricist.replace(" ", ""))
        file1.write("(isWrittenBy %s %s) \n" % (title.replace(" ", ""), lyricist.replace(" ", "")))

    file1.write("(hasPublishDate %s %s) \n" %(title.replace(" ", ""), date))
    file1.write("(inLanguage %s %s) \n" % (title.replace(" ", ""), lang))


    file1.write(";;; \n")
    file1.write("\n")

file1.close()
