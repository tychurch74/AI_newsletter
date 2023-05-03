"""
AI_newsletter base module.

To-do:
    * Add more writers for different types of articles
    * Use a server for image hosting
    * Add more scrapers for more sites
    * Add and integrate DALLE image generation to create splash images
    * Cleanup code
"""
from utils.date_info import (
    get_seven_days_ago_date,
    is_today_monday,
    convert_todays_date,
)
from scrapers.arxiv_scraper import get_arxiv_papers
from scrapers.github_scraper import get_github_repos
from scrapers.news_scraper import get_top_10_ai_news
from writers_room.chatGPT_writer import research_paper_writer
from formatters.newsletter import newsletter_gen


def research_papers(
    testing,
    search_term_1="artificial intelligence",
    search_term_2="natural language processing",
    max_results=5,
):
    pdf_filenames, result_pdf_dict = get_arxiv_papers(
        search_term_1, search_term_2, max_results=max_results
    )
    papers = []
    if testing:
        papers = [
            {
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
            },
        ]
    else:
        print("Feeding to writer")
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


last_week_date = get_seven_days_ago_date()


def main():
    run_as_test = input("Testing? (y/n): ")
    if run_as_test == "y":
        print("Running as test (using dummy data)")
        testing = True
    else:
        print("Running as production (using real data)")
        testing = False

    newsletter_gen(
        convert_todays_date(),
        research_papers(testing),
        github_repos(last_week_date),
        get_top_10_ai_news(),
    )


if __name__ == "__main__":
    main()
