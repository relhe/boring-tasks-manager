# Boring Tasks Manager

Welcome to the **Boring Tasks manager** repository! This project provides a collection of Python scripts that help automate repetitive, time-consuming tasks, so you can save time and focus on more meaningful work. Whether it's renaming files, organizing directories, managing data, or sending automated emails, this project has you covered.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Examples](#examples)
- [Contributing](#contributing)
- [License](#license)

## Features

- **File Management** : Automatically rename, move, or organize files in directories.
- **Email Automation** : Send emails or reminders with a few lines of code.
- **Web Scraping** : Extract and process data from websites.
- **Custom Scripts** : Easily add custom scripts to extend functionality.

Each script is modular and can be used independently or as part of a larger workflow.

## Installation

1. **Clone the repository** :

   ```
   git clone https://github.com/relhe/boring-tasks-manager.git
   cd boring-tasks-manager
   ```
2. **Install dependencies** :

   ```
   pip install -r requirements.txt
   ```

## Usage

Each script is standalone, meaning you can run each one individually to perform a specific task. Some examples of available scripts:

- **File Organizer** : `python file_organizer.py --path <directory>`
- **Email Automation** : `python email_automation.py --recipient <email> --subject <subject> --body <message>`
- **Web Scraper** : `python web_scraper.py --url <website_url>`

### Run a File Renaming Script

Each script in this repository can be executed directly from the command line. Follow the instructions below based on your operating system:

#### macOS & Linux

1. **Open the terminal** .
2. **Navigate to the project directory** :

   ```
   cd /path/to/boring-tasks-manager
   ```
3. **Run the desired script** :

   ```
   python3 <script_name>.py [arguments]
   ```

Example:

```
python3 rename_files.py --directory "/path/to/directory" --replace "oldword" --new "newword"
```

#### Windows

1. **Open Command Prompt or PowerShell** .
2. **Navigate to the project directory** :

   ```
   cd C:\path\to\boring-tasks-manager
   ```
3. **Run the desired script** :

```
python <script_name>.py [arguments]
```

Example :

```
python rename_files.py --directory "C:\path\to\directory" --replace "oldword" --new "newword"

```

_Tip_ : Ensure Python is added to your PATH. You can check by running `python --version` in the command prompt.

### Sending Automated Emails

Send automated emails

```
python email_automation.py --recipient "example@example.com" --subject "Reminder" --body "Don't forget our meeting tomorrow!"
```

### Web scraping for data

Extract product prices from an e-commerce site and save them to a CSV file.

```
python web_scraper.py --url "https://example.com/products"
```

## Contributing

Contributions are welcome! Here’s how you can help:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes.
4. Open a pull request with a description of your changes.

## Suggestions

Feel free to open an issue if you have ideas for more tasks that could be automated or if you find any bugs.

## License

This project is licensed under the MIT License. See the [LICENSE]() file for details.
