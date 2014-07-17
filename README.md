YASN
====
Yet Another [Social News](http://en.wikipedia.org/wiki/Social_news) website, written in django framework.


Features
========
* Users can register and manage their profile
* Users are able to add an post with link, tags and description
* Users can upvote posts of other users, increasing the score of the post

Coming soon
============
* Better algorithm for computing posts score
* Microblog for every User
* Possibility of uploading avatars


Running 
=======
1. Get the source code from the repository: ```git clone git@github.com:msoltysik/YASN.git```
2. Go to the YASN folder ```cd YASN```
3. Create a virtualenv directory, e.g. ```virtualenv2 yasn```
4. Install the required packages via pip: ```pip install -r requirements.txt```
5. Syncdb: ```python2 manage.py syncdb```
6. Run localserver: ``` python2 manage.py runserver```
7. Type in web browser http://127.0.0.1:8000/
