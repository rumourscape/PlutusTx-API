<h1>Cardano-cli Wrapper for interacting with Cardano Plutus Scripts</h1>
Made as part of Plutus Pioneer program Capstone
<br><br>


<h2>Prerequisites</h2>
Python version 3.6 or above<br>
Cardano-node 1.29.0 running with Testnet Magic = 1097911063

<br>

<h2> Instructions </h2>

1. Clone this Github repo and navigate to the directory.
<br>

2. Install the python dependencies
```python
pip install -r requirements.txt
```
<br>

3. Run the local awsgi server
```python
uvicorn main:app --host 0.0.0.0 --port 80
```
<br>

4. Open browser and navigate to localhost
