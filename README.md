# Bit2Me CLI Utilities

## Introduction
Bit2Me CLI Utilities is a command-line interface tool designed to interact with the Bit2Me cryptocurrency platform's API. It provides a convenient way to access and manage Bit2Me services directly from your terminal.

## Getting Started
Before using the Bit2Me CLI Utilities, you'll need to:
1. Have Python installed on your system
2. Obtain your Bit2Me API credentials (API key and secret)
3. Set up your environment configuration

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/bit2me-cli-utilities.git
cd bit2me-cli-utilities
```

2. Set up your environment:
   - Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
   - Edit the `.env` file with your Bit2Me API credentials:
   ```
   BIT2ME_API_BASE_URL=your_api_base_url
   BIT2ME_API_KEY=your_api_key
   BIT2ME_API_SECRET=your_api_secret
   ```

3. Install dependencies:
```bash
pip install .
```

## Usage
The CLI provides various commands to interact with the Bit2Me platform. Here are some examples:

### Global Summary
View your Bit2Me account's financial summary, including total deposits, withdrawals, current value, and net revenue:

```bash
# View global summary
cli global-summary show
```

This will display a formatted summary of your account's financial status in EUR.

### General Commands
```bash
# View all available commands
cli --help

# Get help for a specific command group
cli global-summary --help
```

For detailed documentation on other available commands and their usage, please refer to the CLI help menu.



## Development

To set up the development environment:

1. Install development dependencies:
```bash
uv sync
source .venv/bin/activate
```

2. Install pre-commit hooks:
```bash
task lint
```

3. Run tests:
```bash
python -m pytest
```