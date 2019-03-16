from PD.TextAnalyzer import TextAnalyzer
tr = TextAnalyzer()
tr.get_query_from_file()
tr.get_collection_from_google()
tr.run_rabin_karp()
tr.sentence_rabin_karp()
print(tr.get_scores_and_url())

#print(tr.get_ten_most_relevant())
