# 🛒 AI-Powered Shopping Automation System

A comprehensive shopping automation platform that intelligently fetches grocery lists from multiple sources, translates content using AI, and automates the entire shopping process on Instacart.

## 🚀 Overview

This system demonstrates advanced AI integration by combining multiple cutting-edge technologies:
- **Browser automation** for seamless web interactions
- **AI translation** for multilingual support
- **Task orchestration** for complex workflows
- **Data integration** from various sources

## 🛠️ Technology Stack

### Core Technologies
- **[Browser Use](https://cloud.browser-use.com/)** - AI-powered browser automation
- **[DeepL API](https://www.deepl.com/en/translator)** - Professional-grade translation services
- **[Dedalus Labs](https://www.dedaluslabs.ai/)** - AI agent orchestration platform
- **[Manus](https://manus.im/app)** - Task management and automation
- **[Vibe Kanban](https://www.vibekanban.com/docs)** - AI coding agent orchestration

### Integration Sources
- **Google Docs** - Document-based grocery lists
- **Notion** - Database-driven shopping lists
- **Instacart** - E-commerce automation target

## 📁 Project Structure

```
├── browser_shop.py              # Core browser automation engine
├── google_docs_shopping_final.py # Complete Google Docs integration
├── manus_final_system.py        # Manus API integration for Notion
├── translate_grocery_list.py    # Translation utilities
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
└── .gitignore                   # Security and cleanup rules
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Valid API keys for the services you plan to use
- Chrome browser (for automation)

### Installation
```bash
# Clone the repository
git clone <your-repo-url>
cd shop

# Install dependencies
pip install -r requirements.txt
```

### Usage Options

#### Option 1: Google Docs Integration
```bash
python google_docs_shopping_final.py
```

#### Option 2: Manus + Notion Integration
```bash
# Step 1: Fetch data from Notion via Manus
python manus_final_system.py

# Step 2: Run the shopping system
python google_docs_shopping_final.py
```

#### Option 3: Direct Browser Shopping
```bash
python browser_shop.py
```

## ⚙️ Configuration

### Required API Keys

Before running the system, update the following placeholder values:

| File | Placeholder | Service |
|------|-------------|---------|
| `browser_shop.py` | `YOUR_BROWSER_USE_API_KEY_HERE` | [Browser Use](https://cloud.browser-use.com/) |
| `translate_grocery_list.py` | `YOUR_DEEPL_API_KEY_HERE` | [DeepL API](https://www.deepl.com/en/translator) |
| `manus_final_system.py` | `YOUR_MANUS_API_KEY_HERE` | [Manus](https://manus.im/app) |
| `google_docs_shopping_final.py` | `YOUR_GOOGLE_DOCS_URL_HERE` | Google Docs URL |

### Additional Configuration (Manus + Notion)
- `your_notion_database_id` - Your Notion database ID
- `your_notion_integration_token` - Your Notion integration token

## 🔒 Security

⚠️ **Important Security Notes:**
- This repository contains placeholder API keys for security
- Replace all placeholder values with your actual credentials
- Never commit real API keys to version control
- Consider using environment variables for production deployments
- Review the `.gitignore` file for additional security measures

## ✨ Features

### Core Capabilities
- 🔄 **Multi-source Integration** - Fetch from Google Docs, Notion, or local files
- 🌐 **AI Translation** - Automatic Spanish-to-English translation with quantity preservation
- 🤖 **Intelligent Automation** - AI-powered browser automation for Instacart
- 📊 **Data Processing** - Smart extraction of items with quantities and measurements
- 🔧 **Error Handling** - Comprehensive error handling and fallback mechanisms

### Advanced Features
- 🎯 **Price Optimization** - AI-assisted product selection and price comparison
- 🛒 **Cart Management** - Automatic item addition and cart management
- 💳 **Checkout Automation** - Complete checkout process including payment setup
- 📝 **Logging & Monitoring** - Detailed logging for debugging and monitoring
- 🔄 **Unicode Support** - Full Unicode support for international content

## 🏗️ Architecture

The system follows a modular architecture with clear separation of concerns:

1. **Data Layer** - Handles data fetching from various sources
2. **Translation Layer** - Manages language detection and translation
3. **Automation Layer** - Controls browser automation and shopping logic
4. **Integration Layer** - Manages API integrations and task orchestration

## 🤝 Contributing

We welcome contributions! Please ensure:
- Code follows Python best practices
- All API keys are properly secured
- Tests are included for new features
- Documentation is updated accordingly

## 📄 License

This project is open source. Please review the license terms before use.

## 🆘 Support

For issues and questions:
1. Check the documentation for each integrated service
2. Review the error logs for debugging information
3. Ensure all API keys are correctly configured
4. Verify network connectivity and service availability

---

**Built with ❤️ using cutting-edge AI technologies**
