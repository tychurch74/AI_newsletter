"""
AI_newsletter base module.
"""
from utils.date_info import get_seven_days_ago_date, is_today_monday, convert_todays_date
from scrapers.arxiv_scraper import get_arxiv_papers
from scrapers.github_scraper import get_github_repos
from scrapers.twitter_scraper import format_twitter_results
from scrapers.news_scraper import get_top_10_ai_news
from writers_room.chatGPT_writer import research_paper_writer
from formatters.newsletter import newsletter_gen


last_week_date = get_seven_days_ago_date()
todays_date = convert_todays_date()


def research_papers(testing = False,search_term_1="artificial intelligence", search_term_2="natural language processing", max_results=5):
    pdf_filenames, result_pdf_dict = get_arxiv_papers(
        search_term_1, search_term_2, max_results=max_results
    )
    papers = []
    if testing:
        papers = [{
            "title": "title",
            "date": "date",
            "authors": "authors",
            "article": "article",
            "link": "link",
        },
        {
            "title": "title2",
            "date": "date2",
            "authors": "authors2",
            "article": "article2",
            "link": "link2",
        }]
    else:
        for result in result_pdf_dict:
            title = result["title"]
            date = result["date"]
            author_list = result["authors"]
            authors = []
            for author in author_list:
                authors.append(author.name)
            summary = result["summary"]
            link = result["link"]
            article_text = (
                f"Paper Title: {title} \nPublish Date: {date} \nSummary: {summary}"
            )
            article = research_paper_writer(article_text)
            full_article = {
                "title": title,
                "date": date,
                "authors": authors,
                "article": article,
                "link": link,
            }
            papers.append(full_article)

    return papers


def github_repos(date):
    repo_list = get_github_repos(date)
    top_repos = []
    for count, repo in enumerate(repo_list):
        repo_name = f"{count+1}- {repo['name']}"
        repo_url = repo["URL"]
        repo_entry = {"url": repo_url, "name": repo_name}
        top_repos.append(repo_entry)
    return top_repos


def top_tweets(testing = True):
    if testing:
        top_tweets = [{"text": "Test text","handle": "@test handle","url": "/test/url"}, 
                      {"text": "Test text2","handle": "@test handle2","url": "/test/url2"}]
    else:
        try:
            top_tweets = format_twitter_results("AI")
        except:
            top_tweets = ["Twitter scrape failed"]
    return top_tweets
    

ai_news = get_top_10_ai_news()
newsletter_gen(todays_date, research_papers(), github_repos(last_week_date), ai_news)
