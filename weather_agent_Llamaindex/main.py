import asyncio
import os
import pathlib
from typing import List
from dotenv import load_dotenv

# LlamaIndex imports for the agent, LLM, and MCP tools
from llama_index.core.agent.workflow import ReActAgent
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.tools.mcp import BasicMCPClient, McpToolSpec

# Load environment variables from the parent directory's .env file
env_path = pathlib.Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

async def main():
    """
    Main function to set up and run the LlamaIndex agent.
    """
    print("Initializing LlamaIndex agent...")

    # 1. Set up the LLM
    # Load API key from environment variable
    google_api_key = os.getenv("GOOGLE_GEMINI_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_GEMINI_API_KEY environment variable is not set. Please check your .env file.")
    
    llm = GoogleGenAI(
        model_name="gemini-1.5-flash",
        api_key=google_api_key
    )
    # 2. Set up the MCP client and tools
    # We pass the stdio configuration dictionary directly to the client
    # Use absolute path to the MCP server
    mcp_server_path = pathlib.Path(__file__).parent.parent / 'mcp_server' / 'main.py'
    mcp_client = BasicMCPClient("python", args=[str(mcp_server_path)])

    # McpToolSpec is a LlamaIndex-native way to wrap MCP tools
    tool_spec = McpToolSpec(client=mcp_client)

    # The agent will use the tools loaded from the MCP server
    # We use the async method to fetch the tool definitions
    mcp_tools: List = await tool_spec.to_tool_list_async()
    print(f"Successfully loaded {len(mcp_tools)} tool(s) from the MCP server.")

    # 3. Create the LlamaIndex Agent
    # We use a ReActAgent, a standard and powerful agent type in LlamaIndex
    # It will use the Gemini LLM to reason about when to use the loaded MCP tools
    agent = ReActAgent(tools=mcp_tools, llm=llm, verbose=False)

    print("\nWeather MCP agent is ready. Ask for the weather (e.g., 'What is the weather in London?').")

    # 4. Start the conversation loop
    while True:
        user_input = input("\nYou: ").strip()
        if user_input.lower() in {"exit", "quit", "q"}:
            print("Exiting.")
            break

        if not user_input:
            continue

        try:
            # The agent's chat method handles the full reasoning and tool-calling loop
            response = await agent.run(user_input)
            print("AI:", str(response))
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    # Ensure you have a running asyncio event loop
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")