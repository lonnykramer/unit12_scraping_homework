#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from bs4 import BeautifulSoup as bs # lk added
import requests # lk added
import os # lk added
from splinter import Browser # lk added


# In[2]:


# from exercise 2-7 Splinter for dynamic websites - opens a browser and gives the code control of it
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[3]:


# Scrape everything
# this dictionary will hold everything we pull from all the sites
scraped_data = {}


# In[4]:


news_url = "https://mars.nasa.gov/news/"
browser.visit(news_url)
#print(soup.prettify())


# In[5]:


html = browser.html
soup = bs(html, 'html.parser')


# In[6]:


print(soup.prettify())


# In[7]:


# use BS to scrap the above website to find the news article title
news_title = soup.find("div", class_="content_title").text
news_title


# In[8]:


# use BS to scrap the above website to find the news article paragraph
news_article = soup.find("div", class_="article_teaser_body").text
news_article


# In[9]:



#news_title = "FILL IN THE TITLE" ## already done above
scraped_data['news_title'] = news_title

# use bs to find() the example_title_div and filter on the class_='article_teaser_body'

#news_p = "FILL IN THE PARAGRAPH"
news_p = news_article
scraped_data['news_p'] = news_p


# In[10]:


scraped_data


# In[11]:


# site 2 - https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars - repeat process
base_url = "https://www.jpl.nasa.gov"
jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
browser.visit(jpl_url)
print(soup.prettify())

# use splinter to connect to the url and navigate, then use bs4 to repeat what you did in site 1
html2 = browser.html
soup2 = bs(html2, 'html.parser')


# In[12]:


# Example: 
#featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16225_hires.jpg'
#scraped_data['featured_image_url'] = featured_image_url

img_url = soup2.find("article", class_="carousel_item")
img_url


# In[13]:


# old school python to parse out the image link - notice the ' in the image url above
img_url = img_url['style'].split("'")[1]


# In[14]:


featured_image_url = f'{base_url}{img_url}'
featured_image_url


# In[15]:


# site 3 - https://twitter.com/marswxreport?lang=en
base_url2 = "https://twitter.com/"
twitter_url = "https://twitter.com/marswxreport?lang=en"
# grab the latest tweet and be careful its a weather tweet

browser.visit(twitter_url)
print(soup.prettify())

# use splinter to connect to the url and navigate, then use bs4 to repeat what you did in site 1
html3 = browser.html
soup3 = bs(html3, 'html.parser')

# Example:
#mars_weather = 'Sol 1801 (Aug 30, 2017), Sunny, high -21C/-5F, low -80C/-112F, pressure at 8.82 hPa, daylight 06:09-17:55'


# In[16]:


# Example:
#mars_weather = 'Sol 1801 (Aug 30, 2017), Sunny, high -21C/-5F, low -80C/-112F, pressure at 8.82 hPa, daylight 06:09-17:55'

weather_url = soup3.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
weather_url


# In[17]:


# site 4 - 
facts_url = 'https://space-facts.com/mars/'

browser.visit(facts_url)
print(soup.prettify())


# In[18]:


html4 = browser.html
soup4 = bs(html4, 'html.parser')

# use pandas to parse the table

facts_df = pd.read_html(facts_url)[0]
facts_df


# In[19]:


facts_df = facts_df.set_index('Mars - Earth Comparison')
facts_df


# In[20]:


# convert facts_df to a html string and add to dictionary.
facts_df.to_html('mars_facts.html')


# In[21]:


# site 5 

site5_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

browser.visit(site5_url)
print(soup.prettify())


# In[22]:


# use bs4 to scrape the title and url and add to dictionary
hemisphere_urls = []
links = browser.find_by_css("a.product-item h3")
len(links)


# In[23]:


# use bs4 to scrape the title and url and add to dictionary
#usgs_url = 'https://astrogeology.usgs.gov'
hemisphere_urls = []
links = browser.find_by_css("a.product-item h3")



### site up and running now....

for i in range(len(links)):
    hemisphere = {}

    ### maybe class="itemLink product-item"
    browser.find_by_css("a.product-item h3")[i].click()
    image_anchor = browser.find_link_by_text("Sample").first
    #hemisphere["img_url"] = sample_elem["href"]
    hemisphere["img_url"] = image_anchor["href"]
### there are only 4 'h3' on the page, which encompass the image title    
    hemisphere["title"] = browser.find_by_css("h2.title").text
    
    
    hemisphere_urls.append(hemisphere)
    browser.back()

hemisphere_urls


# Example:
#hemisphere_image_urls = [
#    {"title": "Valles Marineris Hemisphere", "img_url": "..."},
#    {"title": "Cerberus Hemisphere", "img_url": "..."},
#    {"title": "Schiaparelli Hemisphere", "img_url": "..."},
#    {"title": "Syrtis Major Hemisphere", "img_url": "..."},
#]


# In[24]:


# File-> download as python into a new module called scrape_mars.py


# In[25]:


# use day 3 09-Ins_Scrape_And_Render/app.py as a blue print on how to finish the homework.

# replace the contents of def index() and def scraper() appropriately.

# change the index.html to render the site with all the data.


# In[26]:


browser.quit()

