# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup

#
#from selenium import webdriver
#from selenium.webdriver.chrome.service import Service
#from webdriver_manager.chrome import ChromeDriverManager
#

from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def scrape_all():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)
    
    news_title, news_paragraph = mars_news(browser)
    
    #Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now(),
        "hemispheres": mars_hemispheres_imgs(browser) # Deliverable 2 Module challenge
    }
    
    browser.quit()
    #print(data)
    return data

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #Conver the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')
    try:
        slide_elem = news_soup.select_one('div.list_text')
        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first `a` tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        #news_title

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
    except AttributeError:
        return None, None
    
    return news_title, news_p


#### Featured images
def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    return img_url

def mars_facts():
    # Importing html table with pandas
    try:
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    except BaseException:
        return None

    df.columns=['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)
    
    #Convert dataframe into HTML format, add bootstrap
    return df.to_html(classes="table table-striped")

def mars_hemispheres_imgs(browser):
    # 1. Use browser to visit the URL 
    url = 'https://marshemispheres.com/'
    browser.visit(url)
    
    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    html = browser.html
    #image_urls = browser.find_by_tag('itemLink product-item')

    html = browser.html
    my_soup = soup(html, 'html.parser')
    #img_soup

    #img_url_rel = my_soup.find('a', class_='itemLink')
    #img_url_rel = my_soup.find_all('a', class_='itemLink')
    img_url_rel = my_soup.select('a', class_='itemLink product-item')

    #print(img_url_rel)
    #print(len(img_url_rel))

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    for ele in img_url_rel:
        if len(ele.select('h3')) == 0:
            continue
        else:
            html_doc = ele.select('h3')[0].get_text() # Titulo de la pagina donde esta la foto
            if html_doc == "Back":
                continue

            url_to_get_info = url + ele.attrs['href']
            #print(url_to_get_info)
            hemisphere_image_urls.append(get_hdef_pic_info(url_to_get_info, browser, url))

    return hemisphere_image_urls
   
# Support Function which received the URL where the info to get the hres pic is located
def get_hdef_pic_info(source_url, browser, base_url):
    img_url = ""
    img_name = ""
    
    browser.visit(source_url)
    html = browser.html
    my_soup = soup(html, 'html.parser')
    html_pieces = my_soup.select('li')
    h2_tag = my_soup.find('h2', class_='title')
    
    # Getting the file title from the h2 tag
    img_name = h2_tag.get_text() # Image name
    
    for piece in html_pieces:
        #print("--- PIECE ---")
        #print(piece)
        a_tag = piece.find('a')
        #print("--- TEXT ---")
        if a_tag.get_text() == "Sample": # Nos interesa la iamgen con el texto Sample
            img_url = base_url + a_tag.attrs['href']
            #print(img_url)
            
    return { 'img_url':img_url,
            'title': img_name }

if __name__ == "__main__":
    print(scrape_all())
