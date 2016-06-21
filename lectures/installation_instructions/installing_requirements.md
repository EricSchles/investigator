#Some house keeping for getting started!

So for those of you not familiar with git and python here is a quick dirty set of suggestions for getting started!

##Using git

The first thing you should do is clone the repo, so head over to:

[https://github.com/EricSchles/investigator](https://github.com/EricSchles/investigator)

Then you're going to click the `fork` button:

![](fork_button.png)

Once the repository is forked to your github, clone it locally by first clicking the clone or download button:

![](clone_button.png)

then you'll go to the location you want to store your code locally and type the following:

`git clone https://github.com/[your user name]/investigator`

##Using pip

You'll need [get-pip.py](https://bootstrap.pypa.io/get-pip.py) if you don't have pip installed already

once you have it downloaded up a terminal and type:

`python get-pip.py`

And this should download pip for you!

Once you have pip installed open a new terminal and head to your investigator repository and type the following from the top level folder of the repo:

`pip install -r requirements.txt`

It's possible you failed on installing psycopg2, in that case you'll need postgres, don't worry, this isn't hard to get!

##Install brew

If you're on mac, please use brew to install this.

How to [get brew](http://brew.sh/)

If you don't have python 3 make sure you install it:

`brew install python3`

##Install Postgres

To install this we'll make use of brew
`brew install postgres`

then go ahead and type:

`pip install -r requirements.txt`
