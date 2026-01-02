import os
import json
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("WARNING: OPENAI_API_KEY not set!")

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_quiz_openai(topic: str, step_name: str) -> dict:
    """
    Generate a technical quiz with coding and concept questions using OpenAI.
    """
    prompt = f"""You are a technical interview quiz generator for developers.

Generate 15 multiple choice questions to test REAL technical knowledge of: {step_name}
Topic: {topic}

CRITICAL REQUIREMENTS:
1. Questions MUST be technical and specific to the topic
2. Include these question types:
   - Code output questions (What will this code print?)
   - Concept questions (What is the purpose of X?)
   - Best practice questions (Which approach is recommended for Y?)
   - Debugging questions (What's wrong with this code?)
   - Comparison questions (What's the difference between A and B?)
3. For coding questions, include actual code snippets in the question
4. Each question must have exactly 4 options (A, B, C, D)
5. Only ONE option should be correct
6. Explanation must teach WHY the answer is correct
7. Difficulty mix: 5 easy, 6 medium, 4 hard

EXAMPLE GOOD QUESTIONS:
- "What will console.log(typeof null) output in JavaScript?" 
- "In React, what hook is used to perform side effects?"
- "What is the time complexity of binary search?"
- "Which SQL keyword is used to filter grouped results?"

DO NOT ask generic questions like "Why is learning important?" or "What is the best approach to learn?"

Respond with valid JSON only:

{{"questions": [{{"id": 1,"question": "Technical question with code if applicable?","options": {{"A": "Option A","B": "Option B","C": "Option C","D": "Option D"}},"correct": "A","explanation": "Technical explanation of why A is correct","difficulty": "easy"}}]}}

Generate exactly 15 technical questions."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a senior technical interviewer. Generate challenging, real-world technical questions that test actual coding knowledge and concepts. Always include code snippets where relevant. Respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.8,
            max_tokens=4000
        )
        
        response_text = response.choices[0].message.content.strip()
        
        # Clean markdown formatting if present
        if response_text.startswith("```json"):
            response_text = response_text[7:]
        if response_text.startswith("```"):
            response_text = response_text[3:]
        if response_text.endswith("```"):
            response_text = response_text[:-3]
        
        response_text = response_text.strip()
        result = json.loads(response_text)
        
        # Validate we got questions
        if "questions" in result and len(result["questions"]) > 0:
            return result
        else:
            return get_fallback_quiz(topic)
    
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        return get_fallback_quiz(topic)
    except Exception as e:
        print(f"OpenAI quiz generation error: {e}")
        return get_fallback_quiz(topic)


def get_fallback_quiz(topic: str) -> dict:
    """Return technical fallback quiz when API fails."""
    topic_lower = topic.lower()
    
    # Python fallback
    if "python" in topic_lower:
        return {
            "questions": [
                {"id": 1, "question": "What will be the output of: print(type([]) == list)", "options": {"A": "True", "B": "False", "C": "Error", "D": "None"}, "correct": "A", "explanation": "type([]) returns <class 'list'>, which equals list, so the comparison returns True.", "difficulty": "easy"},
                {"id": 2, "question": "Which keyword is used to define a function in Python?", "options": {"A": "function", "B": "def", "C": "func", "D": "define"}, "correct": "B", "explanation": "In Python, 'def' keyword is used to define functions.", "difficulty": "easy"},
                {"id": 3, "question": "What is the output of: print(2 ** 3 ** 2)", "options": {"A": "64", "B": "512", "C": "36", "D": "81"}, "correct": "B", "explanation": "Exponentiation is right-associative, so 3**2=9 first, then 2**9=512.", "difficulty": "medium"},
                {"id": 4, "question": "What does the 'self' parameter represent in a Python class method?", "options": {"A": "The class itself", "B": "The instance of the class", "C": "A global variable", "D": "The parent class"}, "correct": "B", "explanation": "'self' refers to the instance of the class, allowing access to instance attributes and methods.", "difficulty": "easy"},
                {"id": 5, "question": "What will list('hello') return?", "options": {"A": "['hello']", "B": "['h', 'e', 'l', 'l', 'o']", "C": "'hello'", "D": "Error"}, "correct": "B", "explanation": "list() on a string creates a list of individual characters.", "difficulty": "easy"},
                {"id": 6, "question": "What is a Python decorator?", "options": {"A": "A way to add comments", "B": "A function that modifies another function", "C": "A type of loop", "D": "A class attribute"}, "correct": "B", "explanation": "Decorators are functions that wrap other functions to extend their behavior without modifying them.", "difficulty": "medium"},
                {"id": 7, "question": "What is the difference between '==' and 'is' in Python?", "options": {"A": "No difference", "B": "'==' compares values, 'is' compares identity", "C": "'is' compares values, '==' compares identity", "D": "'is' is faster"}, "correct": "B", "explanation": "'==' checks if values are equal, 'is' checks if both variables point to the same object in memory.", "difficulty": "medium"},
                {"id": 8, "question": "What will [1,2,3] + [4,5] return?", "options": {"A": "[1,2,3,4,5]", "B": "[[1,2,3],[4,5]]", "C": "[5,7,3]", "D": "Error"}, "correct": "A", "explanation": "The + operator concatenates lists, creating a new list with all elements.", "difficulty": "easy"},
                {"id": 9, "question": "What is a lambda function in Python?", "options": {"A": "A named function", "B": "An anonymous inline function", "C": "A class method", "D": "A built-in function"}, "correct": "B", "explanation": "Lambda functions are small anonymous functions defined with the lambda keyword.", "difficulty": "medium"},
                {"id": 10, "question": "What does *args do in a function definition?", "options": {"A": "Multiplies arguments", "B": "Accepts variable number of positional arguments", "C": "Accepts keyword arguments", "D": "Creates a pointer"}, "correct": "B", "explanation": "*args allows a function to accept any number of positional arguments as a tuple.", "difficulty": "medium"},
                {"id": 11, "question": "What is the output of: print({1, 2, 2, 3})", "options": {"A": "{1, 2, 2, 3}", "B": "{1, 2, 3}", "C": "[1, 2, 3]", "D": "Error"}, "correct": "B", "explanation": "Sets automatically remove duplicates, so {1, 2, 2, 3} becomes {1, 2, 3}.", "difficulty": "easy"},
                {"id": 12, "question": "What is the time complexity of accessing an element in a Python dictionary?", "options": {"A": "O(n)", "B": "O(log n)", "C": "O(1)", "D": "O(n²)"}, "correct": "C", "explanation": "Dictionary access is O(1) average case due to hash table implementation.", "difficulty": "hard"},
                {"id": 13, "question": "What does the 'yield' keyword do?", "options": {"A": "Returns a value and exits", "B": "Creates a generator, pausing execution", "C": "Raises an exception", "D": "Imports a module"}, "correct": "B", "explanation": "'yield' creates a generator function that can pause and resume, yielding values one at a time.", "difficulty": "hard"},
                {"id": 14, "question": "What is the output of: print('hello'[::-1])", "options": {"A": "'hello'", "B": "'olleh'", "C": "'h'", "D": "Error"}, "correct": "B", "explanation": "[::-1] reverses a string by stepping backwards through it.", "difficulty": "medium"},
                {"id": 15, "question": "What is a Python virtual environment used for?", "options": {"A": "Running code faster", "B": "Isolating project dependencies", "C": "Creating virtual machines", "D": "Debugging code"}, "correct": "B", "explanation": "Virtual environments isolate project dependencies to avoid conflicts between different projects.", "difficulty": "easy"}
            ]
        }
    
    # JavaScript/React fallback
    elif any(word in topic_lower for word in ["javascript", "react", "js", "frontend"]):
        return {
            "questions": [
                {"id": 1, "question": "What will console.log(typeof null) output?", "options": {"A": "'null'", "B": "'undefined'", "C": "'object'", "D": "'boolean'"}, "correct": "C", "explanation": "This is a known JavaScript quirk - typeof null returns 'object' due to a legacy bug.", "difficulty": "medium"},
                {"id": 2, "question": "In React, which hook is used to perform side effects?", "options": {"A": "useState", "B": "useEffect", "C": "useContext", "D": "useReducer"}, "correct": "B", "explanation": "useEffect is used for side effects like data fetching, subscriptions, or DOM manipulation.", "difficulty": "easy"},
                {"id": 3, "question": "What is the output of: console.log([] == false)", "options": {"A": "true", "B": "false", "C": "undefined", "D": "Error"}, "correct": "A", "explanation": "Empty array coerces to empty string, then to 0, and false also coerces to 0, so they're equal.", "difficulty": "hard"},
                {"id": 4, "question": "What does the spread operator (...) do?", "options": {"A": "Multiplies values", "B": "Expands iterables into individual elements", "C": "Creates a loop", "D": "Defines a function"}, "correct": "B", "explanation": "The spread operator expands arrays/objects into individual elements or properties.", "difficulty": "easy"},
                {"id": 5, "question": "What is the difference between let and const?", "options": {"A": "No difference", "B": "let can be reassigned, const cannot", "C": "const is faster", "D": "let is block-scoped, const is not"}, "correct": "B", "explanation": "Both are block-scoped, but const cannot be reassigned after declaration.", "difficulty": "easy"},
                {"id": 6, "question": "What will console.log(1 + '2' + 3) output?", "options": {"A": "6", "B": "'123'", "C": "'33'", "D": "Error"}, "correct": "B", "explanation": "1 + '2' = '12' (string concat), then '12' + 3 = '123'.", "difficulty": "medium"},
                {"id": 7, "question": "In React, what is the purpose of the key prop in lists?", "options": {"A": "Styling elements", "B": "Helping React identify which items changed", "C": "Sorting the list", "D": "Adding event handlers"}, "correct": "B", "explanation": "Keys help React identify which items have changed, been added, or removed for efficient re-rendering.", "difficulty": "easy"},
                {"id": 8, "question": "What is a closure in JavaScript?", "options": {"A": "A way to close the browser", "B": "A function with access to its outer scope", "C": "A type of loop", "D": "An error handler"}, "correct": "B", "explanation": "A closure is a function that remembers and can access variables from its outer scope even after the outer function has returned.", "difficulty": "medium"},
                {"id": 9, "question": "What does async/await do?", "options": {"A": "Makes code run faster", "B": "Handles promises in a synchronous-looking way", "C": "Creates threads", "D": "Imports modules"}, "correct": "B", "explanation": "async/await is syntactic sugar for promises, making asynchronous code easier to read and write.", "difficulty": "medium"},
                {"id": 10, "question": "What is the Virtual DOM in React?", "options": {"A": "The actual browser DOM", "B": "A lightweight copy of the DOM for efficient updates", "C": "A CSS framework", "D": "A testing tool"}, "correct": "B", "explanation": "Virtual DOM is a lightweight JavaScript representation of the DOM that React uses to minimize actual DOM manipulations.", "difficulty": "easy"},
                {"id": 11, "question": "What will console.log(0.1 + 0.2 === 0.3) output?", "options": {"A": "true", "B": "false", "C": "undefined", "D": "Error"}, "correct": "B", "explanation": "Due to floating-point precision issues, 0.1 + 0.2 = 0.30000000000000004, not exactly 0.3.", "difficulty": "hard"},
                {"id": 12, "question": "What is the purpose of useCallback hook?", "options": {"A": "To fetch data", "B": "To memoize functions and prevent unnecessary re-renders", "C": "To manage state", "D": "To handle errors"}, "correct": "B", "explanation": "useCallback memoizes functions so they don't get recreated on every render, useful for optimization.", "difficulty": "medium"},
                {"id": 13, "question": "What is event bubbling?", "options": {"A": "Events only fire on the target", "B": "Events propagate from target up to ancestors", "C": "Events propagate from ancestors down to target", "D": "Events are cancelled"}, "correct": "B", "explanation": "Event bubbling means events propagate upward from the target element through its ancestors.", "difficulty": "medium"},
                {"id": 14, "question": "What does JSON.stringify({a: undefined}) return?", "options": {"A": "'{\"a\":undefined}'", "B": "'{}'", "C": "'{\"a\":null}'", "D": "Error"}, "correct": "B", "explanation": "JSON.stringify omits properties with undefined values, resulting in an empty object string.", "difficulty": "hard"},
                {"id": 15, "question": "What is prop drilling in React?", "options": {"A": "A performance optimization", "B": "Passing props through multiple component levels", "C": "A testing technique", "D": "A styling method"}, "correct": "B", "explanation": "Prop drilling is passing props through intermediate components that don't need them, just to reach deeply nested components.", "difficulty": "easy"}
            ]
        }
    
    # SQL/Database fallback
    elif any(word in topic_lower for word in ["sql", "database", "data"]):
        return {
            "questions": [
                {"id": 1, "question": "Which SQL clause is used to filter rows?", "options": {"A": "SELECT", "B": "WHERE", "C": "FROM", "D": "ORDER BY"}, "correct": "B", "explanation": "WHERE clause filters rows based on specified conditions.", "difficulty": "easy"},
                {"id": 2, "question": "What is the difference between INNER JOIN and LEFT JOIN?", "options": {"A": "No difference", "B": "INNER returns only matching rows, LEFT returns all from left table", "C": "LEFT is faster", "D": "INNER returns all rows"}, "correct": "B", "explanation": "INNER JOIN returns only matching rows, LEFT JOIN returns all rows from left table plus matches from right.", "difficulty": "medium"},
                {"id": 3, "question": "Which keyword removes duplicate rows from results?", "options": {"A": "UNIQUE", "B": "DISTINCT", "C": "DIFFERENT", "D": "SINGLE"}, "correct": "B", "explanation": "DISTINCT keyword removes duplicate rows from the result set.", "difficulty": "easy"},
                {"id": 4, "question": "What does GROUP BY do?", "options": {"A": "Sorts results", "B": "Groups rows with same values for aggregate functions", "C": "Filters rows", "D": "Joins tables"}, "correct": "B", "explanation": "GROUP BY groups rows with identical values, typically used with aggregate functions like COUNT, SUM.", "difficulty": "easy"},
                {"id": 5, "question": "Which clause filters grouped results?", "options": {"A": "WHERE", "B": "HAVING", "C": "GROUP BY", "D": "ORDER BY"}, "correct": "B", "explanation": "HAVING filters groups after GROUP BY, while WHERE filters individual rows before grouping.", "difficulty": "medium"},
                {"id": 6, "question": "What is a PRIMARY KEY?", "options": {"A": "Any column", "B": "A unique identifier for each row", "C": "A foreign reference", "D": "An index"}, "correct": "B", "explanation": "PRIMARY KEY uniquely identifies each row in a table and cannot contain NULL values.", "difficulty": "easy"},
                {"id": 7, "question": "What does FOREIGN KEY do?", "options": {"A": "Creates a new table", "B": "Links two tables by referencing primary key of another table", "C": "Deletes rows", "D": "Sorts data"}, "correct": "B", "explanation": "FOREIGN KEY creates a relationship between tables by referencing the PRIMARY KEY of another table.", "difficulty": "medium"},
                {"id": 8, "question": "What is the result of: SELECT COUNT(*) FROM table WHERE 1=0", "options": {"A": "NULL", "B": "0", "C": "Error", "D": "All rows"}, "correct": "B", "explanation": "1=0 is always false, so no rows match, and COUNT(*) returns 0.", "difficulty": "medium"},
                {"id": 9, "question": "What is database normalization?", "options": {"A": "Making database faster", "B": "Organizing data to reduce redundancy", "C": "Adding more tables", "D": "Backing up data"}, "correct": "B", "explanation": "Normalization organizes database structure to minimize data redundancy and improve integrity.", "difficulty": "medium"},
                {"id": 10, "question": "What does COALESCE function do?", "options": {"A": "Joins strings", "B": "Returns first non-NULL value", "C": "Counts rows", "D": "Converts data types"}, "correct": "B", "explanation": "COALESCE returns the first non-NULL value from a list of arguments.", "difficulty": "hard"},
                {"id": 11, "question": "What is an INDEX used for?", "options": {"A": "Storing data", "B": "Speeding up data retrieval", "C": "Joining tables", "D": "Filtering rows"}, "correct": "B", "explanation": "Indexes speed up data retrieval by creating a quick lookup structure, like a book index.", "difficulty": "easy"},
                {"id": 12, "question": "What is a subquery?", "options": {"A": "A backup query", "B": "A query nested inside another query", "C": "A deleted query", "D": "A fast query"}, "correct": "B", "explanation": "A subquery is a query nested within another SQL query, used in WHERE, FROM, or SELECT clauses.", "difficulty": "medium"},
                {"id": 13, "question": "What does UNION do?", "options": {"A": "Joins tables horizontally", "B": "Combines results of two queries vertically", "C": "Filters duplicates", "D": "Creates a view"}, "correct": "B", "explanation": "UNION combines result sets of two queries, removing duplicates (use UNION ALL to keep duplicates).", "difficulty": "medium"},
                {"id": 14, "question": "What is ACID in databases?", "options": {"A": "A query language", "B": "Properties ensuring reliable transactions", "C": "A database type", "D": "An index type"}, "correct": "B", "explanation": "ACID (Atomicity, Consistency, Isolation, Durability) ensures database transactions are reliable.", "difficulty": "hard"},
                {"id": 15, "question": "What does TRUNCATE do compared to DELETE?", "options": {"A": "Same thing", "B": "TRUNCATE removes all rows faster, can't use WHERE", "C": "DELETE is faster", "D": "TRUNCATE adds rows"}, "correct": "B", "explanation": "TRUNCATE removes all rows quickly without logging individual deletions, but can't filter with WHERE.", "difficulty": "hard"}
            ]
        }
    
    # Generic programming fallback
    else:
        return {
            "questions": [
                {"id": 1, "question": "What is the time complexity of binary search?", "options": {"A": "O(n)", "B": "O(log n)", "C": "O(n²)", "D": "O(1)"}, "correct": "B", "explanation": "Binary search halves the search space each iteration, giving O(log n) complexity.", "difficulty": "medium"},
                {"id": 2, "question": "What is a stack data structure?", "options": {"A": "First In First Out", "B": "Last In First Out", "C": "Random access", "D": "Sorted order"}, "correct": "B", "explanation": "Stack follows LIFO - the last element added is the first one removed.", "difficulty": "easy"},
                {"id": 3, "question": "What is recursion?", "options": {"A": "A loop type", "B": "A function calling itself", "C": "A data structure", "D": "An error"}, "correct": "B", "explanation": "Recursion is when a function calls itself to solve smaller instances of the same problem.", "difficulty": "easy"},
                {"id": 4, "question": "What is the difference between an array and a linked list?", "options": {"A": "No difference", "B": "Arrays have contiguous memory, linked lists use pointers", "C": "Linked lists are faster", "D": "Arrays can't store numbers"}, "correct": "B", "explanation": "Arrays store elements in contiguous memory locations, linked lists use nodes connected by pointers.", "difficulty": "medium"},
                {"id": 5, "question": "What is Big O notation used for?", "options": {"A": "Measuring code length", "B": "Describing algorithm efficiency/complexity", "C": "Counting variables", "D": "Debugging"}, "correct": "B", "explanation": "Big O notation describes the upper bound of an algorithm's time or space complexity.", "difficulty": "easy"},
                {"id": 6, "question": "What is a hash table?", "options": {"A": "A sorted array", "B": "A data structure using key-value pairs with O(1) average access", "C": "A type of tree", "D": "A linked list"}, "correct": "B", "explanation": "Hash tables store key-value pairs and provide O(1) average time complexity for lookups.", "difficulty": "medium"},
                {"id": 7, "question": "What is polymorphism in OOP?", "options": {"A": "Multiple inheritance", "B": "Objects of different types responding to same method", "C": "Hiding data", "D": "Creating objects"}, "correct": "B", "explanation": "Polymorphism allows objects of different classes to be treated as objects of a common parent class.", "difficulty": "medium"},
                {"id": 8, "question": "What is the purpose of version control?", "options": {"A": "Making code faster", "B": "Tracking changes and enabling collaboration", "C": "Compiling code", "D": "Testing code"}, "correct": "B", "explanation": "Version control tracks code changes over time and enables team collaboration.", "difficulty": "easy"},
                {"id": 9, "question": "What is an API?", "options": {"A": "A programming language", "B": "An interface for software components to communicate", "C": "A database", "D": "A testing tool"}, "correct": "B", "explanation": "API (Application Programming Interface) defines how software components should interact.", "difficulty": "easy"},
                {"id": 10, "question": "What is the difference between HTTP GET and POST?", "options": {"A": "No difference", "B": "GET retrieves data, POST sends data to server", "C": "POST is faster", "D": "GET is more secure"}, "correct": "B", "explanation": "GET requests data from server, POST submits data to be processed by server.", "difficulty": "easy"},
                {"id": 11, "question": "What is a deadlock?", "options": {"A": "A fast algorithm", "B": "When processes wait indefinitely for each other's resources", "C": "A type of loop", "D": "A security feature"}, "correct": "B", "explanation": "Deadlock occurs when processes are blocked forever, each waiting for resources held by others.", "difficulty": "hard"},
                {"id": 12, "question": "What is encapsulation in OOP?", "options": {"A": "Inheritance", "B": "Bundling data and methods, hiding internal details", "C": "Creating multiple objects", "D": "Using interfaces"}, "correct": "B", "explanation": "Encapsulation bundles data with methods that operate on it and restricts direct access to internal details.", "difficulty": "medium"},
                {"id": 13, "question": "What is a REST API?", "options": {"A": "A database", "B": "An architectural style using HTTP methods for web services", "C": "A programming language", "D": "A testing framework"}, "correct": "B", "explanation": "REST is an architectural style that uses HTTP methods (GET, POST, PUT, DELETE) for web services.", "difficulty": "medium"},
                {"id": 14, "question": "What is the purpose of unit testing?", "options": {"A": "Testing the entire application", "B": "Testing individual components in isolation", "C": "Testing user interface", "D": "Testing performance"}, "correct": "B", "explanation": "Unit testing verifies individual components or functions work correctly in isolation.", "difficulty": "easy"},
                {"id": 15, "question": "What is memoization?", "options": {"A": "A sorting algorithm", "B": "Caching results of expensive function calls", "C": "A data structure", "D": "A design pattern"}, "correct": "B", "explanation": "Memoization caches results of expensive function calls to avoid redundant computations.", "difficulty": "hard"}
            ]
        }
