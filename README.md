# pension-and-finance-planner

pension-and-finance-planner is a webbased pension- and finance-planner which takes taxquestions, wealth-management and other important parts into account.

## Package-Installation
For installing all packages use a virtual environemtent to install all packages of 'requirements.txt'

For Windows:
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

For macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
Starting server:
```python
uvicorn main:app --reload
```