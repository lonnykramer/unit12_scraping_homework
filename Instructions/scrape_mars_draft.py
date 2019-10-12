# came from Jupyter LK_scratch.ipynb

import pandas as pd
from bs4 import BeautifulSoup as bs 
import requests 
import os 
from splinter import Browser 


def init_browser():
# from exercise 2-7 Splinter for dynamic websites - opens a browser and gives the code control of it
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)



def scrape():
    browser = init_browser()
    # Scrape everything
    # this dictionary will hold everything we pull from all the sites
    scraped_data = {}

    
    news_url = "https://mars.nasa.gov/news/"
    browser.visit(news_url)
    
    html = browser.html
    soup = bs(html, 'html.parser')

    #print(soup.prettify())


    # use BS to scrap the above website to find the news article title
    news_title = soup.find("div", class_="content_title").text
    

    # use BS to scrap the above website to find the news article paragraph
    news_article = soup.find("div", class_="article_teaser_body").text
    

    #news_title = "FILL IN THE TITLE" ## already done above
    scraped_data['news_title'] = news_title

    # use bs to find() the example_title_div and filter on the class_='article_teaser_body'

    #news_p = "FILL IN THE PARAGRAPH"
    news_p = news_article
    scraped_data['news_p'] = news_p


   

########################################
    # site 2 - https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars - repeat process
    base_url = "https://www.jpl.nasa.gov"
    jpl_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(jpl_url)
    #print(soup.prettify())

    # use splinter to connect to the url and navigate, then use bs4 to repeat what you did in site 1
    html2 = browser.html
    soup2 = bs(html2, 'html.parser')


    # Example: 
    #featured_image_url = 'https://www.jpl.nasa.gov/spaceimages/images/largesize/PIA16225_hires.jpg'
    #scraped_data['featured_image_url'] = featured_image_url

    img_url = soup2.find("article", class_="carousel_item")
    img_url
    



    # old school python to parse out the image link - notice the ' in the image url above
    img_url = img_url['style'].split("'")[1]




    featured_image_url = f'{base_url}{img_url}'
    scraped_data['featured_image_url'] = featured_image_url


########################################
    # site 3 - https://twitter.com/marswxreport?lang=en
    base_url2 = "https://twitter.com/"
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    # grab the latest tweet and be careful its a weather tweet

    browser.visit(twitter_url)
    #print(soup.prettify())

    # use splinter to connect to the url and navigate, then use bs4 to repeat what you did in site 1
    html3 = browser.html
    soup3 = bs(html3, 'html.parser')

    # Example:
    #mars_weather = 'Sol 1801 (Aug 30, 2017), Sunny, high -21C/-5F, low -80C/-112F, pressure at 8.82 hPa, daylight 06:09-17:55'




    # Example:
    #mars_weather = 'Sol 1801 (Aug 30, 2017), Sunny, high -21C/-5F, low -80C/-112F, pressure at 8.82 hPa, daylight 06:09-17:55'

    weather_url = soup3.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    scraped_data['weather_url'] = weather_url


    ########################################
    # site 4 - 
    facts_url = 'https://space-facts.com/mars/'

    browser.visit(facts_url)
    

    html4 = browser.html
    soup4 = bs(html4, 'html.parser')

    # use pandas to parse the table

    facts_df = pd.read_html(facts_url)[0]
    
    # re-index the df to match example
    facts_df = facts_df.set_index('Mars - Earth Comparison')
    


    # convert facts_df to a html string and add to dictionary.
    #facts_df.to_html('mars_facts.html')
    
    scraped_data['mars_facts'] = facts_df.to_html()


    # to ensure utf-8 for the html file, i'm going to read it, then write it
    read_in_file = open('mars_facts.html', "r")
    mars_facts_str = read_in_file.read()
    mars_facts_str.replace('\\n', '')
    mars_facts_str = str(mars_facts_str)
    output_file = open('templates/mars_facts_cleaned.html', "w+", encoding='utf8')
    output_file.write(mars_facts_str)
    read_in_file.close()
    output_file.close()


    ########################################
    # site 5 
    ### need to correct jupyter and update this section
    site5_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'

    browser.visit(site5_url)
    #print(soup.prettify())


    # use bs4 to scrape the title and url and add to dictionary
    hemisphere_urls = []
    links = browser.find_by_css("a.product-item h3")

    for i in range(len(links)):
        hemisphere = {}
        browser.find_by_css("a.product-item h3")[i].click()
        image_anchor = browser.find_link_by_text("Sample").first
        
        hemisphere["img_url"] = image_anchor["href"]
        hemisphere["title"] = browser.find_by_css("h2.title").text
    
        hemisphere_urls.append(hemisphere)
        browser.back()

    scraped_data['hemisphere_urls'] = hemisphere_urls



    # Example:
    # hemisphere_image_urls = [
    #    {"title": "Valles Marineris Hemisphere", "img_url": "..."},
    #    {"title": "Cerberus Hemisphere", "img_url": "..."},
    #    {"title": "Schiaparelli Hemisphere", "img_url": "..."},
    #    {"title": "Syrtis Major Hemisphere", "img_url": "..."},
    #]
########################################

    browser.quit()
    return scraped_data
    

if __name__ == "__main__":
    print(scrape())

