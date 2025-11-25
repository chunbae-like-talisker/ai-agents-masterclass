import os, re
from firecrawl import Firecrawl
from firecrawl.v2.types import Document


def web_search_tool(query: str):
    """
    Web Search Tool.
    Args:
        query: str
            The query to search the web for.
    Returns
        A list of search results with the website content in Markdown format.
    """
    app = Firecrawl(api_key=os.getenv("FIRECRAWL_API_KEY"))

    response = app.search(
        query=query,
        limit=5,
        sources=["web"],
        scrape_options={"formats": ["markdown"]},
    )

    cleaned_chunks = []

    for result in response.web:
        if isinstance(result, Document):
            title = result.metadata.title
            url = result.metadata.url
            markdown = result.markdown

            cleaned = re.sub(r"\\+|\n+", "", markdown).strip()
            cleaned = re.sub(r"\[[^\]]+\]\([^\)]+\)|https?://[^\s]+", "", cleaned)

            cleaned_result = {
                "title": title,
                "url": url,
                "markdown": cleaned,
            }

            cleaned_chunks.append(cleaned_result)

    return cleaned_chunks


def save_report_to_md(content: str) -> str:
    """Save report content to report.md file."""
    with open("report.md", "w") as f:
        f.write(content)
    return "report.md"
