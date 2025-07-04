#!/usr/bin/env python3
"""
EduChain MCP Server
===================

A Model Context Protocol (MCP) server that integrates EduChain's educational content
generation capabilities with Claude Desktop and other MCP-compatible clients.

This server exposes three main educational tools:
- Multiple-choice questions (MCQs) generation
- Structured lesson plan creation
- Educational flashcard generation

Features:
---------
- Seamless integration with Claude Desktop
- Support for MCP Inspector for debugging
- Error handling and graceful degradation
- Type-safe implementations with comprehensive docstrings
- Environment variable support for API keys

Requirements:
-------------
- Python 3.10+
- EduChain library (>=0.3.10)
- MCP library with CLI support
- OpenAI API key (set via environment variables)

Usage:
------
    python mcp_server.py

Environment Variables:
----------------------
- OPENAI_API_KEY: Required for EduChain functionality
- Any other environment variables required by EduChain

Compatibility:
--------------
- Claude Desktop
- MCP Inspector
- Any MCP-compatible client

Author: Taksh Pal
Version: 0.1.0
License: MIT
"""

from typing import Any, Dict, Optional, Union
import logging
import os
from dotenv import load_dotenv
from educhain import Educhain
from mcp.server.fastmcp import FastMCP

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables (e.g., OpenAI API key)
load_dotenv()

# Validate required environment variables
if not os.getenv('OPENAI_API_KEY'):
    logger.warning("OPENAI_API_KEY not found in environment variables. "
                  "EduChain functionality may be limited.")

# Initialize EduChain client
# The client will automatically use environment variables for configuration
client = Educhain()
logger.info("EduChain client initialized successfully")

# Create MCP server instance with descriptive name
mcp = FastMCP("EduChain MCP")
logger.info("MCP server instance created")

@mcp.tool()
def generate_mcqs(topic: str, num_questions: int = 5) -> Dict[str, Any]:
    """
    Generate multiple-choice questions (MCQs) for a given educational topic.
    
    This function leverages EduChain's QnA engine to create well-structured
    multiple-choice questions with correct answers and plausible distractors.
    Each question includes four options with one correct answer.
    
    Args:
        topic (str): The educational topic or subject area for which to generate
            questions. Should be specific enough to generate focused questions.
            Examples: "Photosynthesis", "World War II", "Python Programming"
        num_questions (int, optional): The number of questions to generate.
            Defaults to 5. Must be between 1 and 20.
    
    Returns:
        Dict[str, Any]: A dictionary containing the generated questions and metadata.
            On success, includes:
            - questions: List of question objects with options and correct answers
            - topic: The input topic
            - count: Number of questions generated
            On error, includes:
            - error: Error message describing what went wrong
    
    Raises:
        ValueError: If num_questions is not in the valid range (1-20)
    
    Example:
        >>> generate_mcqs("Photosynthesis", 3)
        {
            "questions": [
                {
                    "question": "What is the primary purpose of photosynthesis?",
                    "options": ["A) ...", "B) ...", "C) ...", "D) ..."],
                    "correct_answer": "B"
                },
                ...
            ],
            "topic": "Photosynthesis",
            "count": 3
        }
    """
    # Validate input parameters
    if not isinstance(topic, str) or not topic.strip():
        return {"error": "Topic must be a non-empty string"}
    
    if not isinstance(num_questions, int) or not (1 <= num_questions <= 20):
        return {"error": "Number of questions must be an integer between 1 and 20"}
    
    try:
        logger.info(f"Generating {num_questions} MCQs for topic: {topic}")
        
        result = client.qna_engine.generate_questions(
            topic=topic.strip(),
            num=num_questions,
            question_type="Multiple Choice"
        )
        
        response_data = result.model_dump()
        logger.info(f"Successfully generated {num_questions} MCQs for topic: {topic}")
        
        return response_data
        
    except Exception as e:
        error_msg = f"Failed to generate MCQs for topic '{topic}': {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg}

@mcp.tool()
def lesson_plan(topic: str, duration: Optional[str] = None, grade_level: Optional[str] = None) -> Dict[str, Any]:
    """
    Generate a comprehensive, structured lesson plan for a given educational topic.
    
    This function creates a detailed lesson plan using EduChain's content engine,
    including learning objectives, materials needed, activities, and assessment methods.
    The lesson plan follows educational best practices and can be customized for
    different grade levels and durations.
    
    Args:
        topic (str): The subject, concept, or learning objective for the lesson.
            Should be specific and focused. Examples: "Introduction to Fractions",
            "The American Revolution", "Basic HTML Tags"
        duration (Optional[str]): The intended duration of the lesson.
            Examples: "45 minutes", "1 hour", "2 class periods". If not provided,
            a standard duration will be assumed.
        grade_level (Optional[str]): The target grade level or educational level.
            Examples: "Grade 5", "High School", "College Level", "Adult Education".
            If not provided, a general approach will be used.
    
    Returns:
        Dict[str, Any]: A comprehensive lesson plan dictionary containing:
            On success:
            - title: Lesson title
            - objectives: Learning objectives and goals
            - materials: Required materials and resources
            - activities: Structured learning activities
            - assessment: Methods for evaluating student learning
            - duration: Lesson duration
            - grade_level: Target grade level
            On error:
            - error: Detailed error message
    
    Example:
        >>> lesson_plan("Photosynthesis", "50 minutes", "Grade 7")
        {
            "title": "Understanding Photosynthesis",
            "objectives": ["Students will understand...", "Students will be able to..."],
            "materials": ["Textbook", "Microscope", "Plant samples"],
            "activities": [
                {
                    "name": "Introduction",
                    "duration": "10 minutes",
                    "description": "..."
                },
                ...
            ],
            "assessment": "Quiz on key concepts",
            "duration": "50 minutes",
            "grade_level": "Grade 7"
        }
    """
    # Validate input parameters
    if not isinstance(topic, str) or not topic.strip():
        return {"error": "Topic must be a non-empty string"}
    
    try:
        logger.info(f"Generating lesson plan for topic: {topic}")
        
        # Prepare the topic with additional context if provided
        enhanced_topic = topic.strip()
        if duration:
            enhanced_topic += f" (Duration: {duration})"
        if grade_level:
            enhanced_topic += f" (Grade Level: {grade_level})"
        
        result = client.content_engine.generate_lesson_plan(topic=enhanced_topic)
        
        response_data = result.model_dump()
        
        # Add metadata if provided
        if duration:
            response_data["duration"] = duration
        if grade_level:
            response_data["grade_level"] = grade_level
            
        logger.info(f"Successfully generated lesson plan for topic: {topic}")
        
        return response_data
        
    except Exception as e:
        error_msg = f"Failed to generate lesson plan for topic '{topic}': {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg}

