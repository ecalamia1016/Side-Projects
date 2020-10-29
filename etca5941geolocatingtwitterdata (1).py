# -*- coding: utf-8 -*-
"""etca5941GeolocatingTwitterData.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1euhT_EVnKdbqSVoQJDbOcFuKbqEItFlo

## Make a copy!

Before getting started, make a copy of this notebook into your own Google Drive:

    Go to: File > Save a copy in Drive

# Homework: Geolocating Twitter Data

This is a straightforward assignment in which you will:
 * Extract self-declared users' locations from their Tweets
 * Use the external package `geostring` to resolve the locations to known cities, states, and countries

## Submission

This assignment has two a two-part submission. You will need to turn in both parts for full credit. 

Copy this notebook to your Google Drive, complete the assignment below, and submit both of the following to Canvas:

 * The .py download of your notebook (NOT the .ipynb)
 * The .txt outcomes file

## Overview of the notebook structure

This notebook contains the following parts:

 1. Background
 2. Setup
 3. Code
 4. Outcomes


### 1. **[Background](#scrollTo=2JBmAwmOb-Tu&line=1&uniqifier=1)**

This section provides background reading and investigation to better understand the assignment itself. After reading and understanding this section, the assignment should prove to be rather straightforward to complete.

### 2. **[Setup](#scrollTo=YdEU59C7yh5N&line=1&uniqifier=1)**

You will not need to edit this section, unless you have chosen a different location for your data files.

You should execute the code in this section before continuing with the assignment. Be sure the Drive mount is working correctly, and that you have proper access to the data file for the assignment.

### 3. **[Code](#scrollTo=vaM4nnISykhp&line=1&uniqifier=1)**

**The Code section of the assignment will be autograded**. As such, there are some important things to consider:

 * **Be sure to name any functions and variables exactly as instructed.** The grading tool will be looking for these exact names.
 * **Be sure there are no errors or exceptions** in this code when the notebook is run. The code in this section will always be abstracted into functions, which means if you see an exception here, it is a module-level exception that will trash the grader and throw your entire grade.
 * Generally, there will be **no printed output in this section**, except for debugging purposes. While your functions might print output, the functions will only be called in section 3, **Outcomes** where the printed output will show.
 * **Do not delete the section delimiter** which tells the grader where to stop.

### 4. **[Outcomes](#scrollTo=06bioxmgym8w&line=1&uniqifier=1)**

 Here is where you will make use of the code you wrote above. Here you will call the functions, and provide the necessary printed output. You will copy-paste the output of this section into a text file for submission.

Some things to keep in mind:

 * The code here is still important since it produces the output you will submit. However, it will not be directly scrutinized by the grading tool.
 * **Pay attention to the specified output submission format**. The output itself will also be autograded.

## Part 1. Background

We are interested in the geographic distribution of Tweets around a particular brand. In this case, we are looking to find where people are located who are Tweeting about **Mac N Cheese Breakfast**.

### Scrutinizing the Tweet data structure

At this point, you would probably consider using the Twitter API to fetch the data you need. We have done the actual data fetching for you, but you will need to understand the Twitter API data structure in order to do this assignment.

Take a look at all the metadata associated with a Tweet. It's a lot: https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object (Links to an external site.)

Find the field that maps to user reported location, that is, this field:

<img src="https://canvas.colorado.edu/courses/58125/files/14140548/download?wrap=1" width="500">

This is the field you will be extracting from each Tweet. Because this field is a self-reported location, the data is a bit fuzzy. We will run this location through the [geostring library](https://github.com/dfreelon/geostring) to normalize it to known locations.

#### Take a moment to:

 * Review the Tweet data structure and to find the field representing the user's location
 * Familiarize yourself with the `geostring` library

### The Data

To get this kind of Data, you would normally interface with the [Twitter API](https://developer.twitter.com/en/docs). Here, we have done that work for you, hitting the Twitter API's [search endpoint](https://developer.twitter.com/en/docs/tweets/search/overview) and fetching 10 pages for a total of 1000 Tweets.

Furthermore, we have re-structured the data into a single .jsonl file as described below. The data is available [here](https://drive.google.com/file/d/1dBNF7ly4dJb-_fWW3ICg-CKbITfAHR0C/view?usp=sharing).

Download that file, then upload it to your Google Drive at the location:

```
 APRD6342/Data/MacNCheeseBreakfast-Tweets.jsonl
```

### About jsonl format

.jsonl is an unofficial, but regularly used format of 1 json object per line in a file. This differs from standard json where the entire file is a single json object.

jsonl is handy in that it is streamable, whereas normal json is not. You can, for example, append new data to a jsonl file without actually opening and parsing the existing data. You can't do that with json.

#### Twitter's JSON format

The Twitter API gives us a payload that is something like this:

```
{
    "statuses": [
        {
            "created_at": "Tue Aug 11 16:35:48 +0000 2020", 
            "id": 1293224607684714497,
            ... (remaining Tweet data)
        }, (more Tweets -- up to 100 at a time)
    ]
}
```

What we have done is extracted those statuses from each page into a single file structured like this:

```
{"created_at": "Tue Aug 11 16:35:48 +0000 2020","id": 1293224607684714497, ... (remaining Tweet data) }
... (more Tweets -- as many as you need in a file)
```

That is, each line is a Tweet of the Tweet object data structure that you reviewed above. The code that was used to fetch Tweets is shown below.

### The fetch code

You will not need to execute this code, but it is informative to understand how the data was obtained. As described above, this code fetches 10 pages of 100 Tweets each and writes them to a .jsonl file.

```
import json

# birdy is a Twitter client I happen to like. There are
# others. tweepy is a popular one.
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

### Reading jsonl

Recall briefly how you would load a normal json file:

```
import json
with open(filename) as f:
    data = json.load(f)
```

Alternatively, you can read the json as a string:

```
data = json.loads(f.read())
```

So, in order to read the format of 1 object per line, we do this:

```
with open(filename) as f:
    for line in f:
        data = json.loads(line.strip()) # strip off the newline
        # ... do something with data
```

## Part 2. Setup

Do not edit the setup section except as noted.

Here, we mount Google Drive in order to access our data files. You should place your data files into a Drive folder called APRD6342/Data, or edit the mount code below as indicated.

Do not edit the alternative data path which is used for grading.
"""

