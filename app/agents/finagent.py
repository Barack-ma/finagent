import json
import os

from openai import OpenAI
from sqlalchemy.orm import Session

from app.agents.tools import (
    tool_get_customer_summary,
    tool_get_loan,
    tool_get_payoff_estimate,
    tool_make_payment,
    tool_search_policy,
)


client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_customer_summary",
            "description": (
                "Retrieve a customer's current financial summary."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "customer_id": {
                        "type": "string"
                    }
                },
                "required": ["customer_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_loan",
            "description": (
                "Retrieve details for a specific loan."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "loan_id": {
                        "type": "string"
                    }
                },
                "required": ["loan_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_payoff_estimate",
            "description": (
                "Retrieve an estimated payoff amount for a loan."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "loan_id": {
                        "type": "string"
                    }
                },
                "required": ["loan_id"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_policy",
            "description": (
                "Search approved lending policy documents."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string"
                    },
                    "top_k": {
                        "type": "integer",
                        "default": 3
                    },
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "make_payment",
            "description": (
                "Execute a loan payment after the user's intent "
                "and amount are clear."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "loan_id": {
                        "type": "string"
                    },
                    "amount": {
                        "type": "string"
                    },
                },
                "required": [
                    "loan_id",
                    "amount",
                ],
            },
        },
    },
]

def execute_tool(
    db: Session,
    tool_name: str,
    arguments: dict,
):
    if tool_name == "get_customer_summary":
        return tool_get_customer_summary(
            db,
            **arguments,
        )

    if tool_name == "get_loan":
        return tool_get_loan(
            db,
            **arguments,
        )

    if tool_name == "get_payoff_estimate":
        return tool_get_payoff_estimate(
            db,
            **arguments,
        )

    if tool_name == "search_policy":
        return tool_search_policy(
            **arguments,
        )

    if tool_name == "make_payment":
        return tool_make_payment(
            db,
            **arguments,
        )

    return {
        "error": "unknown_tool"
    }


SYSTEM_PROMPT = """
You are FinAgent, an AI assistant for consumer lending operations.

Rules:
- Never invent account balances, loan details, payment history, or policy.
- Use tools whenever account-specific or policy-specific information is required.
- Never directly calculate or modify database values yourself when a tool exists.
- Do not claim a payment succeeded unless the make_payment tool succeeds.
- If a user asks for a discretionary action such as a fee waiver, interest-rate change,
  loan modification, or delinquency removal, search policy and explain whether escalation
  is required.
- Distinguish estimated payoff amounts from official payoff quotes.
- If required information such as a customer ID or loan ID is missing, ask for it.
"""

def run_finagent(
    db: Session,
    user_message: str,
) -> str:
    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": user_message,
        },
    ]

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        tools=TOOLS,
        tool_choice="auto",
    )

    assistant_message = response.choices[0].message

    if not assistant_message.tool_calls:
        return assistant_message.content or ""

    messages.append(
        assistant_message
    )

    for tool_call in assistant_message.tool_calls:
        tool_name = tool_call.function.name

        arguments = json.loads(
            tool_call.function.arguments
        )

        result = execute_tool(
            db,
            tool_name,
            arguments,
        )

        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(result),
            }
        )

    final_response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        tools=TOOLS,
    )

    return (
        final_response
        .choices[0]
        .message
        .content
        or ""
    )