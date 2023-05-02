from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os


def newsletter_gen(papers_list, repos_list):
    # Mock data for testing
    papers = papers_list

    tweets = [
        "Tweet 1",
        "Tweet 2",
        "Tweet 3",
    ]

    repos = repos_list

    # Set up Jinja2 environment and load template
    env = Environment(loader=FileSystemLoader(os.path.dirname(__file__)))
    template = env.get_template("index.html")

    # Render the template with data
    rendered_newsletter = template.render(papers=papers, tweets=tweets, repos=repos)

    # Save the rendered newsletter to an HTML file
    with open("newsletter.html", "w") as f:
        f.write(rendered_newsletter)

    # Convert the HTML file to a PDF
    HTML(string=rendered_newsletter).write_pdf("newsletter.pdf")

    print("Newsletter generated successfully!")
