from bs4 import BeautifulSoup
import requests
import queue
from urllib.parse import urljoin, urlsplit, urlunsplit
import os
import argparse

from node import Node

parser = argparse.ArgumentParser(description="Follow wikipedia references to find the closest hop distance between two articles.")
parser.add_argument("target_url")
parser.add_argument("--start_url", help="If not specified, it will default to random")
parser.add_argument("--maxdepth", help="Maximum search depth (default: 3)", type=int)

def get_urls_in_page(url):
    '''
    Gets, cleans and filters the URLs on the page.  
    Currently ignores any explicit definition of base_url in the HTML file.
    Hardcoded for wiki atm.
    '''
    all_urls = extract_urls(url)
    base_url = get_base_url(url)
    complete_urls = [complete_url(u, base_url) for u in all_urls]

    filt = urljoin(base_url, "wiki")  # TODO: Remove wiki hardcoding...
    filtered_urls = list(filter(lambda x: "File:" not in x,
                                filter(lambda x: filt in x, complete_urls)))
    return filtered_urls

def get_base_url(url):
    """Get the base url of page"""
    split_url = urlsplit(url)
    base_url = urlunsplit((split_url.scheme, split_url.netloc, "", "", ""))
    return base_url

def extract_urls(url):
    """Extract all URLs on page and return as list"""
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'lxml')
    urls = soup.find_all("a")
    return [url.get("href") for url in urls]    

def complete_url(url, base_url):
    """Complete relative URL with base_url"""
    return urljoin(base_url, url)

def bfs(start_url, target_url, max_depth):
    """Perform a breadth first search"""
    q = queue.Queue()
    start_node = Node(start_url, None)
    q.put(start_node)

    visited = set()

    n_nodes = 0
    while not q.empty():
        print("Checking node {0}".format(n_nodes))
        curr_node = q.get()
        if curr_node.url in visited:
            continue

        urls = get_urls_in_page(curr_node.url)
        for u in urls:
            tmp_node = Node(u,curr_node)

            if tmp_node.url == target_url:
                print("Found relation at depth {0}".format(tmp_node.depth))
                return tmp_node

            if tmp_node.depth > max_depth:
                print("Could not find relation in {0} redirects or less".format(max_depth))
                return

            q.put(tmp_node)
        n_nodes += 1
        visited.add(curr_node.url)



def main():

    args = parser.parse_args()
    target_url = args.target_url

    if args.start_url:
        start_url = args.start_url
    else:
        start = "https://en.wikipedia.org/wiki/Special:Random"
        
        # Get the actual url since Special:Random will redirect
        r = requests.get(start)
        start_url = r.url

    if args.maxdepth:
        max_depth = int(args.maxdepth)
    else:
        max_depth = 3
    
    print("Starting at " + start_url)
    solution = bfs(start_url, target_url, max_depth)

    # Backtrace the path
    trace = []
    curr_node = solution
    while True:
        try:
            trace.append(curr_node.url)
        except AttributeError:
            break
        curr_node = curr_node.parent
    trace.reverse()

    for t in trace:
        print(t)

if __name__ == '__main__':
    main()
