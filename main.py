import time
import re
import os # For creating directories if needed

# Import our tools from the 'tools' package
from tools import weather_tool
from tools import time_tool
from tools import calculator_tool

class DynamicAgent:
    def __init__(self, name="SmartAgent"):
        self.name = name
        self.available_tools = {
            "get_weather": weather_tool.get_weather,
            "get_current_time": time_tool.get_current_time,
            "calculate": calculator_tool.calculate,
        }
        self.tool_descriptions = {
            "get_weather": "Provides current weather information for a given city. Requires 'location' argument.",
            "get_current_time": "Provides the current local time. No arguments needed.",
            "calculate": "Evaluates a simple mathematical expression. Requires 'expression' argument (e.g., '5+3')."
        }
        self.conversation_history = []
        self.last_response = ""

    def _execute_tool(self, tool_name, **kwargs):
        """Executes a registered tool and returns its result."""
        if tool_name in self.available_tools:
            print(f"[{self.name}] Executing tool: '{tool_name}' with args: {kwargs}")
            try:
                result = self.available_tools[tool_name](**kwargs)
                return result
            except TypeError as e:
                # Catch cases where required args are missing for a tool
                return {"status": "error", "result": f"Error: Missing or incorrect arguments for '{tool_name}'. {e}"}
            except Exception as e:
                return {"status": "error", "result": f"Error executing '{tool_name}': {e}"}
        return {"status": "error", "result": f"Unknown tool: '{tool_name}'."}

    def _parse_and_decide(self, user_input):
        """
        The core "brain" of the agent.
        It attempts to identify the user's intent and necessary tool(s) and parameters.
        This is a *simulated* dynamic tool selection process.
        In a real LLM-powered agent, this would be handled by the LLM's reasoning.
        """
        user_input_lower = user_input.lower()
        response = "I'm sorry, I couldn't understand your request or find a suitable tool to help. Can you please rephrase?"
        tool_executed = False

        # Try to match to weather tool
        weather_match = re.search(r'weather in ([\w\s]+)\??', user_input_lower)
        if "weather" in user_input_lower:
            location = "Karachi" # Default if not specified
            if weather_match:
                location = weather_match.group(1).strip()
            tool_result = self._execute_tool("get_weather", location=location.title()) # Capitalize location for display
            if tool_result["status"] == "success":
                response = tool_result["result"]
                tool_executed = True
            else:
                response = tool_result["result"] # Propagate error message from tool

        # Try to match to time tool
        elif "time" in user_input_lower and ("what" in user_input_lower or "current" in user_input_lower):
            tool_result = self._execute_tool("get_current_time")
            if tool_result["status"] == "success":
                response = tool_result["result"]
                tool_executed = True
            else:
                response = tool_result["result"]

        # Try to match to calculator tool
        # Example patterns: "calculate 5+3", "what is 10 times 2", "solve 2* (4+1)"
        calc_match = re.search(r'(calculate|what is|solve|eval)\s+([\d\s\+\-\*\/\(\).]+)', user_input_lower)
        if calc_match:
            expression = calc_match.group(2).strip()
            # Basic sanitization, but full security requires a proper parser
            expression = expression.replace("times", "*").replace("plus", "+").replace("minus", "-").replace("divided by", "/")
            tool_result = self._execute_tool("calculate", expression=expression)
            if tool_result["status"] == "success":
                response = tool_result["result"]
                tool_executed = True
            else:
                response = tool_result["result"]

        # General helpful phrases/greetings
        elif "hello" in user_input_lower or "hi" in user_input_lower:
            response = "Hello! How can I assist you today?"
            tool_executed = True
        elif "how are you" in user_input_lower:
            response = "I am an AI, so I don't have feelings, but I'm functioning well and ready to help!"
            tool_executed = True
        elif "what can you do" in user_input_lower:
            tools_list = ", ".join([desc.split('.')[0] for desc in self.tool_descriptions.values()])
            response = f"I can help you with: {tools_list}. Just ask!"
            tool_executed = True

        self.last_response = response
        return response

    def start_conversation(self):
        """Starts the interactive conversation loop."""
        print(f"\n[{self.name}] Hi there! I'm {self.name}. How can I assist you today?")
        print("You can ask me about the time, weather, or ask me to calculate something.")
        print("Type 'quit' or 'exit' to end the conversation.")

        while True:
            user_input = input("\nYou: ")
            self.conversation_history.append(f"User: {user_input}")

            if user_input.lower() in ["quit", "exit"]:
                print(f"[{self.name}] Goodbye! It was a pleasure assisting you.")
                break

            response = self._parse_and_decide(user_input)
            print(f"{self.name}: {response}")
            self.conversation_history.append(f"Agent: {response}")
            time.sleep(0.2) # Small delay for better flow

# --- Main Execution ---
if __name__ == "__main__":
    # Ensure the 'tools' directory and its modules are discoverable
    # This setup implies that 'main.py' is in the parent directory of 'tools/'

    # You could also add a dummy 'data' directory if you anticipate file I/O
    # import os
    # if not os.path.exists("data"):
    #     os.makedirs("data")
    #     print("Created 'data' directory.")

    agent = DynamicAgent()
    agent.start_conversation()