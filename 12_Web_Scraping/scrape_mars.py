
# coding: utf-8

# In[1]:


# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pandas as pd
from splinter import Browser
import time
from selenium import webdriver
from flask import Flask, render_template
import pymongo


# # NASA Mars News
# Scrape the NASA Mars News Site(https://mars.nasa.gov/news/) and collect the latest News Title and Paragraph Text.

# In[2]:


# scrape the URL Page 
url1 = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
# Retrieve page with the requests module
response = requests.get(url1)


# In[3]:


# Create a Beautiful Soup object
soup1 = bs(response.text, "html5lib")
type(soup1)


# In[4]:


# Extract the text from the class="content_title" and clean up the text use strip
news_title = soup1.find_all('div', class_='content_title')[0].find('a').text.strip()

# print title to check
print(news_title)


# In[5]:


# Extract the paragraph from the class="rollover_description_inner" and clean up the text use strip
news_p = soup1.find_all('div', class_='rollover_description_inner')[0].text.strip()

#print paragraph to check
print(news_p)


# # JPL Mars Space Images - Featured Image
# Use splinter to navigate the JPL's Featured Space Image and scrape the current Featured Mars Image url (https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars)

# In[6]:


# https://splinter.readthedocs.io/en/latest/drivers/chrome.html
get_ipython().system('which chromedriver')


# In[7]:


# Execute Chromedriver
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[8]:


# URL of page to be scraped
url2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'

#Visit the page using the browser
browser.visit(url2)


# In[9]:


# assign html content
html = browser.html
# Create a Beautiful Soup object
soup2 = bs(html, "html5lib")


# In[10]:


#Scrape Path for the Feature Image. got the partial path of the url
partial_address = soup2.find_all('a', class_='fancybox')[0].get('data-fancybox-href').strip()


# In[11]:


#combine the root url to get the full address
featured_image_url = "https://www.jpl.nasa.gov"+partial_address

#Print to check the full URL
print(featured_image_url)

#browse to check url
browser.visit(featured_image_url)


# # Mars Weather
# Visit the Mars Weather twitter account(https://twitter.com/marswxreport?lang=en) and scrape the latest Mars weather tweet from the page using splinter.

# In[12]:


# Execute Chromedriver (add in again in case you close the browser)
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[13]:


# URL of page to be scraped
url3 = 'https://twitter.com/marswxreport?lang=en'

#Visit the page using the browser
browser.visit(url3)


# In[14]:


# assign html content
html = browser.html
# Create a Beautiful Soup object
soup3 = bs(html, "html5lib")


# In[15]:


#scrap latest Mars weather tweet
mars_weather = soup3.find_all('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text')[0].text

#print to check tweet
print(mars_weather)


# # Mars Facts¶
# Visit the Mars Facts webpage(http://space-facts.com/mars/) and use Pandas to scrape and cconvert the data to a HTML table string.

# In[16]:


# URL of page to be scraped
url4 = 'https://space-facts.com/mars/'


# In[17]:


# use Pandas to get the url table
tables = pd.read_html(url4)
tables


# In[18]:


# Convert list of table into pandas dataframe
df = tables[0]

# update column name
df.columns=['description','value']

# inspect dataframe
df


# In[19]:


#Set the index to the description column

df.set_index('description', inplace=True)
df


# In[20]:


# Use pandas to  generate HTML tables from DataFrames and save as html file
df.to_html('table.html')


# # Mars Hemispheres
# Visit the USGS Astrogeology site(https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars) to obtain high resolution images for each of Mar's hemispheres.

# In[21]:


# Execute Chromedriver (add in again in case you close the browser)
executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[22]:


# URL of page to be scraped
url5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

#Visit the page using the browser
browser.visit(url5)


# In[23]:


# assign html content
html = browser.html
# Create a Beautiful Soup object
soup5 = bs(html,"html5lib")


# In[24]:


# assigned list to store:
hemisphere_image_urls = []


# In[25]:


# create empty dict
dict = {}


# In[26]:


# get all the title
results = soup5.find_all('h3')


# In[27]:


# Loop through each result
for result in results:
    # Get text info from result
    itema = result.text
    time.sleep(1)    
    browser.click_link_by_partial_text(itema)
    time.sleep(1)
    # assign html content
    htmla = browser.html
    # Create a Beautiful Soup object
    soupa = bs(htmla,"html5lib")
    time.sleep(1)
    # Grab the image link
    linka = soupa.find_all('div', class_="downloads")[0].find_all('a')[0].get("href")
        # Pass title to Dict
    time.sleep(1)
    dict["title"]=itema
    # Pass url to Dict
    dict["img_url"]=linka
    # Append Dict to the list 
    hemisphere_image_urls.append(dict)
    # Clean Up Dict
    dict = {}
    browser.click_link_by_partial_text('Back')
    time.sleep(1)


# In[28]:


# review List
hemisphere_image_urls

