from typing import Text
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import HTMLResponse, FileResponse, RedirectResponse
import subprocess
import shutil
import os
import io

ALLOWED_EXTENSIONS = {'plutus'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app = FastAPI()

@app.on_event("startup")
def startup():
    os.system("export MAGIC=1097911063")

@app.get('/', response_class=HTMLResponse)
def index():
    return FileResponse('static/index.html')

@app.get('/newscript')
def newscript_html():
    return FileResponse('static/newscript.html')

@app.get('/api/newkeys')
def create_keys():
    if os.path.isfile('payment.skey'): return "Keys already exist. Proceed to next steps."

    key_gen="cardano-cli address key-gen --normal-key --verification-key-file payment.vkey --signing-key-file payment.skey"

    out=subprocess.run([key_gen], shell= True, text= True, stdout = subprocess.PIPE)

    addr_gen=f"cardano-cli address build --payment-verification-key-file payment.vkey --out-file payment.addr --testnet-magic $MAGIC"
    subprocess.run([addr_gen], shell= True, text= True ,stdout = subprocess.PIPE)
    addr=subprocess.run(["cat payment.addr"], shell= True, text= True ,stdout = subprocess.PIPE).stdout.strip()
    html_content= f'''
    <!DOCTYPE html>
<html>

<head>
    <title>New keys</title>
</head>

<body style="font-family: 'Segoe UI', Verdana, sans-serif;">
    Keys created for the test_address: {addr} <br>
    Fund this address with test-ada to procceed further.
</body>

</html>
    '''

    if not out.stdout:
        return HTMLResponse(content=html_content, status_code=200)
    else: return("Error Occurred.")

@app.get('/api/checkbal')
def check_bal():
    if os.path.isfile('payment.addr'):
        query="cardano-cli query utxo --address $(cat payment.addr) --testnet-magic $MAGIC"
        out=subprocess.Popen([query], shell= True, stdout = subprocess.PIPE)
        html=''
        for line in io.TextIOWrapper(out.stdout, encoding="utf-8"):
            html = html+ line+ "<br>"
            
        html_content= f'''
                    <!DOCTYPE html>
                <html>

                <head>
                    <title>New keys</title>
                </head>

                <body style="font-family: 'Segoe UI', Verdana, sans-serif;">
                    <h2>Address UTxO: </h2><br>
                    <h3> {html} </h3>
                </body>

                </html>
                    '''
        return HTMLResponse(content=html_content, status_code=200)

@app.post('/api/newscript')
def newscript(
    utxo:str = Form(...),
    tada:int = Form(...),
    datum:str = Form(...),
    script: UploadFile= File(...)
                ):
    
    if allowed_file(script.filename):
        file_location = f"{script.filename}"
        with open(file_location, "wb+") as file_object:
            shutil.copyfileobj(script.file, file_object)
    else: return "Invalid Filetype. Upload .plutus script."

    hasher=f"cardano-cli transaction hash-script-data --script-data-value {datum}"
    datumhash=subprocess.run([hasher], shell= True, text= True, stdout = subprocess.PIPE).stdout.strip()
    if not datumhash: return "Error"

    scr=f"cardano-cli address build --payment-script-file {script.filename} --testnet-magic $MAGIC --out-file script.addr"
    script_addr=subprocess.run([scr], shell= True, text= True, stdout = subprocess.PIPE).stdout

    if script_addr: return "Error"

    builder= f" cardano-cli transaction build --alonzo-era --tx-in {utxo} --tx-out $(cat script.addr)+{str(tada*1000000)} --tx-out-datum-hash {datumhash} --change-address $(cat payment.addr) --protocol-params-file protocol.json --out-file tx.raw --testnet-magic $MAGIC"
    build=subprocess.run([builder], shell= True, text= True, stdout = subprocess.PIPE).stdout.strip()
    
    signer=f"cardano-cli transaction sign --tx-body-file tx.raw --testnet-magic $MAGIC --signing-key-file payment.skey --out-file tx.sign"
    sign=subprocess.run([signer], shell= True, text= True, stdout = subprocess.PIPE).stdout.strip()
    
    submission=f"cardano-cli transaction submit --tx-file tx.sign --testnet-magic $MAGIC"
    submit=subprocess.run([submission], shell= True, text= True, stdout = subprocess.PIPE).stdout.strip()

    return  submit
