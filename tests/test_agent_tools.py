from app.agents.finagent import execute_tool


def test_unknown_tool_returns_error():
    result = execute_tool(
        db=None,
        tool_name="does_not_exist",
        arguments={},
    )

    assert result == {
        "error": "unknown_tool"
    }