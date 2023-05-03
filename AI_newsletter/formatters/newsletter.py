import os

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML



def newsletter_gen(todays_date, papers_list, repos_list, news_list):
    """
    Generate newsletter.html and newsletter.pdf files.

    Args:
        todays_date (str): Today's date in Month Day, Year format.
        papers_list (list): List of dictionaries containing the title, date, authors, GPT written article, and link for each paper.
        repos_list (list): List of dictionaries containing the name and url of each repo.
        news_list (list): List of dictionaries containing the number, title, description, and url of each article.
    """
    date = [{'today': todays_date}]
    papers = papers_list
    repos = repos_list
    news = news_list
    
    env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))
    template = env.get_template("index.html")

    rendered_newsletter = template.render(date=date, papers=papers, news=news, repos=repos)
    
    with open("newsletter.html", "w") as f:
        f.write(rendered_newsletter)

    HTML(string=rendered_newsletter).write_pdf("newsletter.pdf")

    print("Newsletter generated successfully!")
