"""
AI_newsletter base module.
"""
from utils.get_current_week import get_seven_days_ago_date, is_today_monday
from scrapers.arxiv_scraper import get_arxiv_papers
from scrapers.github_scraper import get_github_repos
from writers.chatGPT_writer import chatGPT_writer
from templates.newsletter import newsletter_gen


date = get_seven_days_ago_date()

def research_papers():
    pdf_filenames, result_pdf_dict = get_arxiv_papers("artificial intelligence", "natural language processing", max_results=1)
    papers = []
    for result in result_pdf_dict:
        title = (result['title'])
        date = (result['date'])
        authors = (result['authors'])
        summary = (result['summary'])
        article_text = (f"Paper Title: {title} \nPublish Date: {date} \nSummary: {summary}")
        article = chatGPT_writer(article_text)
        full_article = {'title': title, 'date': date, 'authors': authors, 'article': article}
        papers.append(full_article)
    
    return papers

def github_repos(date):
    repo_list = get_github_repos(date)
    top_repos = []
    for count, repo in enumerate(repo_list):
        repo_name = (f"{count+1}- {repo['name']}")
        repo_url = (repo['URL'])
        repo_entry = {'url': repo_url, 'name': repo_name}
        top_repos.append(repo_entry)
    return top_repos


def top_tweets():
    pass



newsletter_gen(research_papers(), github_repos(date))



    
