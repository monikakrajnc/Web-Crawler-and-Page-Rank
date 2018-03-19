# Feeling Lucky

# lucky_search takes as input an index, a ranks
# dictionary (the result of compute_ranks), and a keyword, and returns the one
# URL most likely to be the best site for that keyword. If the keyword does not
# appear in the index, lucky_search should return None.

def lucky_search(index, ranks, keyword):
    if lookup(index, keyword):   #ckeck if keyword exist
        b = 0
        a = index[keyword]
        for i in a:           #find the biggest rank
            if ranks[i] > b:
                b = ranks[i]
            else:
                b = b
        for j in ranks:        #find to which url belongs the biggest rank
            if ranks[j] == b:
                return j      #the url that is the most likely to be the best site for the keyword
    else:
        return None       #if keyword doesn't exist in the index
    
    

cache = {
   'http://udacity.com/cs101x/urank/index.html': """<html>
<body>
<h1>Dave's Cooking Algorithms</h1>
<p>
Here are my favorite recipies:
<ul>
<li> <a href="http://udacity.com/cs101x/urank/hummus.html">Hummus Recipe</a>
<li> <a href="http://udacity.com/cs101x/urank/arsenic.html">World's Best Hummus</a>
<li> <a href="http://udacity.com/cs101x/urank/kathleen.html">Kathleen's Hummus Recipe</a>
</ul>

For more expert opinions, check out the 
<a href="http://udacity.com/cs101x/urank/nickel.html">Nickel Chef</a> 
and <a href="http://udacity.com/cs101x/urank/zinc.html">Zinc Chef</a>.
</body>
</html>






""",
   'http://udacity.com/cs101x/urank/zinc.html': """<html>
<body>
<h1>The Zinc Chef</h1>
<p>
I learned everything I know from 
<a href="http://udacity.com/cs101x/urank/nickel.html">the Nickel Chef</a>.
</p>
<p>
For great hummus, try 
<a href="http://udacity.com/cs101x/urank/arsenic.html">this recipe</a>.

</body>
</html>






""",
   'http://udacity.com/cs101x/urank/nickel.html': """<html>
<body>
<h1>The Nickel Chef</h1>
<p>
This is the
<a href="http://udacity.com/cs101x/urank/kathleen.html">
best Hummus recipe!
</a>

</body>
</html>






""",
   'http://udacity.com/cs101x/urank/kathleen.html': """<html>
<body>
<h1>
Kathleen's Hummus Recipe
</h1>
<p>

<ol>
<li> Open a can of garbonzo beans.
<li> Crush them in a blender.
<li> Add 3 tablesppons of tahini sauce.
<li> Squeeze in one lemon.
<li> Add salt, pepper, and buttercream frosting to taste.
</ol>

</body>
</html>

""",
   'http://udacity.com/cs101x/urank/arsenic.html': """<html>
<body>
<h1>
The Arsenic Chef's World Famous Hummus Recipe
</h1>
<p>

<ol>
<li> Kidnap the <a href="http://udacity.com/cs101x/urank/nickel.html">Nickel Chef</a>.
<li> Force her to make hummus for you.
</ol>

</body>
</html>

""",
   'http://udacity.com/cs101x/urank/hummus.html': """<html>
<body>
<h1>
Hummus Recipe
</h1>
<p>

<ol>
<li> Go to the store and buy a container of hummus.
<li> Open it.
</ol>

</body>
</html>




""",
}

#find if the url exist in the cache dictionary
def get_page(url):
    if url in cache:
        return cache[url]
    return ""

#finding an url on the page
def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:      #if there are no urls on the page, return None
        return None, 0
    start_quote = page.find('"', start_link)       #find the beginning of the url
    end_quote = page.find('"', start_quote + 1)    #finding the end of the url
    url = page[start_quote + 1:end_quote]
    return url, end_quote

#create a list of all links from the page
def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)   #finding a link on the page
        if url:                               #if there is a link, add it to a list "links" and
            links.append(url)                 #continue search from that spot
            page = page[endpos:]
        else:                  #if there aren't any links stop the search
            break
    return links

#add elements from second input to the first one
def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)

#update the index to include all of the word occurences found in the
#page content by adding the url to the word's associated url list 
def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)

#add url to the keyword, it is associated with.     
def add_to_index(index, keyword, url):
    if keyword in index:      #if the keyword is already in the index, add the url to the list of urls associated with the keyword
        index[keyword].append(url)
    else:                   #if not, add new entry to the index
        index[keyword] = [url]

#check if keyword exist in the index   
def lookup(index, keyword):
    if keyword in index:
        return index[keyword]
    else:
        return None

def crawl_web(seed): # returns index, graph of inlinks
    tocrawl = [seed]       #list of pages that needs to be crawled
    crawled = []           #list of pages that have already been crawled
    graph = {}  # <url>, [list of pages it links to]
    index = {} 
    while tocrawl:    #until the is a page to crawl
        page = tocrawl.pop()
        if page not in crawled:         #check if page hasn't been crawled yet
            content = get_page(page)    #find the content (urls) of the page
            add_page_to_index(index, page, content)    #add page with its urls to the index
            outlinks = get_all_links(content)          #find links on the current crawled page, they need to be crawled next
            graph[page] = outlinks          #all the links that you can click on the page, to go to a different page
            union(tocrawl, outlinks)
            crawled.append(page)             #after finding all links on the page, put the page into crawled list
    return index, graph

def compute_ranks(graph):
    d = 0.8 # damping factor
    numloops = 10
    
    ranks = {}
    npages = len(graph)
    for page in graph:
        ranks[page] = 1.0 / npages
    
    for i in range(0, numloops):
        newranks = {}
        for page in graph:
            newrank = (1 - d) / npages
            for node in graph:
                if page in graph[node]:
                    newrank = newrank + d * (ranks[node] / len(graph[node]))
            newranks[page] = newrank
        ranks = newranks
    return ranks


#Here's an example of how your procedure should work on the test site: 

index, graph = crawl_web('http://udacity.com/cs101x/urank/index.html')
ranks = compute_ranks(graph)

print lucky_search(index, ranks, 'Hummus')
#>>> http://udacity.com/cs101x/urank/kathleen.html

print lucky_search(index, ranks, 'the')
#>>> http://udacity.com/cs101x/urank/nickel.html

print lucky_search(index, ranks, 'babaganoush')
#>>> None
