little random search web app
============================

do a web search and randomly choose which search engine to use.  don't repeat the same one twice.

this works best for the upper-right-hand search shortcut box.  there's an OSD XML file so it can be added to FF and IE.  safari doesn't support this; see [NOTES.safari.txt](NOTES.safari.txt) on how to solve by binary hacking (yikes).

obviously in its current state this code is designed only to run on my own machine, under apache+mod\_wsgi.  further obviously, this should be fixed.