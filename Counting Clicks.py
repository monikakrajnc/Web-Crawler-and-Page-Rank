# Counting Clicks

# The result of lookup(index,keyword) should
# be a list of url entries, where each url
# entry is a list of a url and a number
# indicating the number of times that url
# was clicked for this query keyword.

# record_user_click(index,word,url) modifies the entry in the index for
# the input word by increasing the count associated
# with the url by 1.

#counting the number of times a user clicks on the link for this keyword
def record_user_click(index, keyword, url):
    urls = lookup(index, keyword)
    if urls:
        for entry in urls:     #each entry has an element an url and a number of clicks
            if entry[0] == url:
                entry[1] = entry[1]+1

def add_to_index(index, keyword, url):
    # format of index: [[keyword, [[url, count], [url, count],..]],...]
    for entry in index:
        if entry[0] == keyword:     #if keyword already exist in the index, 
            for urls in entry[1]:   #check if also url exist, if not add it to the sublist of the keyword
                if urls[0] == url:
                    return
            entry[1].append([url,0])
            return
    # not found, add new keyword to index
    index.append([keyword, [[url,0]]])         #if keyword is not yet in the index, add keyword and url


def get_page(url):
    try:
        if url == "http://www.udacity.com/cs101x/index.html":
            return '''<html> <body> This is a test page for learning to crawl!
<p> It is a good idea to
<a href="http://www.udacity.com/cs101x/crawling.html">
learn to crawl</a> before you try to
<a href="http://www.udacity.com/cs101x/walking.html">walk</a> or
<a href="http://www.udacity.com/cs101x/flying.html">fly</a>.</p></body></html>'''

        elif url == "http://www.udacity.com/cs101x/crawling.html":
            return '''<html> <body> I have not learned to crawl yet, but I am
quite good at  <a href="http://www.udacity.com/cs101x/kicking.html">kicking</a>.
</body> </html>'''

        elif url == "http://www.udacity.com/cs101x/walking.html":
            return '''<html> <body> I cant get enough
<a href="http://www.udacity.com/cs101x/index.html">crawling</a>!</body></html>'''

        elif url == "http://www.udacity.com/cs101x/flying.html":
            return '<html><body>The magic words are Squeamish Ossifrage!</body></html>'
    except:
        return ""
    return ""

#add elements from the second input to the first one
def union(a, b):
    for e in b:
        if e not in a:
            a.append(e)

#finding an url on the page
def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:       #if there are no urls on the page, return None
        return None, 0
    start_quote = page.find('"', start_link)      #find the beginning of the url
    end_quote = page.find('"', start_quote + 1)    #finding the end of the url
    url = page[start_quote + 1:end_quote]          
    return url, end_quote

#create a list of all links from the page
def get_all_links(page):
    links = []
    while True:
        url, endpos = get_next_target(page)        #finding a link on the page
        if url:                           #if there is a link, add it to a list "links" and
            links.append(url)             # continue search from that spot
            page = page[endpos:]
        else:               #if there aren't any links stop the search
            break
    return links

def crawl_web(seed):
    tocrawl = [seed]      #list of pages that needs to be crawled
    crawled = []          #list of pages that have already been crawled
    index = []
    while tocrawl:       #until the is a page to crawl
        page = tocrawl.pop()
        if page not in crawled:           #check if page hasn't been crawled yet
            content = get_page(page)      #find the content (urls) of the page
            add_page_to_index(index, page, content)      #add page with its urls to the index
            union(tocrawl, get_all_links(content))       #find links on the current crawled page, they need to be crawled next
            crawled.append(page)                         #after finding all links on the page, put the page into crawled list
    return index

#update the index to include all of the word occurences found in the
#page content by adding the url to the word's associated url list 
def add_page_to_index(index, url, content):
    words = content.split()
    for word in words:
        add_to_index(index, word, url)

#check if keyword exist in the index and return list of links connected to that keyword
def lookup(index, keyword):
    for entry in index:
        if entry[0] == keyword:
            return entry[1]
    #return None


#Here is an example showing a sequence of interactions:
index = crawl_web('http://www.udacity.com/cs101x/index.html')
print lookup(index, 'good')
#>>> [['http://www.udacity.com/cs101x/index.html', 0],
#>>> ['http://www.udacity.com/cs101x/crawling.html', 0]]
record_user_click(index, 'good', 'http://www.udacity.com/cs101x/crawling.html')
print lookup(index, 'good')
#>>> [['http://www.udacity.com/cs101x/index.html', 0],
#>>> ['http://www.udacity.com/cs101x/crawling.html', 1]]

