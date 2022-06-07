# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

executable_path = {'executable_path': ChromeDriverManager().install()}
browser = Browser('chrome', **executable_path, headless=False)

# Visit the mars nasa news site
url = 'https://redplanetscience.com'
browser.visit(url)
# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)

html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('div.list_text')

slide_elem.find('div', class_='content_title')

# Use the parent element to find the first `a` tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title

# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ### Featured images
# Visit URL
url = 'https://spaceimages-mars.com'
browser.visit(url)

# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel

# Use the base URL to create an absolute URL
img_url = f'https://spaceimages-mars.com/{img_url_rel}'
img_url

# Importing html table with pandas
df = pd.read_html('https://galaxyfacts-mars.com')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

df.to_html()

#browser.quit()

# # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
# ### Hemispheres

# 1. Use browser to visit the URL 
url = 'https://marshemispheres.com/'
browser.visit(url)

# Function which received the URL where the info to get the hres pic is located
def get_hdef_pic_info(source_url, browser):
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
            img_url = url + a_tag.attrs['href']
            #print(img_url)
            
    return { 'img_url':img_url,
            'title': img_name }
    
    
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
        hemisphere_image_urls.append(get_hdef_pic_info(url_to_get_info, browser))



hemisphere_image_urls

# 5. Quit browser
browser.quit()
