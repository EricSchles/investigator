#How to store your credentials to different api's

I have elected to use python's builtin data serializer to store my credentials.  

##What is data serialization

Data serialization is the process of taking data read by a program and saving it to the file system.  The most common example of a data serialization standard is JSON - which serializes Javascript objects that can be passed as strings.  Since a file is just a big string (with annotation depending on the file), we can always turn an object or anything that can be treated as data and save it to the file system.  

##How our data looks

In this case, we are saving credentials to a file, with `.creds` extension.  I have written into the `.gitignore` that anything with `.creds` will be ignored by github, so you can safely push and pull without fear of ever exposing your credentials.  If you decide you would like to use your own extension of credentials, you can do this by adding it to `.gitignore`.  I'd highly recommend sticking with the conventions I've set, if only because then people know what you are doing with your branch and version of this code base.

