#Looking for commonly used phrases

Up until this point we've mostly taken a frequency of our data.  Nothing that interesting.  We were able to use this data to discern real insights.  The types of questions we've answer up until this point are mostly of the form:

Of the ads being posting - how many of them are likely connected by some hard attribute?

Now we take that analysis a simple step further - 

Of the ads being posted with a common hard attribute, what would happen if we looked for further connections between ads with different hard attributes?  And further, can we use this new information to draw real connections between specific ads or between clusters of ads?

###Here's how will do this in general

1. Pick a hard attribute

2. Partition the set of ads into categories with the same hard attribute 

3. Look for some way of drawing connections between the ads that are in different categories.  

###Here's what we'll do in specific

1. Pick a hard attribute - we have two - phone numbers and location (using external data).

2. Partition the set of ads into categories with the same hard attribute - if two ads have the same phone number, they are in the same category.  Or if we were doing geographic analysis - If two ads are close enough, they are in the same category.  Just to make that statement concrete, say that all ads within 1 mile radius are in the same category.  Or all ads within a neighborhood are in the same category.  Or all ads with similar demographic features, such as average income or average age are in the same category.

3. Look for some way of drawing connections between the ads that are in different categories.  Since we have the full ad at our disposal we'll first look at language of the advertisement.  We'll use this to determine how similar the phrases are across all ads of a given category or between categories.  This will give us a sense of how much overlap there is in the language.  This can give us a loose sense of how much posters are reading the ads of others.  It may also give clues to law enforcement of how to speak with the most frequently used terms, in order to sound like a buyer of commercial sex.  Using this, a law enforcement representative could pose as a buyer more convincingly and conduct a "buy".  

###How the code works

The major work horse of our analysis will be the n-gram.  The n-gram of a sentence is all words of the sentence split up into grams of length n.  

So the sentence: 

"Hello there I'm Eric" 

Would be:   

["Hello","there"]
["there","I'm"]
["I'm","Eric"]

If n=2.

This allows us to isolate each document into a set of phrases, that can be removed from their original context.  So we are only looking for lingo right now - the shallowest level of textual analysis, we need only consider this simple model.

Here is the code for creating n-grams in general:

```
def ngrams(sentence,n):
    sentence = sentence.replace("\n"," ").replace("\r"," ")
    sentence = sentence.replace("\n"," ").replace("\r"," ")
    input_list = [elem for elem in sentence.split(" ") if elem != '']
    return list(zip(*[input_list[i:] for i in range(n)]))
```

Using this we'll look at the phrase frequency amongst a set of ads.  The idea is pretty simple - how often does a poster using the same number use the same phrases?  

Here's how I check for that:

from [nlp_tools.py](https://github.com/EricSchles/investigator/blob/master/code/investigator/app/nlp_tools.py)

```
def phrase_frequency(documents,max_ngram_size=10):
    documents = "\n".join([document.lower() for document in documents])
    ngrams_doc= [ngrams(documents,i) for i in range(1,max_ngram_size)]
    
    similarity_scores = {}
    [similarity_scores.update({}.fromkeys(phrases,{"absolute frequency":1,"relative frequency":1})) for phrases in ngrams_doc] 
    for i_gram in range(0,len(ngrams_doc)):
        for index,elem in enumerate(ngrams_doc[i_gram]):
            if elem in ngrams_doc[i_gram][:index] or elem in ngrams_doc[i_gram][index+1:]:
                similarity_scores[elem]["absolute frequency"] += 1            
        similarity_scores[elem]["relative frequency"] = similarity_scores[elem]["absolute frequency"]/float(len(ngrams_doc[i_gram]))
    return similarity_scores
```

What's happening here is I first join all the documents together and then generate all n-grams from 1 word, to the max specified.  My rule of thumb is to not go beyond n-grams, where n=10.  I don't have much imperical justification for this.  But 10 is a fairly safe upper bound.  Most of the learnign happens for grams of size 2 or 3.  

Then all i do is count up every time I see that phrase, other than it's current index.  If a phrase is repeated it's count will increase, in therefore it is words are more frequently used together.


Let's see how to make use of this to do some real analysis with phone numbers:

from [metric_generation.py](https://github.com/EricSchles/investigator/blob/master/code/investigator/app/metric_generation.py)

```
def overall_comparison():
    total_ads = [elem.ad_body for elem in BackpageAdInfo.query.all()]
    return phrase_frequency(total_ads)

def phrase_frequency_categorized_by_phone_number():
    ads = {}
    for ad in BackpageAdInfo.query.all():
        if ad.phone_number and (len(ad.phone_number) == 10 or len(ad.phone_number) == 11):
            if ad.phone_number in ads:
                ads[ad.phone_number] += "\n" + ad.ad_body
            else:
                ads[ad.phone_number] = ad.ad_body
    
    phrase_frequency_per_phone_number = {}
    for ad in ads.keys():
        phrase_frequency_per_phone_number[ad] = phrase_frequency(ads[ad])
    return phrase_frequency_per_phone_number
```

The first method just looks at all the documents to see how often people are using the same phrases overall.  

The second way we make use of ngrams is by doing a rough approximating of overall document similarity.  What we are really looking is looking at overall phrase similarity.  For this we'll make use of a method called `document_similarity` in the [nlp_tools.py](https://github.com/EricSchles/investigator/blob/master/code/investigator/app/nlp_tools.py) file:

```
def document_similarity(document_a,document_b,max_ngram_size=10):
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
```

We'll use this to get average phrase similarity between categories by phone number:

This is found in [metric_generation.py](https://github.com/EricSchles/investigator/blob/master/code/investigator/app/metric_generation.py):

```
def average_phrase_similarity_between_documents_by_phone_number(number_of_grams=10,profiling=False):
    ads = {}
    for ad in BackpageAdInfo.query.all():
        if ad.phone_number and (len(ad.phone_number) == 10 or len(ad.phone_number) == 11):
            if ad.phone_number in ads:
                ads[ad.phone_number] += "\n" + ad.ad_body
            else:
                ads[ad.phone_number] = ad.ad_body
    checklist_of_nodes_to_process = generate_connected_graph([key for key in ads.keys()])
    average_per_gram = {}.fromkeys([elem for elem in range(1,number_of_grams)],0)
    total = 0
    
    for key in checklist_of_nodes_to_process:
        if profiling:
            print(len(checklist_of_nodes_to_process[key]),"total nodes to process")
        if profiling: start = time.time()
        for list_item in checklist_of_nodes_to_process[key]:
            similarity_scores = document_similarity(ads[key],ads[list_item])
            total += 1
            for i_gram in similarity_scores.keys():
                average_per_gram[i_gram] += similarity_scores[i_gram]
        if profiling: print(time.time() - start)
    average_per_gram = {key:average_per_gram[key]/total for key in average_per_gram.keys()}
    return average_per_gram
```

From here we see can get an approximate sense of how much people are using different kinds of phrases.  And how much overlap on average there is between posters, representing different possible traffickers.  

Let's see our methods in action to get insight about how much posters use the same kinds of terminology:

This data was collected over the course of a month and scraping for around 10 hours in total.  

