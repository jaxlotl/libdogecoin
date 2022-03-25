from multiprocessing.connection import wait
import subprocess
import time

def get_shell_output(cmd):
    raw_output = subprocess.run(cmd, shell=True, capture_output=True).stdout
    str_output = raw_output.decode("utf-8")
    return str_output

try:
    subprocess.run("dogecoind -regtest &", shell=True)
    time.sleep(1) #CHANGE LATER
    transaction_hex = get_shell_output(f"dogecoin-cli createrawtransaction \"[{{\"txid\" : \"mytxid\",\"vout\":0}}]" "{\"myaddress\":0.01}\"")
    print(f"transaction hex is {transaction_hex}")
    signed_hex = get_shell_output(f"dogecoin-cli signrawtransactionwithwallet {transaction_hex}")
    print(f"signed hex is {signed_hex}")
    res = get_shell_output(f"dogecoin-cli sendrawtransaction {signed_hex}")
    print(res)
finally:
    dogepid = subprocess.run("pidof dogecoind", shell=True, capture_output=True).stdout.decode("utf-8")
    if dogepid:
        subprocess.run(str.format("kill {}", dogepid), shell=True)