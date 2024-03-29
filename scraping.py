# Import Dependancies, including: Splinter, BeautifulSoup, and Pandas
# from isort import code
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager

# Set up Splinter


def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # Set New Title and Paragraph Variables (returns 2 variables)
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data

# Create Mars Function


def mars_news(browser):
    # Visit the Mars news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first a tag and save it as `news_title`
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find(
            'div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

# ## JPL Space Images Featured Image


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

    # Add try/except for error handling
    try:
        # find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'

    return img_url

# ## Mars Facts


def mars_facts():
    # Add try/except for error handling
    try:
        # use 'read_html" to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns = ['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    # return df.to_html(classes="table table-striped")  ??? Was this something that My tutuor added?  What are bootstraps?
    return df.to_html(classes="table table-striped")


def hemispheres(browser):
    url = "https://marshemispheres.com/"
    browser.visit(url+"index.html")

    hemiimageurls = []
    #links = browser.find_by_css("a.product-item img")

    for i in range(4):
        # hemispheres={}
        browser.find_by_css("a.product-item img")[i].click()
        hemispheres = scrape_hemisphere(browser.html)
        #sample = browser.links.find_by_text("Sample").first
        hemispheres["img_url"] = url+hemispheres["img_url"]

        # hemispheres["title"]=browser.find_by_css("h2.title").text

        hemiimageurls.append(hemispheres)

        browser.back()
    return hemiimageurls


def scrape_hemisphere(html_text):
    hemisoup = soup(html_text, "html.parser")

    try:
        sample = hemisoup.find("a", text="Sample").get("href")
        title = hemisoup.find("h2", class_="title").get_text()
    except:
        title = None,
        sample = None,

    hemispheres = {
        "title": title,
        "img_url": sample}

    return hemispheres


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())
