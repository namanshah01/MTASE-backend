from rake_nltk import Rake

def keyword_extractor(DOCUMENT):
    rake_nltk_var = Rake()
    text = DOCUMENT
    rake_nltk_var.extract_keywords_from_text(text)
    keywords_extracted = rake_nltk_var.get_ranked_phrases()[:7]
    # print(keywords_extracted)
    
    return (keywords_extracted)