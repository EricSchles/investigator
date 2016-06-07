#How do I even?

The first thing to note, if you ran the above commands (either via a python shell or saving things to a script), is that you just get back a string.  So how do you pull out meaningful information from this?

There are a number of great tools for scraping the web, but my personal favorite is lxml.  To get lxml you may have to do a little work, but it's worth it (and then some!).  

[lxml's documentation](http://lxml.de/installation.html) recommends doing the following:

`STATIC_DEPS=true sudo pip install lxml`

Which might be wrong, depending on your build - the key is you'll need `libxml2` and `libxslt`, which don't come with mac.  When I was running into this problem I used brew to install `libxml2` and `libxslt`:

`brew install libxml2 libxslt`

As an alternative, you could always get an linux vm (I recommend ubuntu) and install everything there.  Sadly, that's out of scope for this tutorial, but I'm happy to do another one on installing vm's and post it here.  

So, why did I ask you to go through all that effort?

```
import requests
import lxml.html

r = requests.get("https://www.google.com")
html = lxml.html.fromstring(r.text)
print(html.xpath("//a/@href"))
```

`lxml` exposes a parser for html pages that is superb.  The parser can be used a lot of ways, but I'd say the canonical way is to make use of the `xpath` api exposed through the library.  If you're unfamiliar with xpath, you can kind of think it like regular expressions for parsing web pages.  We'll make deep use of it throughout this tutorial, so it's recommended that you find a reference or two.

* [w3 schools](http://www.w3schools.com/xsl/xpath_intro.asp) has a good tutorial on this.  

* [Some advanced examples](https://renderman.pixar.com/resources/current/RenderMan/xPathExamples.html).

Let's start with understanding how xpath treats a document and then we'll move into the specifics of the above xpath query.  

lxml treats html documents as Directed Acyclic Graph's, typically referred to as trees.  The root of the document is the highest level - the openning and closing `<html>`,`</html>` tags.  Each layer of tree is one level deeper in the tag hierarchy so, in the following html:

```
<html>
<head>
	<title></title>
</head>
<body>
	<p>Hello</p>
</body>
</html>
```

The second layer is the head tag and the body tag.  At the third layer is the title tag and the p tag.  As should be clear from the example - the layer of your tag is determined by how many other tags enclose it.  The more tags enclose the tag your interested in, the deep in the tree it exists.

Let's break down the above xpath "query".

`//[tag]` - says search the whole document, at every layer for this [tag] type.  In our case - `//a` will return all the a tags.  

`/@[attribute]` - The `@` symbol is used to denote a tag attribute - and specifically return everything of this type.  Assuming the attribute is defined for the tag - in this case `//a/@href` returns the hyper link for the a tag.

What happens when we want other attributes or data?  

In the case of wanting other attributes we can make use of a whole host of methods to get the relevant metadata (aka the values of certain attributes) or we can get the text used for the hyper links via the following:

```
import requests
import lxml.html

r = requests.get("https://www.google.com")
html = lxml.html.fromstring(r.text)
print("Names of links:")
print([elem.text_content() for elem in html.xpath("//a")])
print("Links themselves:")
print(html.xpath("//a/@href"))
```

All done ;)
