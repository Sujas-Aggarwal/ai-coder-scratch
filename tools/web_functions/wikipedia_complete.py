import aiohttp
import asyncio


# This is not good since it fetches the whole article, which can be very large.
# It is better to use the summary endpoint for large articles.
async def wikipedia_complete(topic):
    """
    [For Whole Article] Searches Wikipedia for a topic and returns the whole information about that page.
    
    Parameters:
    - topic (str): The topic to be searched.
    
    Returns:
    - str: complete or error message.
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

        # Step 2: Fetch the complete
        complete_url = f"https://en.wikipedia.org/w/index.php?title={best_title.replace(' ', '_')}&action=raw"
        async with session.get(complete_url) as resp:
            if resp.status != 200:
                return f"Error fetching complete for '{best_title}'."
            response = await resp.text()
            return "Results are from " + complete_url + "\n\n" + response

# 🔍 Usage Example
async def main():
    print(await wikipedia_complete("nazi germany"))

if __name__ == "__main__":
    asyncio.run(main())
