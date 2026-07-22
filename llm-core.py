from langchain_ollama import ChatOllama
from langchain.messages import HumanMessage, SystemMessage, ToolMessage
from slip_box_tools import create_note, search_notes, explore_links, create_link
from pathlib import Path
import json
from prompt_toolkit import prompt

SYSTEM_PROMPT = Path("prompts/systemprompt.txt").read_text(encoding="utf-8")

llm = ChatOllama(model="qwen3.5:9b", reasoning=True)
TOOLS = {
    "create_note": create_note,
    "search_notes": search_notes,
    "explore_links": explore_links,
    "create_link": create_link
}

llm = llm.bind_tools(list(TOOLS.values()))

messages = [SystemMessage(content=SYSTEM_PROMPT)]

while True:
    question = prompt("> ", multiline=True)

    question = question.strip()

    if question == "/bye":
        break

    messages.append(HumanMessage(question))

    while True:

        response = llm.invoke(messages)

        messages.append(response) #Saving assistant response to history

        reasoning = ""

        for block in response.content_blocks:
            if block["type"] == "reasoning":
                reasoning += block.get("reasoning", "")

        if reasoning:
            print("Thinking:")
            print(reasoning)

        if response.tool_calls:
            for tool_call in response.tool_calls:
                print("Tool Calls:")

                print(tool_call["name"])
                print(tool_call["args"])

                tool = TOOLS.get(tool_call["name"])

                if tool:

                    args = tool_call["args"]

                    print(type(args))
                    print(args)

                    # Temporary workaround for models that return JSON strings
                    if (
                            tool_call["name"] == "create_note"
                            and isinstance(args.get("note"), str)
                    ):
                        args["note"] = json.loads(args["note"])

                    result = tool.invoke(args)

                else:

                    result = "Unknown tool."

                print("\nTool Result:")
                print(result)

                messages.append(
                    ToolMessage(
                        content=str(result),
                        tool_call_id=tool_call["id"],
                    )
                )

            continue

        answer = ""

        for block in response.content_blocks:
            if block["type"] == "text":
                answer += block["text"]

        print(answer)
        break


