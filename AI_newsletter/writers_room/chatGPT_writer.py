import os
import openai


openai_api_key = os.environ["OPENAI_API_KEY"]

research_messages = [{"role": "system", "content": "Writer is a large language model trained by OpenAI that writes simple, concise, and entertaining articles for a weekly machine learning, artificial intelligence and general computing newsletter based on research paper excerpts and/or other text provided by the user. Your response should only include the generated article and not contain any additional content or context. Do not include the title in your response if it's provided by the user. The generated article will be used directly in the newsletter."}]

quote_messages = [{"role": "system", "content": "Writer is a large language model trained by OpenAI that writes simple, concise, silly and entertaining quotes for a weekly machine learning, artificial intelligence and general computing newsletter; similar to the splash texts shown on Minecraft's title screen. Your response should only include the generated quote and not contain any additional content or context. Your response should only be a quote, do not start your response with any phrases such as Sure here it is: or Here you go:"}, {"role": "user", "content": "Could you write a silly quote or phrase for this week's newsletter?"}, {"role": "system", "content": "Now with 12 herbs and spices!"}, {"role": "user", "content": "Could you write a silly quote or phrase for this week's newsletter?"}, {"role": "system", "content": "Now in 3D!"}, {"role": "user", "content": "Could you write a silly quote or phrase for this week's newsletter?"}, {"role": "system", "content": "Caution: Buzzwords Ahead"}, {"role": "user", "content": "Could you write a silly quote or phrase for this week's newsletter?"}, {"role": "system", "content": "Hallucinating quotes since 2022"}]


def research_paper_writer(article_text):
    openai.api_key = openai_api_key
    text = f"Write a newsletter article detailing content from the following research paper: {article_text}"
    research_messages.append({"role": "user", "content": text})
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=research_messages)
    written_content = completion.choices[0].message.content
    return written_content


def quote_writer():
    openai.api_key = openai_api_key
    text = f"Could you write a silly quote or phrase for this week's newsletter? Do not respond with anything other than the quote you come up with."
    quote_messages.append({"role": "user", "content": text})
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=quote_messages)
    quote_content = completion.choices[0].message.content
    return quote_content






