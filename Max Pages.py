# Max Pages

# Modify the crawl_web procedure to take a second parameter,
# max_pages, that limits the number of pages to crawl.
# Your procedure should terminate the crawl after
# max_pages different pages have been crawled, or when
# there are no more pages to crawl.

# The following definition of get_page provides an interface
# to the website found at http://www.udacity.com/cs101x/index.html

# The function output order does not affect grading.

def get_page(url):
    try:
        if url == "http://www.udacity.com/cs101x/index.html":
            return ('<html> <body> This is a test page for learning to crawl! '
            '<p> It is a good idea to '
            '<a href="http://www.udacity.com/cs101x/crawling.html">learn to '
            'crawl</a> before you try to  '
            '<a href="http://www.udacity.com/cs101x/walking.html">walk</a> '
            'or  <a href="http://www.udacity.com/cs101x/flying.html">fly</a>. '
            '</p> </body> </html> ')
        elif url == "http://www.udacity.com/cs101x/crawling.html":
            return ('<html> <body> I have not learned to crawl yet, but I '
            'am quite good at '
            '<a href="http://www.udacity.com/cs101x/kicking.html">kicking</a>.'
            '</body> </html>')
        elif url == "http://www.udacity.com/cs101x/walking.html":
            return ('<html> <body> I cant get enough '
            '<a href="http://www.udacity.com/cs101x/index.html">crawling</a>! '
            '</body> </html>')
        elif url == "http://www.udacity.com/cs101x/flying.html":
            return ('<html> <body> The magic words are Squeamish Ossifrage! '
            '</body> </html>')
    except:
        return ""
    return ""

#searching for links on the page
def get_next_target(page):
    start_link = page.find('<a href=')
    if start_link == -1:     #if you don't find the beginning of a link, it means there is no link on the page
        return None, 0
    start_quote = page.find('"', start_link)       #finding the beginning of a link
    end_quote = page.find('"', start_quote + 1)    #finding the end of a link
    url = page[start_quote + 1:end_quote]
    return url, end_quote

def union(p,q):
    for e in q:
        if e not in p:
            p.append(e)

#get all the links from the page
def get_all_links(page):
    links = []
    while True:
        url,endpos = get_next_target(page)      #looking for a link on the page
        if url:         #if there is a link on the page, add it to the list "links" and continue search, for the next link, from that spot
            links.append(url)
            page = page[endpos:]
        else:          #if there is no more links, stop the search
            break
    return links

#crawling limited number of pages
def crawl_web(seed, max_pages):
    tocrawl = [seed]
    crawled = []     #at the beginning nothing has been crawled yet
    while tocrawl:
        page = tocrawl.pop()      #take the last page from the list "tocrawl"
        if page not in crawled and len(crawled) < max_pages:        #if page hasn't been crawled yet and number of crawled pages is less than defined number of pages to be crawled 
            union(tocrawl, get_all_links(get_page(page)))           #get all links from the crawled page and if they are not in the list "tocrawl", add them
            crawled.append(page)                                    #after page is crawled add it to the list "crawled"
    return crawled

print crawl_web("http://www.udacity.com/cs101x/index.html",1) 
#>>> ['http://www.udacity.com/cs101x/index.html']

print crawl_web("http://www.udacity.com/cs101x/index.html",3) 
#>>> ['http://www.udacity.com/cs101x/index.html', 
#>>> 'http://www.udacity.com/cs101x/flying.html', 
#>>> 'http://www.udacity.com/cs101x/walking.html']

#print crawl_web("http://www.udacity.com/cs101x/index.html",500) 
#>>> ['http://www.udacity.com/cs101x/index.html', 
#>>> 'http://www.udacity.com/cs101x/flying.html', 
#>>> 'http://www.udacity.com/cs101x/walking.html', 
#>>> 'http://www.udacity.com/cs101x/crawling.html', 
#>>> 'http://www.udacity.com/cs101x/kicking.html']
