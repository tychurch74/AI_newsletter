import os
import openai


openai_api_key = os.environ["OPENAI_API_KEY"]

research_messages = [{"role": "system", "content": "Writer is a large language model trained by OpenAI that writes simple, concise, and entertaining articles for a weekly machine learning, artificial intelligence and general computing newsletter based on research paper excerpts and/or other text provided by the user. Your response should only include the generated article and not contain any additional content or context. Do not include the title in your response if it's provided by the user. The generated article will be used directly in the newsletter."}]

def research_paper_writer(article_text):
    openai.api_key = openai_api_key
    text = f"Write a newsletter article detailing content from the following research paper: {article_text}"
    research_messages.append({"role": "user", "content": text})
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=research_messages)
    written_content = completion.choices[0].message.content
    return written_content