@mcp.tool()
def generate_flashcards(topic: str, num_cards: int = 10, difficulty: Optional[str] = None) -> Dict[str, Any]:
    """
    Generate educational flashcards for effective study and memorization.
    
    This function creates a set of flashcards using EduChain's content engine,
    focusing on key concepts, definitions, and important facts related to the topic.
    Each flashcard contains a question/prompt on one side and a comprehensive
    answer on the other side, optimized for spaced repetition learning.
    
    Args:
        topic (str): The subject area, concept, or learning domain for which to
            create flashcards. Should be specific enough to generate focused content.
            Examples: "Spanish Vocabulary - Food", "Chemistry - Periodic Table",
            "History - World War I Events"
        num_cards (int, optional): The number of flashcards to generate.
            Defaults to 10. Must be between 1 and 50.
        difficulty (Optional[str]): The difficulty level for the flashcards.
            Options: "beginner", "intermediate", "advanced". If not provided,
            a mixed difficulty approach will be used.
    
    Returns:
        Dict[str, Any]: A dictionary containing the generated flashcards and metadata.
            On success:
            - flashcards: List of flashcard objects with front and back content
            - topic: The input topic
            - count: Number of flashcards generated
            - difficulty: Difficulty level (if specified)
            On error:
            - error: Detailed error message
    
    Raises:
        ValueError: If num_cards is not in the valid range (1-50)
    
    Example:
        >>> generate_flashcards("Spanish Vocabulary - Animals", 5, "beginner")
        {
            "flashcards": [
                {
                    "front": "What is the Spanish word for 'dog'?",
                    "back": "perro (masculine noun)"
                },
                {
                    "front": "Translate: 'The cat is sleeping'",
                    "back": "El gato está durmiendo"
                },
                ...
            ],
            "topic": "Spanish Vocabulary - Animals",
            "count": 5,
            "difficulty": "beginner"
        }
    """
    # Validate input parameters
    if not isinstance(topic, str) or not topic.strip():
        return {"error": "Topic must be a non-empty string"}
    
    if not isinstance(num_cards, int) or not (1 <= num_cards <= 50):
        return {"error": "Number of cards must be an integer between 1 and 50"}
    
    if difficulty and difficulty.lower() not in ["beginner", "intermediate", "advanced"]:
        return {"error": "Difficulty must be 'beginner', 'intermediate', or 'advanced'"}
    
    try:
        logger.info(f"Generating {num_cards} flashcards for topic: {topic}")
        
        # Prepare the topic with additional context if provided
        enhanced_topic = topic.strip()
        if difficulty:
            enhanced_topic += f" (Difficulty: {difficulty})"
        
        result = client.content_engine.generate_flashcards(
            topic=enhanced_topic,
            num=num_cards
        )
        
        response_data = result.model_dump()
        
        # Add metadata
        response_data["count"] = num_cards
        if difficulty:
            response_data["difficulty"] = difficulty
            
        logger.info(f"Successfully generated {num_cards} flashcards for topic: {topic}")
        
        return response_data
        
    except Exception as e:
        error_msg = f"Failed to generate flashcards for topic '{topic}': {str(e)}"
        logger.error(error_msg)
        return {"error": error_msg}

def main() -> None:
    """
    Main entry point for the EduChain MCP server.
    
    Initializes and starts the MCP server using stdio transport, which is
    compatible with Claude Desktop and other MCP clients. The server will
    continue running until interrupted or until the client disconnects.
    
    The server exposes three main tools:
    1. generate_mcqs: Creates multiple-choice questions
    2. lesson_plan: Generates structured lesson plans
    3. generate_flashcards: Creates educational flashcards
    
    Raises:
        KeyboardInterrupt: When the server is manually stopped
        Exception: For any other server initialization or runtime errors
    """
    try:
        logger.info("Starting EduChain MCP server...")
        logger.info("Server will use stdio transport for Claude Desktop compatibility")
        logger.info("Available tools: generate_mcqs, lesson_plan, generate_flashcards")
        
        # Start the MCP server using stdio (Claude Desktop compatible)
        mcp.run(transport="stdio")
        
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {str(e)}")
        raise
    finally:
        logger.info("EduChain MCP server shutdown complete")


if __name__ == "__main__":
    main()
