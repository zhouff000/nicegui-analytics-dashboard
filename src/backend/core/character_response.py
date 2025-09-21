from typing import Dict, Any, Optional, Generator, Iterator
from dataclasses import dataclass
from enum import Enum


class DataSource(Enum):
    """Data source type enumeration"""

    DATABASE = "database"
    LLM = "llm"


@dataclass
class CharacterResponse:
    """Unified Chinese character response wrapper class"""

    character: str
    scenario: str
    source: DataSource
    content: Optional[str] = None
    reasoning_content: Optional[str] = None  # New field for reasoning content
    is_streaming: bool = False
    _llm_response: Optional[Any] = None
    _stream_generator: Optional[Generator] = None

    def get_content(self) -> str:
        """Get response content"""
        if self.source == DataSource.DATABASE:
            return self.content or ""
        elif self.source == DataSource.LLM and self._llm_response:
            return self._llm_response.choices[0].message.content or ""
        return ""

    def get_reasoning_content(self) -> str:
        """Get reasoning content (LLM only)"""
        if self.source == DataSource.DATABASE:
            return ""  # Database data has no reasoning content
        elif self.source == DataSource.LLM and self._llm_response:
            # Check if reasoning content exists
            if hasattr(self._llm_response.choices[0].message, "reasoning_content"):
                return self._llm_response.choices[0].message.reasoning_content or ""
        return self.reasoning_content or ""

    def stream_content(self) -> Iterator[Dict[str, str]]:
        """Stream content (LLM only)

        Returns:
            Iterator of dictionaries containing content and reasoning_content
        """
        if not self.is_streaming or not self._stream_generator:
            raise ValueError("This response does not support streaming")

        for chunk in self._stream_generator:
            result = {}

            # Check regular content
            if (
                hasattr(chunk.choices[0].delta, "content")
                and chunk.choices[0].delta.content
            ):
                result["content"] = chunk.choices[0].delta.content

            # Check reasoning content
            if (
                hasattr(chunk.choices[0].delta, "reasoning_content")
                and chunk.choices[0].delta.reasoning_content
            ):
                result["reasoning_content"] = chunk.choices[0].delta.reasoning_content

            # Only yield when there's content
            if result:
                yield result

    def stream_content_only(self) -> Iterator[str]:
        """Stream content only (backward compatibility)"""
        for chunk_data in self.stream_content():
            if "content" in chunk_data:
                yield chunk_data["content"]

    def stream_reasoning_only(self) -> Iterator[str]:
        """Stream reasoning content only"""
        for chunk_data in self.stream_content():
            if "reasoning_content" in chunk_data:
                yield chunk_data["reasoning_content"]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format"""
        result = {
            "character": self.character,
            "scenario": self.scenario,
            "source": self.source.value,
            "content": self.get_content(),
            "is_streaming": self.is_streaming,
        }

        # Add reasoning content if available
        reasoning = self.get_reasoning_content()
        if reasoning:
            result["reasoning_content"] = reasoning

        return result


def create_database_response(
    character: str, scenario: str, db_data: Dict[str, Any]
) -> CharacterResponse:
    """Create database response"""
    # Extract content from database data, adjust according to actual fields
    content_fields = [
        "id",
        "source",
        "character",
        "pronunciation",
        "stroke",
        "meaning",
        "idioms",
        "culture",
        "practice",
    ]
    content = ""

    for field in content_fields:
        if field in db_data and db_data[field]:
            content = str(db_data[field])
            break

    # If no content field found, use string representation of all data
    if not content:
        content = str(db_data)

    return CharacterResponse(
        character=character,
        scenario=scenario,
        source=DataSource.DATABASE,
        content=content,
        is_streaming=False,
    )


def create_llm_response(
    character: str, scenario: str, llm_response: Any, stream: bool = False
) -> CharacterResponse:
    """Create LLM response"""
    if stream:
        return CharacterResponse(
            character=character,
            scenario=scenario,
            source=DataSource.LLM,
            is_streaming=True,
            _stream_generator=llm_response,
        )
    else:
        # For non-streaming response, try to extract reasoning content
        reasoning_content = ""
        if hasattr(llm_response.choices[0].message, "reasoning_content"):
            reasoning_content = llm_response.choices[0].message.reasoning_content or ""

        return CharacterResponse(
            character=character,
            scenario=scenario,
            source=DataSource.LLM,
            reasoning_content=reasoning_content,
            is_streaming=False,
            _llm_response=llm_response,
        )
