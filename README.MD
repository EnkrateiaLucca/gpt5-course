# O'Reilly Live Training - Getting Started with GPT-5

## Course Overview

This repository contains materials for the O'Reilly Live Training on GPT-5. You'll learn about the latest advancements in language models, practical implementation strategies, and hands-on experience with their new cutting edge model.

## Setup

### Prerequisites
- Python 3.11 or higher
- OpenAI API access
- Basic understanding of Python and machine learning concepts

### Installation Options

**Option 1: Using Conda (Recommended)**

1. Install [Anaconda](https://www.anaconda.com/download)
2. Create a new environment:
   ```bash
   conda create -n oreilly-gpt5 python=3.11
   ```
3. Activate the environment:
   ```bash
   conda activate oreilly-gpt5
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

**Option 2: Using pip with venv**

1. **Create a Virtual Environment:**
   Navigate to your project directory and create a virtual environment:
   ```bash
   python -m venv oreilly-gpt5
   ```

2. **Activate the Virtual Environment:**
   - **On Windows:**
     ```bash
     .\oreilly-gpt5\Scripts\activate
     ```
   - **On macOS and Linux:**
     ```bash
     source oreilly-gpt5/bin/activate
     ```

3. **Install Dependencies:**
   ```bash
   pip install python-dotenv
   pip install -r requirements.txt
   ```

4. **Deactivate when done:**
   ```bash
   deactivate
   ```

## Configuration

### Setting up API Keys

1. Copy the `.env.example` file to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Add your OpenAI API key to the `.env` file:
   ```
   OPENAI_API_KEY=<your_openai_api_key_here>
   ```

3. Get your API key from [OpenAI Platform](https://platform.openai.com/)

## Using with Jupyter Notebooks

To use this environment with Jupyter notebooks:

**For Conda users:**
```bash
conda install jupyter -y
python -m ipykernel install --user --name=oreilly-gpt5
```

**For pip users:**
```bash
pip install jupyter
python -m ipykernel install --user --name=oreilly-gpt5
```

## Course Content

### Notebooks

The course materials are organized in the `notebooks/` folder:

- `1.0-intro-gpt5.ipynb`: intro to gpt-5 and usage of basic parameters and examples.
- `2.0-gpt5-params.ipynb`: deep dive into newest features that come with gpt-5 model
- `3.0-gpt5-prompting-guide.ipynb`: deep dive into prompting best practices with gpt-5
- `4.0-gpt5-frontend-dev-experiments.ipynb`: fun experiment with building a web app maker app with gpt5 

## Quick Start

1. Complete the setup instructions above
2. Activate your environment
3. Launch Jupyter:
   ```bash
   jupyter notebook
   ```
4. Open the first notebook to begin

## Troubleshooting

### Common Issues

- **API Key errors**: Ensure your `.env` file is properly configured with a valid OpenAI API key
- **Import errors**: Make sure all dependencies are installed with `pip install -r requirements/requirements.txt`
- **Python version issues**: This course requires Python 3.11 or higher

## Support

For questions or issues related to the course materials, please:
- Check the troubleshooting section above
- Review the course discussion forum
- Contact the course instructor during live sessions


## Acknowledgments

Special thanks to O'Reilly Media for hosting this training and to all participants for joining this journey into next-generation AI technologies.