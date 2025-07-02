def calculate(expression):
    """
    Evaluates a simple mathematical expression.
    Args:
        expression (str): The mathematical expression to evaluate (e.g., "5+3", "10*2").
    Returns:
        dict: A dictionary with 'status' and 'result' of the operation.
    """
    print(f"[Tool: Calculator] Calculating expression: '{expression}'")
    try:
        # Using eval() for simplicity in this demo.
        # In a real application, a safer math expression parser would be used
        # to prevent security vulnerabilities.
        result = eval(str(expression))
        print(f"[Tool: Calculator] Result: {result}")
        return {"status": "success", "result": f"The result of '{expression}' is {result}."}
    except (SyntaxError, TypeError, NameError) as e:
        print(f"[Tool: Calculator] Invalid expression: {e}")
        return {"status": "failure", "result": f"Could not calculate '{expression}'. Invalid expression."}
    except Exception as e:
        print(f"[Tool: Calculator] An unexpected error occurred: {e}")
        return {"status": "failure", "result": f"An error occurred during calculation."}

if __name__ == '__main__':
    # Simple test for the tool
    print(calculate("10 + 5"))
    print(calculate("7 * 3 - 2"))
    print(calculate("invalid expression"))