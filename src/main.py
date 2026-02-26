import json
from llm import LLMChat
from config import MODEL, API_URL, SYSTEM_PROMPT, TOOL_REQUEST_PATTERN

def _extract_tool_request(content: str):
    match = TOOL_REQUEST_PATTERN.search(content)
    if not match:
        return None
    
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError as e:
        return None

def _call_functions(llm: LLMChat, reply: dict):
    tool_request = _extract_tool_request(reply.get("content"))
    if tool_request and tool_request.get("name") == "exec_bash_command":
        args = tool_request["arguments"]["cmd"]

        confirm_execution = input(f"Execute command: {args}? (y/n): ")
        if confirm_execution.lower() != 'y':
            shell_result = {"Error": "Command execution cancelled by user."}
        else:
            shell_result = llm.bash.exec_bash_command(args)

        llm.messages.append({
            "role": "tool",
            "name": "exec_bash_command",
            "content": json.dumps(shell_result)
        })

        return shell_result


llm = LLMChat(model=MODEL, api_url=API_URL, system_prompt=SYSTEM_PROMPT)

while True:
    user = input(f"{llm.bash.cwd}> User: ")
    reply = llm.query(message=user, tools=[llm.bash.to_json_schema()])

    if reply:
        function_call_result = _call_functions(llm, reply)
        if function_call_result:
            if function_call_result.get("stdout"):
                print(f"{function_call_result['stdout']}")
                continue
            elif function_call_result.get("stderr"):
                print(f"Error: {function_call_result['stderr']}")
                continue
    
    last_message = llm.messages[-1]["content"]
    print(f"{last_message}")
