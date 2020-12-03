# wikihopper
Hack to find the hop distance between two wiki articles.

If the distance is `maxdepth` clicks/hops or less, this simple script will find the shortest path between the two articles.

Running the script:

`>>python3 wikihopper.py https://en.wikipedia.org/wiki/Monty_Python --maxdepth 4`

This will start at a random wikipedia article and try to find its way to the Monty Python article.
