def ngrams(sentence,n):
    sentence = sentence.replace("\n"," ").replace("\r"," ")
    input_list = [elem for elem in sentence.split(" ") if elem != '']
    return list(zip(*[input_list[i:] for i in range(n)]))

def document_similarity(document_a,document_b,max_ngram_size=10):
    """
    Here we compute document similarity by looking at i-grams of up to length max_ngram_size.
    We can use this to inspect data across some further semantic divide.  For example,
    assume we have split ads by phone number and then joined all ads with the same phone number.
    This function could be used to examine the phrase similarity between two given phone numbers
    across many ads.  Or if you like, it could be used to consider all ads pairwise, based on split by
    phone number.

    @document_a - each document is defined above, across some semantic split.  It is of type string
    @document_b - the same as document_a except with some categorical value that is different
    @max_ngram_size - the default size is 10.  This is an integer and states how many grams to split into
    a 2-gram is words of 2 groups, a 3-gram is words of group length 3.
    To see this in action, I recommend running the ngrams function (defined above) with a string, number of grams as input.

    """
    document_a,document_b  = document_a.lower(),document_b.lower()
    ngrams_doc_a = [ngrams(document_a,i) for i in range(1,max_ngram_size)]
    ngrams_doc_b = [ngrams(document_b,i) for i in range(1,max_ngram_size)]
    similarity_scores = []
    for i_gram in range(0,len(ngrams_doc_a)):
        similarity_count = 0
        for elem_a in ngrams_doc_a[i_gram]:
            if elem_a in ngrams_doc_b[i_gram]:
                similarity_count += 1
        similarity_scores.append(similarity_count/float(len(ngrams_doc_a[i_gram])))
    similarity_score_with_n_grams = {}
    for index in range(0,len(ngrams_doc_a)):
        similarity_score_with_n_grams[index+1] = similarity_scores[index]
    return similarity_score_with_n_grams

def phrase_frequency(documents,max_ngram_size=10):
    """
    Here we compute phrase frequency over a set of documents.  This gives us the absolute frequency of how often a phrase was used,
    as well as the relative frequency that the term was used compared to all other terms of the same gram size.

    
    """
    documents = "\n".join([document.lower() for document in documents])
    ngrams_doc= [ngrams(document,i) for i in range(1,max_ngram_size)]
    
    similarity_scores = {}
    [similarity_scores.update({}.fromkeys(phrases,1)) for phrases in ngrams_doc] 
    for i_gram in range(0,len(ngrams_doc)):
        for index,elem in enumerate(ngrams_doc[i_gram]):
            if elem in ngrams_doc[i_gram][:index] or elem in ngrams_doc[i_gram][index+1:]:
                similarity_scores[elem]["absolute frequency"] += 1            
        similarity_scores[elem]["relative frequency"] = similarity_scores[elem]["absolute frequency"]/float(len(ngrams_doc_a[i_gram]))
    return similarity_scores
 
