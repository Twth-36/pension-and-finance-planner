# pension-and-finance-planner

pension-and-finance-planner takes taxquestions, wealth-management and other important parts into account for successfully plan ones retirement or generar financial decisions. In a first approach it is limited to the canton of Bern.

## Package-Installation
For installing all packages use a virtual environemtent to install all packages of 'requirements.txt'

For Windows:
```bash
python -m venv plannerVenv
plannerVenv\Scripts\activate
pip install -r requirements.txt
```

For macOS/Linux:
```bash
python3 -m venv plannerVenv
source plannerVenv/bin/activate
pip install -r requirements.txt
```
Starting app (after plannerVenv activated):
```python
python main.py
```