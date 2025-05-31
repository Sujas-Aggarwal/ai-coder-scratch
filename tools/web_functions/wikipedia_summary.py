import aiohttp
import asyncio

async def wikipedia_summary(topic):
    """
    [For Summary Only] Searches Wikipedia for a topic and returns a summary.
    
    Parameters:
    - topic (str): The search term (can be fuzzy or informal).
    
    Returns:
    - str: Summary or error message.
    """
    async with aiohttp.ClientSession() as session:
        # Step 1: Search for best-matching title
        search_url = "https://en.wikipedia.org/w/api.php"
        search_params = {
            "action": "query",
            "list": "search",
            "srsearch": topic,
            "format": "json"
        }

        async with session.get(search_url, params=search_params) as resp:
            search_data = await resp.json()
            search_results = search_data.get("query", {}).get("search", [])
            if not search_results:
                return f"No Wikipedia page found for '{topic}'."

            best_title = search_results[0]["title"]

        # Step 2: Fetch the summary
        summary_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{best_title.replace(' ', '_')}"
        async with session.get(summary_url) as resp:
            if resp.status != 200:
                return f"Error fetching summary for '{best_title}'."

            summary_data = await resp.json()
            full_text = summary_data.get("extract", "No summary available.")
            return "Results are from " + summary_url + "\n\n".join(full_text.split(". "))

# 🔍 Usage Example
async def main():
    print(await wikipedia_summary("godawan"))
    print(await wikipedia_summary("indian democracy"))

if __name__ == "__main__":
    asyncio.run(main())
