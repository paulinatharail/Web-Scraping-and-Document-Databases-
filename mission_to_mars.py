




import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup 
import requests
import os



def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)
    


# #-----------------------------------------------------
# # News title and description
# #-----------------------------------------------------

def news_title():

    # Get the News titles and descriptions 
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    #Retrieve page with the requests module
    response = requests.get(url)
    
    #Create BeautifulSoup object; and parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')
    
    #display html with identation
    # print(soup.prettify())
    
    #Find all the div with class='slide'
    divs = soup.find_all('div', class_="slide")

    # New list to hold all the title and description 
    news_divs = []

    #iterate through each div element
    for div in divs:
    
        #identify title and return news title
        title = div.find('div', class_='content_title').text.strip()
    
        #identify and return the description of the news
        description = div.find('div', class_='rollover_description_inner').text.strip()
    
        news_dict = {'Title': title,
                    'Description': description
                    }
        news_divs.append(news_dict)
        
        return news_divs[0]


# #-----------------------------------------------------
# # Mars Image using Splinter
# #-----------------------------------------------------


def mars_featured_img():
    browser = init_browser()
    
    # Mars images with Splinter
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    article = soup.find_all('article',class_='carousel_item')
    #print (article)
    
    # Extract the URL for the full image
    for art in article:
        article_a = art.find('a')
        featured_image_url = 'https://www.jpl.nasa.gov' + article_a['data-fancybox-href']

    return featured_image_url


# #-----------------------------------------------------
# # Mars Weather
# #-----------------------------------------------------


def mars_weather():
    url = 'https://twitter.com/marswxreport?lang=en'
    browser = init_browser()
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
    #Get all the tweets in the div element 
    tweets = soup.find_all('div',class_='js-tweet-text-container')

    #create a new list to contain all the tweets
    tweet_txt = []
    for tweet in tweets:
        tweet_txt.append(tweet.find('p').text)
    
    #Assign the latest weather to the variable mars_weather
    mars_weather = tweet_txt[0]

    return mars_weather    


# #-----------------------------------------------------
# # Mars Facts (pandas scraping)
# #-----------------------------------------------------



def mars_facts():
    url = 'https://space-facts.com/mars/'

    #scrape tabular data with pandas
    tables = pd.read_html(url)

    #tables is a list of dataframes
    #tables
    
    # convert to dataframe
    df = tables[0]

    df.columns = ['Facts','Measurements']

    #convert dataframe to dictionary
    mars_facts = df.to_dict('records')
    
    return mars_facts

# #-----------------------------------------------------
# # Mars Hemispheres
# #-----------------------------------------------------

def mars_hemisphers():
    

    # Access the locally saved Gitlab page to get the Mars Hemisphere pictures
    filepath = os.path.join("static", "Mars_Hemispheres.png")

    # with open(filepath) as file:
    #     html = file.read()

    # #create a Beautiful Soup objet
    # soup = BeautifulSoup(html, 'lxml')

    # #Extract images
    # images = []

    # imgs = soup.find_all('a', class_="no-attachment-icon")
    # for image in imgs:

    #    print(image)
    #    print(image.img["alt"])
    img_url = filepath
    img_title = "Mars Hemispheres"

    img_dict = {'url':img_url,
                'title':img_title
                }

    #images.append(img_dict)


    return img_dict



# #-----------------------------------------------------
# # scrape()
# #-----------------------------------------------------




#scrape () to return all scraped info as a dictionary

def scrape():
    mars_info = {}
    
    news_divs = news_title()
    featured_image_url = mars_featured_img()
    mars_weather_info = mars_weather()
    mars_fact = mars_facts()
    mars_hems = mars_hemisphers()
    
    mars_info = {
        'Mars_News': news_divs
        , 'Featured_Image': featured_image_url
        , 'Mars_weather': mars_weather_info
        , 'Mars_Facts': mars_fact
        , 'Mars_Hemispheres': mars_hems
    }
    
    return mars_info

