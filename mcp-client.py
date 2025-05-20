import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client
from langchain_openai import AzureOpenAI
import os

os.environ["OPENAI_API_VERSION"] = os.getenv('OPENAI_API_VERSION')
os.environ["AZURE_OPENAI_ENDPOINT"] = os.getenv('AZURE_OPENAI_ENDPOINT')
os.environ["AZURE_OPENAI_API_KEY"] = os.getenv('AZURE_OPENAI_API_KEY')

# Create an instance of Azure OpenAI
# Replace the deployment name with your own
llm = AzureOpenAI(
    deployment_name="gpt-35-turbo-instruct-0914",
)

async def main():
    """
    Connects to the MCP server using SSE transport, initializes the session, lists available tools,
    and calls the 'add' tool with example arguments (a=2, b=3), printing the result.
    """
    url = os.getenv('mcp-weather-url')

    # Connect to the server using SSE
    async with sse_client(url) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()

            # List available tools
            tools_result = await session.list_tools()
            print("Available tools:")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}")

            # Call our calculator tool
            result = await session.call_tool(f"{tool.name}", arguments={"city":"Pune"})
            print(f"Today's Weather forecasts {result.content[0].text}")


if __name__ == "__main__":
    asyncio.run(main())