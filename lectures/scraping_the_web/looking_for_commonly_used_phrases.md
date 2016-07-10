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

