"""
AI_newsletter base module.

This module contains the main function for the AI newsletter.

Functions:
    research_papers: Get research papers from arxiv, feed summaries to GPT-3.5, and format them into a list of dictionaries for newsletter generation.
    github_repos: Get top 10 github repos from the last week.
    main: Main function for the AI newsletter.
"""
from utils.date_info import get_seven_days_ago_date, convert_todays_date
from scrapers.arxiv_scraper import get_arxiv_papers
from scrapers.github_scraper import get_github_repos
from scrapers.news_scraper import get_top_10_ai_news
from writers_room.chatGPT_writer import research_paper_writer
from formatters.newsletter import newsletter_gen


def research_papers(testing, search_terms=("artificial intelligence", "natural language processing"), max_results=5):
    """
    Get research papers from arxiv, feed summaries to GPT-3.5, and format them into a list of dictionaries for newsletter generation.

    Args:
        testing (bool): Whether or not to run as a test (using dummy data). If False, will feed data to OpenAI's API.
        search_terms (tuple, optional): Search terms to use for arxiv. Defaults to ("artificial intelligence", "natural language processing").
        max_results (int, optional): Maximum number of results to return from arxiv. Defaults to 5.

    Returns:
        list: List of dictionaries containing the title, date, authors, GPT written article, and link for each paper (if testing=False).

    """
    
    pdf_filenames, result_pdf_dict = get_arxiv_papers(search_terms, max_results=max_results)
    papers = []

    if testing:
        papers = [
            {"title": "title", "date": "date", "authors": "authors", "article": "article", "link": "link"},
            {"title": "title2", "date": "date2", "authors": "authors2", "article": "article2", "link": "link2"},
        ]
    else:
        print("Feeding to writer")
        for result in result_pdf_dict:
            title, date, author_list, summary, link = result.values()
            authors = [author.name for author in author_list]
            article_text = f"Paper Title: {title}\nPublish Date: {date}\nSummary: {summary}"
            article = research_paper_writer(article_text)
            full_article = {"title": title, "date": date, "authors": authors, "article": article, "link": link}
            papers.append(full_article)

    return papers


def github_repos(date):
    """
    Get top 10 github repos from the last week.

    Args:
        date (str): Date in YYYY-MM-DD format.

    Returns:
        list: List of dictionaries containing the name and url of each repo.
    
    """
    repo_list = get_github_repos(date)
    top_repos = [{"url": repo["URL"], "name": f"{count+1}- {repo['name']}"} for count, repo in enumerate(repo_list)]
    return top_repos


def main():
    last_week_date = get_seven_days_ago_date()
    run_as_test = input("Testing? (y/n): ").lower() == "y"

    if run_as_test:
        print("Running as test (using dummy data)")
    else:
        print("Running as production (using real data)")

    newsletter_gen(
        convert_todays_date(),
        research_papers(run_as_test),
        github_repos(last_week_date),
        get_top_10_ai_news(),
    )
