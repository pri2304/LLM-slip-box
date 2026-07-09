from langchain_ollama import ChatOllama
from langchain.messages import HumanMessage, SystemMessage

llm = ChatOllama(model="qwen3.5:9b", reasoning=True)

while True:
    question = input("Enter the question you wish to ask: ")

    if question == "/bye":
        break

    messages = [
        SystemMessage("You are a deep philosopher"),
        HumanMessage(question),
    ]

    printing_reasoning = False

    for chunk in llm.stream(messages):
        for block in chunk.content_blocks:
            match block["type"]:
                case "reasoning":
                    if not printing_reasoning:
                        print("\nThinking:\n", end="")
                        printing_reasoning = True

                    print(block.get("reasoning", ""), end="", flush=True)

                case "text":
                    if printing_reasoning:
                        print("\n\nAnswer:\n", end="")
                        printing_reasoning = False

                    print(block["text"], end="", flush=True)
    print() #Add line so it prints terminal properly

