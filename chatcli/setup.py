from setuptools import setup, find_packages

setup(
    name="chatcli",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
    "click>=8.1.0",
    "openai>=1.0.0",
    "python-dotenv>=1.0.0",
    "rich>=13.0.0",
    "textual>=0.35.0",
    "prompt_toolkit>=3.0.0",
],
    entry_points="""
        [console_scripts]
            chatcli=chatcli.main:cli
    """,
    python_requires=">=3.8",
    author="David",
    author_email="david.hoover@vetsfirstdme.com",
    description="An interactive CLI chat application that uses OpenAI models to provide intelligent responses",
    keywords="openai,ai,cli",
    url="https://github.com/doover17/ChatCLI.git",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
