<h1>Cardano-cli Wrapper for interacting with Cardano Plutus Scripts</h1>
Made as part of Plutus Pioneer program Capstone
<br><br>


<h2>Prerequisites</h2>
Python version 3.6 or above<br>
Cardano-node 1.29.0 running with Testnet Magic = 1097911063

<br><br>

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
uvicorn app:app --host 0.0.0.0 --port 80
```
<br>

4. Open browser and navigate to localhost <br><br>
   ![image](https://user-images.githubusercontent.com/56497189/135043259-94d504fa-5326-4789-94da-b233ff5aaae3.png)

<br>

5. Create payment keys and address with Option 1
<br>

6. Fund this given address with your test_ada<br>
   You can do this via the testnet faucet or your own tesnet wallet<br>
   <strong> DO NOT SEND IT REAL ADA </strong>
<br>

7. Select Option 2 to check if the address has recieved your tAda<br>
   Once you see a new UTxO, proceed further <br><br>
   ![image](https://user-images.githubusercontent.com/56497189/135046239-94f3f834-5711-4f6c-8452-319c2b00416f.png)
   
<br>

8. Move to option 3 to create a tx to the script address with a new UTxO<br>
   Upload the compiled Plutus script, its address will be built internally. <br><br>
   ![image](https://user-images.githubusercontent.com/56497189/135046821-676d56f5-b1d0-4b4b-a39d-37d3dc603c3a.png)
   
<br>

9. Check UTxO balance with Option 2 for confirmation of transaction  <br><br>
   ![image](https://user-images.githubusercontent.com/56497189/135047035-3c104f0e-8a41-4a9e-8c08-e7cd3a3612f6.png)
<br>

10. Option 4 can be used to redeem the funded script UTxO <br><br>
   ![image](https://user-images.githubusercontent.com/56497189/135047347-d0e0f4ae-c92a-489e-a837-8ae6fc25ffe2.png)
<br>
 11. You will recieve your unlocked funds. <br><br>
   ![image](https://user-images.githubusercontent.com/56497189/135047554-ecf39fc7-5d56-4581-96b0-3fc4fbb878de.png)
<br>

