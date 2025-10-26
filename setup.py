#!/usr/bin/env python3
"""
Setup script for AI Shopping Automation System
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="ai-shopping-automation",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="AI-powered shopping automation system with multi-source integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-username/ai-shopping-automation",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
        "Topic :: Office/Business :: Scheduling",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
        ],
    },
    entry_points={
        "console_scripts": [
            "ai-shopping=google_docs_shopping_final:main",
            "browser-shop=browser_shop:main",
            "manus-fetch=manus_final_system:main",
        ],
    },
    keywords="ai automation shopping browser translation deepl notion google-docs",
    project_urls={
        "Bug Reports": "https://github.com/your-username/ai-shopping-automation/issues",
        "Source": "https://github.com/your-username/ai-shopping-automation",
        "Documentation": "https://github.com/your-username/ai-shopping-automation#readme",
    },
)
