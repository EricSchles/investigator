#A Trivial Example

Getting started with web scraping is pretty straight forward.  However the skill level needed to do web scraping right goes from simple to intermediate to advanced.  We'll try to treat each of the necessary pieces in kind, moving through different types of concerns section by section.  By the end of this document, you should be an expert in scraping any kind of web site, for any reason.

So, let's scrape something!

From the command line run:

`pip install requests`

if you don't have pip you can get [pip here](https://pip.pypa.io/en/stable/installing/)

```
r = requests.get("https://www.google.com")
print(r.url)
print(r.text)
```

We can treat `requests.get([website])` as the same thing as pointing your browser to `[website]`.  The returned objected, abbreviated as `r`, stands for response.  As in the response from one of google's servers to the `get` request issued by `requests`.
