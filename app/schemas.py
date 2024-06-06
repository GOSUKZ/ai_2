import logging
import json
import os
from app.promts import system_promt
from app.functions import (
    find_cars_by_price,
    find_cars_by_name,
    find_cars_by_model,
    find_cars_by_mileage,
    find_cars_by_year,
    find_apartments_by_square,
    find_apartments_by_address,
    find_apartments_by_price,
    find_apartments_by_district
)
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.environ['OPENAI_API_KEY']

client = OpenAI(api_key=TOKEN)

user_contexts = {}


def run_conversation(user_id, content):
    print(content)
    if user_id not in user_contexts:
        user_contexts[user_id] = [{"role": "system", "content": system_promt}, {"role": "user", "content": content}]
    else:
        user_contexts[user_id].append({"role": "user", "content": content})

    tools = [
        {
            "type": "function",
            "function": {
                "name": "find_cars_by_price",
                "description": "Find cars with the  price",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "price": {"type": "number", "description": "The price"},
                    },
                    "required": ["price"],
                },
            }
        },
        {
            "type": "function",
            "function": {
                "name": "find_cars_by_name",
                "description": "Find cars by name",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "name": {"type": "string", "description": "The name of the car"},
                    },
                    "required": ["name"],
                },
            }
        },
        {
            "type": "function",
            "function": {
                "name": "find_cars_by_model",
                "description": "Find cars by model",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "model": {"type": "string", "description": "The model of the car"},
                    },
                    "required": ["model"],
                },
            }
        },
        {
            "type": "function",
            "function": {
                "name": "find_cars_by_mileage",
                "description": "Find cars by mileage",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "mileage": {"type": "number", "description": "The mileage"},
                    },
                    "required": ["mileage"],
                },
            }
        },
        {
            "type": "function",
            "function": {
                "name": "find_cars_by_year",
                "description": "Find cars by year",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "year": {"type": "string", "description": "The year of the car"},
                    },
                    "required": ["year"],
                },
            }
        },
        {
            "type": "function",
            "function": {
                "name": "find_apartments_by_square",
                "description": "Find apartments by square footage",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "square": {"type": "number", "description": "The square footage"},

                    },
                    "required": ["square"],
                },
            }
        },
        {
            "type": "function",
            "function": {
                "name": "find_apartments_by_address",
                "description": "Find apartments by address",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "address": {"type": "string", "description": "The address of the apartment"},
                    },
                    "required": ["address"],
                },
            }
        },
        {
            "type": "function",
            "function": {
                "name": "find_apartments_by_price",
                "description": "Find apartments within the specified price range",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "price": {"type": "number", "description": "The price"},
                    },
                    "required": ["price"],
                },
            }
        },
        {
            "type": "function",
            "function": {
                "name": "find_apartments_by_district",
                "description": "Find apartments by district",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "district": {"type": "string", "description": "The district of the apartment"},
                    },
                    "required": ["district"],
                },
            }
        },
    ]

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=user_contexts[user_id],
            tools=tools,
            tool_choice="auto",
            temperature=0.5
        )
    except Exception as e:
        logging.error(f"Error calling OpenAI API: {e}")
        return None

    if response and response.choices:
        response_message = response.choices[0].message
        user_contexts[user_id].append(response_message)
        tool_calls = response_message.tool_calls

        if tool_calls:
            available_functions = {
                "find_cars_by_price": find_cars_by_price,
                "find_cars_by_name": find_cars_by_name,
                "find_cars_by_model": find_cars_by_model,
                "find_cars_by_mileage": find_cars_by_mileage,
                "find_cars_by_year": find_cars_by_year,
                "find_apartments_by_square": find_apartments_by_square,
                "find_apartments_by_address": find_apartments_by_address,
                "find_apartments_by_price": find_apartments_by_price,
                "find_apartments_by_district": find_apartments_by_district,
            }
            for tool_call in tool_calls:
                logging.info(f"Function: {tool_call.function.name}")
                logging.info(f"Params: {tool_call.function.arguments}")
                function_name = tool_call.function.name
                function_to_call = available_functions[function_name]
                function_args = json.loads(tool_call.function.arguments)
                function_response = function_to_call(**function_args)
                logging.info(f"API: {function_response}")
                user_contexts[user_id].append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )

            second_response = client.chat.completions.create(
                temperature=0.5,
                model="gpt-4o",
                messages=user_contexts[user_id],
                stream=False

            )
            return second_response
    return response
