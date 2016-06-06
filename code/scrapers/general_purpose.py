"""

This module implements various general purpose scrapers for scraping all the links on a domain as well as all the links between 2 domains.  In order to do this we define websites as directed graphs (possibly cyclical) that interoperate.  For this we will use Breadth First Search, Depth First Search, and Dijkstra's algorithm to scrape these websites in a minimal general purpose setting.  Then minimium cuts, max flows and other basic graph theoretic techniques will be used to assess website interoperability and generally set up a standard for web referencing.

By 

Eric Schles - ericschles@gmail.com

""" 

import requests
import lxml.html
import heapq

class Stack:
    def __init__(self):
        self.internal = []
    def push(self,data):
        self.internal.append(data)
    def pop(self):
        return self.internal.pop()
    def empty(self):
        return self.internal == []
    
class Queue:
    def __init__(self):
        self.internal = []
    def push(self,data):
        self.internal.insert(0,data)
    def pop(self):
        return self.internal.pop()
    def empty(self):
        return self.internal == []

class PriorityQueue:
    def __init__(self):
        self.internal = []
    def empty(self):
        return self.internal == []
    def push(self,data,priority):
        heapq.heappush(self.internal, (priority, data))
    def pop(self):
        return heapq.heappop(self.internal)[1]
    
def complete_relative_url(url,base):
    if url.startswith("/") and base.endswith("/"):
        url = base + url.lstrip("/")
    elif not base.endswith("/") and url.startswith("/"):
        url = base + url
    return url

def get_neighbors(url,base):
    url = complete_relative_url(url,base)
    html = lxml.html.fromstring(requests.get(url).text)
    return [complete_relative_url(url,base) for url in html.xpath("//a/@href")]
        
def dfs(start):
    stack = Stack()
    already_seen = [start]
    came_from = {}
    stack.push(start)
    came_from[start] = []
    while not stack.empty():
        current = stack.pop()
        neighbors = get_neighbors(current,start)
        for neighbor in neighbors:
            if neighbor not in already_seen:
                stack.push(neighbor)
                already_seen.append(neighbor)
                came_from[neighbor] = [current]
            else:
                came_from[neighbor].append(current)     
    return already_seen, came_from

def bfs(start):
    queue = Queue()
    already_seen = [start]
    came_from = {}
    queue.push(start)
    came_from[start] = []
    while not queue.empty():
        current = queue.pop()
        neighbors = get_neighbors(current,start)
        for neighbor in neighbors:
            if neighbor not in already_seen:
                queue.push(neighbor)
                already_seen.append(neighbor)
                came_from[neighbor] = [current]
            else:
                came_from[neighbor].append(current)
    return already_seen, came_from

def get_min_distance_index(F,distances):
    minimum = float("inf")
    cur_index = 0
    for index,element in enumerate(F):
        if distances[element] < minimum:
            minimum = distances[element]
            cur_index = index
    return cur_index

def dijsktra(start,graph):
    already_seen = PriorityQueue()
    already_seen.push(start,0)
    came_from,cost_so_far = {},{}
    came_from[start] = None
    cost_so_far[start] = 0

    #TO DOS:
    while not already_seen.empty():
        current = already_seen.get()
        #graph is the result of bfs's came_from
        for next in graph[current]: #define neighbors function
            #set up internal graph
            new_cost = cost_so_far[current] + #define cost function
