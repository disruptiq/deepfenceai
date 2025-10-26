# DeepFence AI

A sophisticated AI-powered cybersecurity analysis system that orchestrates multiple specialized agents to perform comprehensive security assessments and generate detailed reports.

## 🚀 Features

- **Multi-Agent Architecture**: Utilizes specialized mapper, organizer, and reporter agents
- **Automated Repository Management**: Automatically clones and updates agent repositories
- **Comprehensive Analysis**: Performs static analysis, dependency mapping, and security assessments
- **Beautiful Visual Feedback**: Colorful ASCII art progression indicators
- **Modular Design**: Clean separation of concerns with organized source code structure
- **Automated Reporting**: Generates detailed security reports and findings

## 📁 Project Structure

```
deepfenceai/
├── src/                    # Source code directory
│   └── ascii_art.py       # ASCII art and terminal styling utilities
├── agents/                # Cloned agent repositories (auto-generated)
├── outputs/               # Analysis results and reports (auto-generated)
├── archive/               # Previous session archives (auto-generated)
├── config.json            # Agent configuration
├── main.py               # Main orchestration script
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- Git
- Internet connection (for cloning agent repositories)

### Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/disruptiq/deepfenceai.git
   cd deepfenceai
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure agents (optional):**
   Edit `config.json` to customize agent repositories and settings.

## 📖 Usage

### Basic Usage

```bash
python main.py <target-path>
```

**Parameters:**
- `target-path`: Path to the codebase or project directory to analyze

### Example

```bash
# Analyze the current directory
python main.py .

# Analyze a specific project
python main.py /path/to/your/project
```

### Visual Output

The system provides beautiful visual feedback throughout execution:
- 🎨 **Colorful ASCII art** for each processing stage
- 📊 **Progress indicators** with stage-specific colors
- ✅ **Success/failure messages** with appropriate coloring
- 📁 **File collection status** for each agent

## ⚙️ Configuration

### Agent Configuration

The `config.json` file defines the agents used in the analysis:

```json
{
  "mapper_agents": [
    {
      "name": "mapper-agent",
      "repo": "https://github.com/disruptiq/mapper-agent"
    }
  ],
  "organizer_agents": [
    {
      "type": "static-organizer-agent",
      "name": "static-organizer-agent",
      "repo": "https://github.com/disruptiq/static-organizer-agent"
    }
  ],
  "reporter_agent": {
    "name": "reporter",
    "repo": "https://github.com/disruptiq/reporter-agent"
  }
}
```

## 🏗️ Architecture

### Agent Types

1. **Mapper Agents**: Extract and map data from the target codebase
   - Network mapping
   - Database schema analysis
   - API specification extraction
   - Dependency analysis

2. **Organizer Agents**: Process and structure the mapped data
   - Static analysis
   - Code quality assessment
   - Security vulnerability detection

3. **Reporter Agent**: Generate comprehensive reports
   - Aggregates findings from all agents
   - Creates HTML reports with security insights
   - Provides executive summaries

### Data Flow

1. **Input**: Target codebase path
2. **Mapping**: Extract structured data from codebase
3. **Organization**: Analyze and categorize findings
4. **Reporting**: Generate comprehensive security reports
5. **Output**: HTML reports and structured findings

## 📊 Output Structure

Results are organized in the `outputs/` directory:

```
outputs/
├── mapper-agent/          # Raw mapped data
├── static-organizer-agent/# Processed analysis results
└── reporter_report.html   # Final comprehensive report
```

Previous sessions are automatically archived in `archive/output-XXXXX/`.

## 🔧 Development

### Adding New Agents

1. Create agent repository with required interface
2. Update `config.json` with agent details
3. Ensure agent accepts command-line parameters as needed

### Modifying ASCII Art

ASCII art configurations are in `src/ascii_art.py`. Add new stages or modify existing art there.

### Code Style

- Follow PEP 8 guidelines
- Use type hints where appropriate
- Maintain modular structure

## 📋 Requirements

- Python 3.8+
- colorama>=0.4.6
- Git
- Various analysis tools (installed automatically by agents)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

**"colorama not installed"**
- The system will automatically install colorama if missing

**"Repository not found"**
- Check internet connection and repository URLs in config.json

**"Permission denied"**
- Ensure write permissions for output directories

**Unicode display issues**
- The ASCII art uses standard characters and should display correctly in most terminals

### Getting Help

- Check the issues page for known problems
- Create a new issue for bugs or feature requests

---

*Built with ❤️ for comprehensive cybersecurity analysis*
