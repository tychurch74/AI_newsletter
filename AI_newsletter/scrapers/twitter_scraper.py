import json

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
    page.goto(f"https://twitter.com/i/flow/login")
    page.wait_for_selector("//div[@data-testid='LoginForm_Login_Button']")  # wait for content to load
    page.click("//div[@data-testid='LoginForm_Login_Button']")
    page.goto(f"https://twitter.com/search?q={query}&src=typed_query&f=user")
    page.wait_for_selector("//div[@data-testid='UserCell']")  # wait for content to load
    profiles = parse_profiles(Selector(page.content()))
    return profiles


def scrape_twitter(search_term):
    with sync_playwright() as pw:
        print("The following will open a browser window. Please log in to Twitter if prompted.")
        input("Press Enter to continue...")
        browser = pw.chromium.launch(headless=False)
        page = browser.new_page(viewport={"width": 720, "height": 480})
        search_keyword = search_term
        tweet_search = scrape_top_search(search_keyword, page)
        json_object = json.dumps(tweet_search, indent=4)
 
        with open("tweets.json", "w") as outfile:
            outfile.write(json_object)
        
        return tweet_search


def format_twitter_results(keyword):    
    scrape_twitter(keyword)
    with open('tweets.json', 'r') as openfile:
        json_object = json.load(openfile)
    tweet_search = json_object
    result_tweet_dict = []
    for result in tweet_search:
        tweet_text = result['text']
        tweet_handle = result['url']
        tweet_url = result['url']
        ds_result = {'text': tweet_text, 'handle': tweet_handle, 'url': tweet_url}
        result_tweet_dict.append(ds_result)
    print(f"formatted dictionary: {result_tweet_dict}")
    return result_tweet_dict
    
"""
[
  {
    "text": "The best AI tools you need to know about!\n\n#ai #ChatGPT #Google",
    "username": "Ishan Sharma",
    "handle": "@Ishansharma7390",
    "datetime": "2023-02-07T11:32:28.000Z",
    "verified": false,
    "url": "/Ishansharma7390/status/1622921232646635520",
    "video": "https://video.twimg.com/ext_tw_video/1622921135833890817/pu/vid/720x1280/L5GkN9mSB8WPdxDz.mp4?tag=12",
    "video_thumb": "https://pbs.twimg.com/ext_tw_video_thumb/1622921135833890817/pu/img/c2XpGEntF_wfHDXA.jpg",
    "likes": "667",
    "retweets": "171",
    "replies": "26",
    "views": "21982"
  }
]
[{'text': tweet_text, 'handle': tweet_handle, 'url': tweet_url}]
"""