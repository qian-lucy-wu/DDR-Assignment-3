#!/usr/bin/env python
# coding: utf-8

# In[81]:


import requests
from bs4 import BeautifulSoup


# ### a) Use the URL identified in part 1 and load the first page with 40 items per page

# In[82]:


# Access the URL of the first page with 40 items per page of “B&N Top 100”
first_page_url= "https://www.barnesandnoble.com/b/books/_/N-1fZ29Z8q8?Nrpp=40&page=1"


# In[8]:


# Load the above webpage
page1 = requests.get(first_page_url, headers={"User-Agent": "Mozilla/5.0"})

# Check that connection is successful
page1


# In[83]:


# Parse the data by creating a beautifulsoup object 
soup1 = BeautifulSoup(page1.text, 'lxml')

# View selected text
soup1


# ### b) Create a list of each book’s product page URL

# In[84]:


# Find all tags <div> of class "product-shelf-title"
list = soup1.find_all('div',class_= "product-shelf-title")

# View selected content containing product page URLs
list


# In[11]:


# Add a string in front of html content to form the complete product page URL
bn_str = "www.barnesandnoble.com"

# Print the html content with a length of 40
for div in list:
    # h3 = div.find('h3')
    # a = h3.find('a')
    a = div.find('a')
    print(bn_str + a.get('href'))


# In[85]:


# Alternatively, direclty find tags <a> with attribute "href" that follows tags <h3>
books_list = soup1.select("h3 > a[href]")
books_list


# In[13]:


# Add a string in front of html content to form the complete product page URL
bn_str = "www.barnesandnoble.com"

# Print a list of each book’s product page URL with a length of 40
for a in books_list:
    print(bn_str + a.get('href'))


# ### c) Write a loop that downloads each product page of the top 40 books

# In[86]:


# Creat an empty string url_list at the beginning
url_list = []

# Generate all webpage URLs and save them in url_list
for i in list:
    a_list = i.find_all('a')
    for j in a_list:
        url_data = j.get('href')
        url_data = "http://www.barnesandnoble.com" + url_data
        url_list.append(url_data)


# In[87]:


# This list should be of length 40.
len(url_list)


# In[88]:


# Print all URLs in the list
for i in url_list:
    print(i)


# In[89]:


# Library for opening and reading URLs
import urllib.request

# Library for controlling time
import time
from time import sleep


# In[90]:


# Downloads each product page of the top 40 books in “B&N Top 100
for i in range(len(url_list)): # run through a list with length of 40
    page = requests.get(url_list[i], headers={"User-Agent": "Mozilla/5.0"})
    soup = BeautifulSoup(page.content, "html.parser")
    with open('bn_top_100_%d.html'%i, 'wb') as file: # create and open a html file to save each webpage 
        file.write(page.content) 
        time.sleep(5) # give a 5 second pause after each page request
        file.close()


# ### d) Access and read the “Overview” section in the above pages that are downloaded

# #### - Using the html files that have been downloaded in question (c)

# In[91]:


# Looping through all the pages we downloaded before
for i in range(len(url_list)):
    file = 'bn_top_100_%d.html'%i
    html = open(file, "r", encoding='utf-8').read() 
    # parse the data into soup objects:
    soup = BeautifulSoup(html, 'lxml') 
    # select the html content that we're interested:
    overview = soup.select("div#overviewSection div.overview-cntnt")
    # lastly, print the first 100 characters of the overview text:
    for j in overview:
        print(j.text[0:100]+"\n") 


# #### - Directly load the pages from website without referring to downloaded files (additional exploration for question d)

# In[92]:


# Intial trial with the first book's webpage
url = url_list[0]
page = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(page.text, 'lxml')
list_of_contents = soup.select("div#overviewSection div.overview-cntnt")


# In[93]:


# Then, check if the “Overview” section is printed as expected
for i in list_of_contents:
    print(i.text[0:100])


# In[94]:


# Similarly, do the same for all books on the list by looping through the pages above
for i in range(len(url_list)): 
    page = requests.get(url_list[i], headers={"User-Agent": "Mozilla/5.0"})
    # parse the data into soup objects:
    soup = BeautifulSoup(page.content, "html.parser")
    # select the html content that we're interested:
    list_of_contents = soup.select("div#overviewSection div.overview-cntnt")
    # print the first 100 characters of the overview text:
    for j in list_of_contents:
        print(j.text[0:100])


# In[ ]:




