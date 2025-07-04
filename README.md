# EduChain MCP Server

A Model Context Protocol (MCP) server that integrates [EduChain](https://github.com/satvik314/educhain)'s educational content generation capabilities with Claude Desktop and other MCP-compatible clients.

## 🎯 Overview

The EduChain MCP Server provides three powerful educational tools accessible through Claude Desktop:

- **📝 Multiple Choice Questions (MCQs)**: Generate well-structured questions with plausible distractors
- **📚 Lesson Plans**: Create comprehensive, structured lesson plans with objectives, activities, and assessments
- **🗂️ Flashcards**: Generate educational flashcards optimized for spaced repetition learning

## 🚀 Features

- **Claude Desktop Integration**: Seamless integration with Claude Desktop via MCP protocol
- **Type-Safe Implementation**: Full type hints and comprehensive docstrings
- **Error Handling**: Robust error handling and graceful degradation
- **Logging**: Comprehensive logging for debugging and monitoring
- **Input Validation**: Thorough validation of all input parameters
- **Environment Configuration**: Support for environment variables
- **MCP Inspector Compatible**: Works with MCP Inspector for debugging

## 📋 Requirements

- Python 3.10 or higher
- OpenAI API key (for EduChain functionality)
- Claude Desktop (for MCP integration)

## 🔧 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/educhain-mcp.git
   cd educhain-mcp
   ```

2. **Install dependencies:**
   ```bash
   pip install -e .
   ```
   
   Or install manually:
   ```bash
   pip install educhain>=0.3.10 httpx>=0.28.1 "mcp[cli]>=1.10.1" python-dotenv
   ```

3. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## 🏃 Usage

### Running the Server

```bash
python mcp_server.py
```

The server will start and listen for MCP connections via stdio transport, making it compatible with Claude Desktop.

### Claude Desktop Configuration

Add the following to your Claude Desktop configuration file:

**Windows:** `%APPDATA%\Claude\claude_desktop_config.json`
**macOS:** `~/Library/Application Support/Claude/claude_desktop_config.json`
**Linux:** `~/.config/claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "weather": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/PARENT/FOLDER/weather",
        "run",
        "weather.py"
      ]
    }
  }
}
```

### MCP Inspector

For debugging and development, you can use the MCP Inspector:

```bash
npx @modelcontextprotocol/inspector python mcp_server.py
```

## 🛠️ Available Tools

### 1. Generate MCQs

**Function:** `generate_mcqs(topic: str, num_questions: int = 5)`

**Description:** Generate multiple-choice questions for a given educational topic.

**Parameters:**
- `topic` (str): The educational topic (e.g., "Photosynthesis", "World War II")
- `num_questions` (int, optional): Number of questions to generate (1-20, default: 5)

**Example:**
```python
result = generate_mcqs("Photosynthesis", 3)
```

### 2. Lesson Plan

**Function:** `lesson_plan(topic: str, duration: Optional[str] = None, grade_level: Optional[str] = None)`

**Description:** Generate a comprehensive, structured lesson plan.

**Parameters:**
- `topic` (str): The lesson topic (e.g., "Introduction to Fractions")
- `duration` (str, optional): Lesson duration (e.g., "45 minutes", "1 hour")
- `grade_level` (str, optional): Target grade level (e.g., "Grade 5", "High School")

**Example:**
```python
result = lesson_plan("Photosynthesis", "50 minutes", "Grade 7")
```

### 3. Generate Flashcards

**Function:** `generate_flashcards(topic: str, num_cards: int = 10, difficulty: Optional[str] = None)`

**Description:** Generate educational flashcards for study and memorization.

**Parameters:**
- `topic` (str): The subject area (e.g., "Spanish Vocabulary - Animals")
- `num_cards` (int, optional): Number of flashcards to generate (1-50, default: 10)
- `difficulty` (str, optional): Difficulty level ("beginner", "intermediate", "advanced")

**Example:**
```python
result = generate_flashcards("Spanish Vocabulary - Animals", 5, "beginner")
```

## 📝 Project Structure

```
educhain-mcp/
├── mcp_server.py          # Main MCP server implementation
├── main.py                # Simple entry point (not used for MCP)
├── pyproject.toml         # Project configuration and dependencies
├── README.md              # This documentation
└── .env                   # Environment variables (create this)
```

## 🔍 Logging

The server includes comprehensive logging to help with debugging and monitoring:

- **INFO Level**: Server startup, tool execution, and success messages
- **WARNING Level**: Missing environment variables and non-critical issues
- **ERROR Level**: Tool execution failures and server errors

Logs are formatted with timestamps and include the module name for easy identification.

## 🛡️ Error Handling

The server implements robust error handling:

- **Input Validation**: All parameters are validated before processing
- **Graceful Degradation**: Errors are returned as structured responses
- **Logging**: All errors are logged with detailed messages
- **Type Safety**: Full type hints prevent common runtime errors

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🙏 Acknowledgments

- [EduChain](https://github.com/satvik314/educhain) for the educational content generation capabilities
- [Model Context Protocol](https://modelcontextprotocol.io/) for the integration framework
- [Claude Desktop](https://claude.ai/) for the AI assistant platform

## 📧 Support

For issues, questions, or contributions, please:

1. Check the [Issues](https://github.com/yourusername/educhain-mcp/issues) page
2. Create a new issue if your problem isn't already listed
3. Provide detailed information about your environment and the issue

## 🔄 Changelog

### v0.1.0
- Initial release
- Basic MCP server implementation
- Three educational tools: MCQs, lesson plans, flashcards
- Claude Desktop integration
- Comprehensive documentation and error handling
