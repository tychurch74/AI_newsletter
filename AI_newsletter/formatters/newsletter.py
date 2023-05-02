from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os


def newsletter_gen(todays_date, papers_list, repos_list, news_list):
    # Mock data for testing
    date = [{'today': todays_date}]
    
    papers = papers_list
    
    repos = repos_list
    
    news = news_list
    # Set up Jinja2 environment and load template
    env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))
    template = env.get_template("index.html")

    # Render the template with data
    rendered_newsletter = template.render(date=date, papers=papers, news=news, repos=repos)

    # Save the rendered newsletter to an HTML file
    with open("newsletter.html", "w") as f:
        f.write(rendered_newsletter)

    # Convert the HTML file to a PDF
    HTML(string=rendered_newsletter).write_pdf("newsletter.pdf")

    print("Newsletter generated successfully!")
