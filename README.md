# IvaLineX

A Python project code tracker application built with PyQt6.  
IvaLineX allows you to count Python code lines in selected folders, store results per project, and visualize progress over time.

## Features

- Count Python code lines directly from a selected folder.
- Create and manage projects with stored paths for consistent counting.
- Save results per project per date to track code evolution.
- Visualize progress in an interactive graph showing code, empty lines, and comments.
- Control which files to include (.py, __init__, .venv, README, JSON, etc.).
- Configure counting options such as saving history, counting empty lines and comments.
- Reset settings if needed.
- Simple and scalable PyQt6 interface, designed for learning and experimentation.

## Installation

(Tested on macOS, IDE: PyCharm)

- Clone the repository:
```bash
  git clone https://github.com/Jin-Mach/IvaLineX.git
```

- Navigate to the project directory:
```bash
  cd IvaLineX
```

- Create a virtual environment:
  - On Windows:
```bash
  python -m venv .venv
```
  - On macOS/Linux:
```bash
  python3 -m venv .venv
```

- Activate the virtual environment:
  - On Windows (Command Prompt):
```bash
  .venv\Scripts\activate
```
  - On Windows (PowerShell):
```bash
  .venv\Scripts\activate.ps1
```
  - On macOS/Linux:
```bash
  source .venv/bin/activate
```

- Install the required packages:
  - On Windows:
```bash
  python -m pip install -r requirements.txt
```
  - On macOS/Linux:
```bash
  python3 -m pip install -r requirements.txt
```
  - (Optional) for development and testing:
    - On Windows:
```bash
  python -m pip install -r dev_requirements.txt
```
    - On macOS/Linux:
```bash
  python3 -m pip install -r dev_requirements.txt
```

## Usage

After installing the dependencies, you can start the application with the following command:

- Run the application:
  - On Windows:
```bash
  python iva_line.py
```
  - On macOS/Linux:
```bash
  python3 iva_line.py
```

## License

- This project is licensed under the MIT License.

## Credits

- Developed by [Jin-Mach](https://github.com/Jin-Mach).

## Contact

- Questions or feedback? Reach out via GitHub: [Jin-Mach](https://github.com/Jin-Mach).