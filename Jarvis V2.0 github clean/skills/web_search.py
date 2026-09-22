import os

from tavily import TavilyClient


client = TavilyClient(
    api_key=os.environ.get("TAVILY_API_KEY")
)


def search_web(query, current=False):

    if not query:
        return None

    try:

        search_options = {
            "query": query,
            "search_depth": "advanced",
            "max_results": 5
        }

        # For current/news questions, strongly favor recent information
        if current:

            search_options["topic"] = "news"
            search_options["time_range"] = "week"

        response = client.search(
            **search_options
        )

        return response

    except Exception as error:

        print(
            "Web search error:",
            error
        )

        return None


# ---------------- TEST MODE ----------------

if __name__ == "__main__":

    while True:

        query = input(
            "Search the web: "
        ).strip()

        if query.lower() == "exit":
            break

        result = search_web(
            query,
            current=True
        )

        if result:

            print("\nSEARCH RESULTS:\n")

            for item in result.get(
                "results",
                []
            ):

                print(
                    "TITLE:",
                    item.get("title")
                )

                print(
                    "URL:",
                    item.get("url")
                )

                print(
                    "CONTENT:",
                    item.get("content")
                )

                print(
                    "\n--------------------\n"
                )

        else:

            print(
                "No search results returned."
            )