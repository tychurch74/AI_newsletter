from parsel import Selector
from playwright.sync_api import sync_playwright
from playwright.sync_api._generated import Page


def parse_tweets(selector: Selector):
    """
    parse tweets from pages containing tweets like:
    - tweet page
    - search page
    - reply page
    - homepage
    returns list of tweets on the page where 1st tweet is the 
    main tweet and the rest are replies
    """
    results = []
    # select all tweets on the page as individual boxes
    # each tweet is stored under <article data-testid="tweet"> box:
    tweets = selector.xpath("//article[@data-testid='tweet']")
    for i, tweet in enumerate(tweets):
        # using data-testid attribute we can get tweet details:
        found = {
            "text": "".join(tweet.xpath(".//*[@data-testid='tweetText']//text()").getall()),
            "username": tweet.xpath(".//*[@data-testid='User-Names']/div[1]//text()").get(),
            "handle": tweet.xpath(".//*[@data-testid='User-Names']/div[2]//text()").get(),
            "datetime": tweet.xpath(".//time/@datetime").get(),
            "verified": bool(tweet.xpath(".//svg[@data-testid='icon-verified']")),
            "url": tweet.xpath(".//time/../@href").get(),
            "image": tweet.xpath(".//*[@data-testid='tweetPhoto']/img/@src").get(),
            "video": tweet.xpath(".//video/@src").get(),
            "video_thumb": tweet.xpath(".//video/@poster").get(),
            "likes": tweet.xpath(".//*[@data-testid='like']//text()").get(),
            "retweets": tweet.xpath(".//*[@data-testid='retweet']//text()").get(),
            "replies": tweet.xpath(".//*[@data-testid='reply']//text()").get(),
            "views": (tweet.xpath(".//*[contains(@aria-label,'Views')]").re("(\d+) Views") or [None])[0],
        }
        # main tweet (not a reply):
        if i == 0:
            found["views"] = tweet.xpath('.//span[contains(text(),"Views")]/../preceding-sibling::div//text()').get()
            found["retweets"] = tweet.xpath('.//a[contains(@href,"retweets")]//text()').get()
            found["quote_tweets"] = tweet.xpath('.//a[contains(@href,"retweets/with_comments")]//text()').get()
            found["likes"] = tweet.xpath('.//a[contains(@href,"likes")]//text()').get()
        results.append({k: v for k, v in found.items() if v is not None})
    return results


def scrape_tweet(url: str, page: Page):
    """
    Scrape tweet and replies from tweet page like:
    https://twitter.com/Scrapfly_dev/status/1587431468141318146
    """
    # go to url
    page.goto(url)
    # wait for content to load
    page.wait_for_selector("//article[@data-testid='tweet']")  
    # retrieve final page HTML:
    html = page.content()
    # parse it for data:
    selector = Selector(html)
    tweets = parse_tweets(selector)
    return tweets
def parse_profiles(sel: Selector):
    """parse profile preview data from Twitter profile search"""
    profiles = []
    for profile in sel.xpath("//div[@data-testid='UserCell']"):
        profiles.append(
            {
                "name": profile.xpath(".//a[not(@tabindex=-1)]//text()").get().strip(),
                "handle": profile.xpath(".//a[@tabindex=-1]//text()").get().strip(),
                "bio": ''.join(profile.xpath("(.//div[@dir='auto'])[last()]//text()").getall()),
                "url": profile.xpath(".//a/@href").get(),
                "image": profile.xpath(".//img/@src").get(),
            }
        )
    return profiles


def scrape_top_search(query: str, page: Page):
    """scrape top Twitter page for featured tweets"""
    page.goto(f"https://twitter.com/search?q={query}&src=typed_query")
    page.wait_for_selector("//article[@data-testid='tweet']")  # wait for content to load
    tweets = parse_tweets(Selector(page.content()))
    return tweets


def scrape_people_search(query: str, page: Page):
    """scrape people search Twitter page for related users"""
    page.goto(f"https://twitter.com/search?q={query}&src=typed_query&f=user")
    page.wait_for_selector("//div[@data-testid='UserCell']")  # wait for content to load
    profiles = parse_profiles(Selector(page.content()))
    return profiles


def scrape_twitter(search_term: str):
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        page = browser.new_page(viewport={"width": 720, "height": 480})
        
        top_tweet_search = scrape_top_search(search_term, page)
        people_tweet_search = scrape_people_search(search_term, page)

        return top_tweet_search