# Mount data location. Do not edit this cell except as indicated.

# Be sure you have a folder in the root of your Google Drive called APRD6342/Data.
# Data files for the course should be uploaded to that folder.
from pathlib import Path
try:
    from google.colab import drive
    drive.mount('/content/drive')
    datadir = Path('drive/My Drive/APRD6342/Data') # you may edit this location ...
except ModuleNotFoundError:
    datadir = Path('../../Data') # ... but don't change this!!!

"""You should now be able to open files in your APRD6342/Data folder using Python's [Pathlib library](https://docs.python.org/3/library/pathlib.html).

For example, opening the first file in this assignment would look something like this, using Python's `open` function (a.k.a. the old-fashioned way):

```
open(datadir / 'MacNCheeseBreakfast-Tweets.jsonl')
```

Or, alternatively, using Pathlib's `open` method:

```
(datadir / 'MacNCheeseBreakfast-Tweets.jsonl').open()
```

Finally, if you prefer the old-fashioned [built-in open function](https://docs.python.org/3.7/library/functions.html#open):

```
import os
open(os.path.join(datadir, 'MacNCheeseBreakfast-Tweets.jsonl'))
```

## Part 3. Code

We are interested in counts by location in order to better understand from what locations people are tweeting about Mac N Cheese Breakfast!

Ultimately your code will parse all of Tweet locations from the input file and will aggregate those locations into counting dictionaries. To do this, you will implement the functions:

 * record_location -- Given a location string, record the city, state (ie. subcountry), and country to the counting dictionaries
 * top_locations -- Given a location counting dictionary (one of the 3) return the top locations by count

### imports
"""

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

"""### Submission

 * Download this completed notebook as a .py file and submit to Canvas
 * Copy-paste the output of the last cell (ie. the top cities, subcountries, and countries) into a .txt file called top_locations.txt and submit to Canvas. **Do not** reformat the output -- simply copy it as-is and paste to a .txt file.
"""