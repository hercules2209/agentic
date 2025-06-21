# Agentic 🤖

A powerful AI-powered coding assistant that can autonomously read, write, execute, and debug code within a sandboxed environment. Built with Google Gemini API and designed for iterative problem-solving.

## 🚀 Features

- **Autonomous Code Analysis**: Intelligently explores codebases and understands project structure
- **Bug Detection & Fixing**: Identifies and resolves coding issues through systematic debugging
- **Feature Development**: Adds new functionality to existing projects
- **Code Execution**: Runs Python files with full output capture and error handling
- **Sandboxed Environment**: Secure file operations restricted to specified working directory
- **Iterative Problem Solving**: Multi-turn conversations with configurable iteration limits
- **Comprehensive Logging**: Detailed execution traces with optional verbose mode

## 🛠️ Architecture

The agent operates through four core tools:
- `get_files_info()` - Directory exploration and file discovery
- `get_file_content()` - Complete file reading with truncation handling
- `run_python_file()` - Python execution with timeout and output capture
- `write_file()` - Complete file writing/overwriting with directory creation

## 📋 Requirements

- Python 3.12+
- Google Gemini API key
- UV package manager (recommended)

## ⚡ Quick Start

1. **Clone and Setup**
   ```bash
   git clone https://github.com/hercules2209/agentic.git
   cd agentic
   
   # Using UV (recommended)
   uv sync
   
   # Or using pip
   pip install -r requirements.txt
   ```
2. **Configure Environment**
   ```bash
   # Create .env file
   echo "GEMINI_API_KEY=your_api_key_here" > .env
   ```

3. **Configure Settings** (config.py)
   ```python
   MODEL_NAME = "gemini-2.0-flash-001"  # or "gemini-2.5-pro" for better performance
   WORKING_DIR = "./calculator"  # Your target project directory
   MAX_ITERS = 20  # Maximum agent iterations
   ```

4. **Run the Agent**
   ```bash
   uv run main.py "fix the calculator precedence bug" --verbose
   ```

## 🎯 Use Cases & Examples

### Bug Fixing
```bash
uv run main.py "fix the bug: 3 + 7 * 2 shouldn't be 20"
```
*The agent will explore the codebase, identify the precedence issue in the calculator logic, and implement the correct fix.*

### Feature Development
```bash
uv run main.py "add exponent functionality using ^ symbol to the calculator"
```
*The agent will analyze the existing calculator structure and seamlessly integrate new power operation support.*

### Code Analysis
```bash
uv run main.py "explain how the render function works and optimize it"
```
*The agent will examine the code, provide detailed explanations, and suggest improvements.*

## 🏗️ Project Structure

```
agentic/
├── main.py              # Entry point and agent orchestration
├── config.py            # Configuration settings
├── prompts.py           # System prompt definitions
├── functions/           # Tool implementations
│   ├── get_file_content.py
│   ├── get_files_info.py
│   ├── run_python_file.py
│   └── write_file.py
├── calculator/          # Example project for testing
└── requirements.txt
```

## 🔧 Configuration

### Model Selection
- **gemini-2.0-flash-001**: Faster, cost-effective, may require multiple attempts
- **gemini-2.5-pro**: Higher accuracy, better first-attempt success rate
- **Any other Google Gemini model**: Configure in `config.py` as `MODEL_NAME`

### Working Directory
Set `WORKING_DIR` in `config.py` to any project you want the agent to work on. The agent is sandboxed to this directory for security. The included `calculator/` directory serves as an example project for testing the agent's capabilities.

### System Prompt
Customize the agent's behavior by modifying the system prompt in `prompts.py`.

### Max Agent iterations
During some complex tasks you might need to increase maximum number of iterations you can do so by modifying `MAX_ITERS` in `config.py`

## 🧠 How It Works

1. **Exploration Phase**: Agent surveys the project structure using `get_files_info()`
2. **Analysis Phase**: Reads relevant files with `get_file_content()` to understand the codebase
3. **Execution Phase**: Tests current functionality using `run_python_file()`
4. **Solution Phase**: Implements fixes/features using `write_file()`
5. **Validation Phase**: Verifies changes by re-running the code
6. **Iteration**: Repeats until task completion or max iterations reached

## 🚀 Future Roadmap

- [ ] **Enhanced Tool Capabilities** - File operations, debugging tools, package management
- [ ] **Conversational Interface** - Multi-turn conversations for complex tasks
- [ ] **Git Integration** - Version control and rollback capabilities
- [ ] **Multi-LLM Support** - OpenAI, Anthropic, and local model integration
- [ ] **Language Expansion** - Support for JavaScript, Go, Rust, and more
- [ ] **Terminal UI** - Rich interactive interface using Textual
- [ ] **Collaborative Features** - Multi-agent coordination for complex projects

## 📊 Performance Notes

- **Context Window**: Limited by the selected model's context capacity
- **File Size Limit**: 10,000 characters per file (with truncation handling)
- **Execution Timeout**: 30 seconds per Python file execution
- **Iteration Limit**: Configurable maximum to prevent infinite loops

## 🤝 Contributing

Contributions are welcome! This project is open for:
- Tool enhancement and new tool development
- UI/UX improvements
- Multi-language support
- Performance optimizations
- Documentation improvements

## 📄 License

GNU GPL v3 License - see LICENSE file for details.

## 👨‍🎓 About

Developed by Harshaditya Sharma, a Computer Science student specializing in Artificial Intelligence and Machine Learning. This project demonstrates practical applications of LLM agents in software development automation.

---

*Built with ❤️ using Google Gemini API and modern Python trolling*
