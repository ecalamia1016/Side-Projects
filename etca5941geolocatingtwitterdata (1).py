import json


from birdy.twitter import UserClient

# These values would need to be filled in with your own app credentials
consumer_key=
consumer_secret=
access_token=
access_token_secret=

user_client = UserClient(
                consumer_key,
                consumer_secret,
                access_token,
                access_token_secret)

params = {
    'lang': 'en',
    'result_type': 'recent',
    'count': 100,
    'include_entities': True
}

def fetch_tweets(query, filename, pages=10):
    '''Fetch pages for query and write the resulting Tweets to
    filename as 1 JSON object per line, i.e. jsonl format.
    '''
    max_id = None
    with open(filename, 'w') as outfile:
        for i in range(pages):
            results = user_client.api.search.tweets.get(
                q=query, max_id=max_id, **params)
            for tweet in results.data['statuses']:
                # this is the jsonl part
                outfile.write(json.dumps(tweet)) 
                outfile.write('\n')
                if max_id is None or tweet['id'] < max_id:
                    max_id = tweet['id']

fetch_tweets('mac cheese breakfast', 'MacNCheeseBreakfast-Tweets.jsonl')
```

### Reading jsonlimport json
with open(filename) as f:
    data = json.load(f)





data = json.loads(f.read())
```

So, in order to read the format of 1 object per line, we do this:

```
with open(filename) as f:
    for line in f:
        data = json.loads(line.strip()) # strip off the newline
        # ... do something with data
```



import json
try:
    import geostring
except ModuleNotFoundError:
    !pip install geostring
    import geostring

"""### The counting dictionaries

These dictionaries are the data structures that will be used to count up respective resolved locations. E.g., the cities dictionary might look like this at some arbitrary point:

```
{
    'Chicago': 3,
    'Denver': 2,
    'New York': 5
}
```
"""

# dictionaries for tracking location counts
cities = {}
subcountries = {}
countries = {}

"""### record_location function

Complete the function that will record a resolved location (in the form of city, subcountry, country) to the respective count dictionaries.
"""

def record_location(resolved_city, resolved_subcountry, resolved_country):
    """Add each of the location components to their respective count dictionaries.
    If a component is empty or None, that count is not affected.

    This function operates on the globally initialized dictionaries: cities,
    subcountries, countries.

    Parameters:
     * resolved_city: str
     * resolved_subcountry: str
     * resolved_country: str

    For convenience, it returns the 3 dictionaries:
    Returns a 3-tuple of cities, subcountries, countries
    """
    if resolved_city != '':
      if resolved_city in cities:
        cities[resolved_city] += 1
      if resolved_city not in cities:
        cities[resolved_city] = 1
    
    if resolved_subcountry != '':
      if resolved_subcountry in subcountries:
        subcountries[resolved_subcountry] += 1
      if resolved_subcountry not in subcountries:
        subcountries[resolved_subcountry] = 1
      
    if resolved_country != '':
      if resolved_country in countries:
        countries[resolved_country] += 1
      if resolved_country not in countries:
        countries[resolved_country] = 1
    
    return cities, subcountries, countries

"""### top_items function

After all the data is aggregated, we want to know what the top cities, states, and countries are. This function returns the top n elements of any dictionary provided in the format of `{ item: count }`


#### Why the generic name?

Think about this: our location count dictionaries could be counting **anything**. By defining a concept of an item counting dictionary, we've created an abstraction that will be useful beyond the scope of this assignment!
"""

from collections import Counter

def top_items(item_counts, n=3):
    """For item count dictionary item_counts, return the top n items by count.

    Parameters:
     * item_counts: dict
     * n: int (default: 3)

    Returns:
     * list of top n items
      
    E.g:

    >>> top_items({ 'Chicago': 2, 'Los Angeles': 3, 'New York': 5 }, n=2)
    ['New York', 'Los Angeles']
    """
    count = Counter(item_counts)
    most_common = count.most_common(n)
    for item in zip(*most_common):
      return list(item)

"""### end of autograded code"""

#~~ /code # do not edit or remove this line

"""## Part 4. Outcomes

Here you will write the code that uses the above functions. When complete, these cells will record all of the available Tweet user locations, and will output the top cities, subcountries, and countries.

The procedure for reading jsonl files is described above in the [Reading jsonl section](#scrollTo=-dXQ6PLauPPV)
"""

INFILE = 'MacNCheeseBreakfast-Tweets.jsonl'
with open(datadir / INFILE) as f:
    for line in f:
      line_object = json.loads(line)
      index = line_object['user']['location']
      location = geostring.resolve(index)
      record_location( location['resolved_city'], location['resolved_subcountry'], location['resolved_country'])
         # Complete this with code that does the following:
             # 1. parse the tweet line
             # 2. resolve the location with geostring
             # 3. record the location by passing the geostring components to the record_location function

print('top cities:', top_items(cities))
print('top states:', top_items(subcountries))
print('top countries:', top_items(countries))
