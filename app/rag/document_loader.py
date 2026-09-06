from dataclasses import dataclass
from pathlib import Path


@dataclass
class PolicyDocument:
    source: str
    text: str


def load_policy_documents(
    directory: str = "data/policies",
) -> list[PolicyDocument]:
    policy_directory = Path(directory)

    documents: list[PolicyDocument] = []

    for file_path in policy_directory.glob("*.txt"):
        text = file_path.read_text(
            encoding="utf-8"
        )

        documents.append(
            PolicyDocument(
                source=file_path.name,
                text=text,
            )
        )

    return documents