import arxiv
import requests

from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings 
from langchain.document_loaders import PyPDFLoader
from langchain.chains import ChatVectorDBChain
from langchain.llms import OpenAI


def get_arxiv_papers(search_terms=("artificial intelligence", "natural language processing"), max_results=5):
    """
    Get research papers from arxiv, download pdf versions, and return a list dictionaries containing information from each paper.

    Args:
        search_terms (tuple, optional): Search terms to use for arxiv. Defaults to ("artificial intelligence", "natural language processing").
        max_results (int, optional): Maximum number of results to return from arxiv. Defaults to 5.

    Returns:
        list: List of generated pdf filenames.
        list: List of dictionaries containing the title, date, authors, summary, and link for each paper.
    """
    
    search_query = " AND ".join(f'"{term}"' for term in search_terms)
    search = arxiv.Search(
        query=search_query,
        max_results=max_results,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending,
    )
    result_pdf_list = []
    result_pdf_dict = []
    for result in search.results():
        result_pdf_list.append(result.pdf_url)
        ds_result = {'title': result.title, 'date': result.published, 'authors': result.authors, 'summary': result.summary, 'link': result.pdf_url}
        result_pdf_dict.append(ds_result)

    pdf_filenames = []
    for count, pdf in enumerate(result_pdf_list):
        print(f"Downloading {count+1} of {len(result_pdf_list)}")
        r = requests.get(pdf, allow_redirects=True)
        open(f"AI_newsletter/papers/paper-{count+1}.pdf", "wb").write(r.content)
        pdf_filenames.append(f"AI_newsletter/papers/paper-{count+1}.pdf")
    
    return pdf_filenames, result_pdf_dict


# Additional functions for searching pdf results. To be implemented in future versions.

def search_pdf(pdf_filename):
    loader = PyPDFLoader(pdf_filename)
    pages = loader.load_and_split()
    return pages


def embed_pdf(pages):   
    embeddings = OpenAIEmbeddings()
    vectordb = Chroma.from_documents(pages, embedding=embeddings, persist_directory=".")
    vectordb.persist()
    return vectordb


def chain_pdf(vectordb, query):
    pdf_qa = ChatVectorDBChain.from_llm(
        OpenAI(temperature=0.9, model_name="gpt-3.5-turbo"),
        vectordb,
        return_source_documents=True,
    )
    result = pdf_qa({"question": query, "chat_history": ""})
    return(result["answer"])

