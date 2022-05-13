import json
from tkinter import messagebox
import tkinter as tk
from turtle import clear
import screeninfo as scr
import time
import libdogecoin as w
import ctypes as ct
import subprocess


# HELPER METHODS
def display_radiobutton_user_choice(frame, choices):

    #clear frame
    clear_frame(frame)

    #display menu
    selection = tk.IntVar()
    op = [None]*len(choices)
    for i in range(len(choices)):
        op[i] = tk.Radiobutton(frame, variable=selection, text=choices[i], value=i)
        op[i].grid(row=i, sticky="w")

    #register choice on click
    ok = tk.Button(frame, text="OK", command=lambda: user_choice.set(selection.get()))
    ok.grid(row=len(choices), padx=5, pady=5)
    ok.wait_variable(user_choice)

    #return result
    return user_choice.get()


def receive_user_entry(frame, prompt):

    #clear frame
    clear_frame(frame)

    #write prompt
    msg = tk.Label(frame, text=prompt)
    msg.grid(row=1, column=1)

    #create entry box
    entry = tk.Entry(frame, width=30)
    entry.grid(row=2, column=1)

    #accept input on click
    ok = tk.Button(frame, text="OK", command=lambda: user_response.set(entry.get()))
    ok.grid(row=3, column=1)
    ok.wait_variable(user_response)
    
    #return result
    return str(user_response.get())

def display_error_output(frame, msg):
    clear_frame(frame)
    label = tk.Label(frame, test=msg, justify=tk.CENTER)
    label.grid()

def display_output(frame, labs, vals):
    clear_frame(frame)

    labels = [None]*len(labs)
    values = [None]*len(vals)
    copy_buttons = [None]*len(vals)

    for i in range(len(labs)):
        labels[i] = tk.Label(frame, text=labs[i], justify=tk.CENTER)
        labels[i].grid(row=3*i, sticky="nesw", columnspan=2)
        values[i] = tk.Label(frame, text=vals[i], justify=tk.LEFT, wraplength=int(win_width*0.5))
        values[i].grid(row=(3*i)+1, sticky="nesw", columnspan=2)
        copy_buttons[i] = tk.Button(frame, text="Copy to clipboard", command=lambda: copy_to_clipboard(vals[i]))
        copy_buttons[i].grid(row=(3*i)+2, sticky="nesw", columnspan=2, padx=5, pady=5)

def display_copyable_output(frame, labs, vals):
    clear_frame(frame)

    labels = [None]*len(labs)
    values = [None]*len(vals)
    copy_buttons = [None]*len(vals)

    for i in range(len(labs)):
        labels[i] = tk.Label(frame, text=labs[i], justify=tk.CENTER)
        labels[i].grid(row=3*i, sticky="nesw", columnspan=2)
        values[i] = tk.Label(frame, text=vals[i], justify=tk.LEFT, wraplength=int(win_width*0.5))
        values[i].grid(row=(3*i)+1, sticky="nesw", columnspan=2)
        copy_buttons[i] = tk.Button(frame, text="Copy to clipboard", command=lambda: copy_to_clipboard(vals[i]))
        copy_buttons[i].grid(row=(3*i)+2, sticky="nesw", columnspan=2, padx=5, pady=5)

def copy_to_clipboard(input):
    tmp = tk.Tk()
    tmp.withdraw()
    tmp.clipboard_clear()
    tmp.clipboard_append(input)
    tmp.destroy()

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def on_exit():
    w.context_stop()
    user_choice.set(-1)
    user_response.set("err")
    stop_nodes()
    root.destroy()


# LIBDOGE METHODS
def gen_keypair(in_frame, out_frame):
    clear_frame(in_frame)
    clear_frame(out_frame)
    chain_list = ["Main", "Testnet"]
    chain = display_radiobutton_user_choice(in_frame, chain_list)

    if user_choice.get() != -1:
        user_choice.set(None)
        res = w.generate_priv_pub_key_pair(chain_code=chain)
        labels = ["Wif-encoded private key:", "P2PKH address:"]
        values = list(res)
        display_copyable_output(out_frame, labels, values)


def gen_hdkeypair(in_frame, out_frame):
    clear_frame(in_frame)
    clear_frame(out_frame)
    chain_list = ["Main", "Testnet"]
    chain = display_radiobutton_user_choice(in_frame, chain_list)

    if user_choice.get() != -1:
        user_choice.set(None)
        res = w.generate_hd_master_pub_key_pair(chain_code=chain)
        labels = ["Wif-encoded master private key:", "P2PKH master public key:"]
        values = list(res)
        display_copyable_output(out_frame, labels, values)


def derive_child(in_frame, out_frame):
    clear_frame(in_frame)
    clear_frame(out_frame)
    master_key = receive_user_entry(in_frame, "Enter the master private key")

    if user_response.get() != "err":
        user_response.set(None)
        res = w.generate_derived_hd_pub_key(master_key)
        labels = ["Derived child P2PKH public key"]
        values = [res]
        display_copyable_output(out_frame, labels, values)


def verify_address(in_frame, out_frame):
    clear_frame(in_frame)
    clear_frame(out_frame)
    address = receive_user_entry(in_frame, "Enter p2pkh address:")
    clear_frame(in_frame)
    if w.verify_p2pkh_address(address):
        result = "Address is valid."
    else:
        result = "Address is invalid."
    message = tk.Label(out_frame, text=result, justify=tk.CENTER)
    message.grid()


def send_tx(in_frame, out_frame):
    # clear all elements in frame
    clear_frame(in_frame)
    clear_frame(out_frame)

    # read unspent transaction info
    raw_utxos = run_cmd_get_output("listunspent").split("},\n")

    # strip all JSON formatting
    utxos = []
    for ru in raw_utxos:
        utxos.append(ru.translate({ord(x): None for x in "{[]}"})) #ord(x) strips json of all brackets/braces
    
    # restore necessary braces
    fmtd_utxos = []
    for u in utxos:
        fmtd_utxos.append(json.loads(f"{{{u}}}"))

    # assign input information to variables
    inp_txids = []
    inp_vouts = []
    inp_addrs = []
    inp_scriptpks = []
    inp_amounts = []
    for fu in fmtd_utxos:
        inp_txids.append(fu["txid"])
        inp_vouts.append(fu["vout"])
        inp_addrs.append(fu["address"])
        inp_scriptpks.append(fu["scriptPubKey"])
        inp_amounts.append(fu["amount"])

    # generate keys/addresses
    my_addr = inp_addrs[0] # all record addresses should be the same
    LOLA = "nbMFaHF9pjNoohS4fD1jefKBgDnETK9uPu"
    KRAMER = "nnY36T2PtRywcp7amPMEVAYgiSpVMC7kow"
    priv = run_cmd_get_output(f"dumpprivkey {my_addr}").strip()

    # user set transaction parameters
    ext_addr = receive_user_entry(in_frame, "Enter address to send to: ")
    if ext_addr=="lola":
        ext_addr = LOLA
    if ext_addr=="kramer":
        ext_addr = KRAMER
    send_amt = int(receive_user_entry(in_frame, "Enter send amount (INTEGER ONLY): "))
    fee = float(receive_user_entry(in_frame, "Enter fee amount: "))

    # collect inputs
    input_total = 0
    num_inputs = 0
    while input_total<send_amt:
        input_total += inp_amounts[num_inputs]
        num_inputs+=1

    # build transaction and display components
    idx = w.w_start_transaction()
    column1_width = 100
    column2_width = 10
    input_header = tk.Label(out_frame, text="Inputs:", justify=tk.LEFT)
    input_header.grid(row=0, column=0, sticky="w")
    inputs = []
    for i in range(num_inputs):
        inputs.append(tk.Label(out_frame, text=f"\t{inp_addrs[i]:<{column1_width}}{str(inp_amounts[i]):>{column2_width}}", justify=tk.LEFT))
        inputs[i].grid(row=i+1, sticky="w")
        assert(w.w_add_utxo(idx, inp_txids[i], inp_vouts[i])==1)
    assert(w.w_add_output(idx, ext_addr, send_amt)==1)
    raw_tx = w.w_finalize_transaction(idx, ext_addr, fee, int(input_total), my_addr)
    
    output_header = tk.Label(out_frame, text="Outputs:", justify=tk.LEFT)
    output_header.grid(row=num_inputs+2, column=0, sticky="w")
    outputs = []
    outputs.append(tk.Label(out_frame, text=f"\t{ext_addr:<{column1_width}}{str(send_amt):>{column2_width}}", justify=tk.LEFT))
    outputs[0].grid(row=num_inputs+3, column=0, sticky="w")
    outputs.append(tk.Label(out_frame, text=f"\t{my_addr:<{column1_width}}{str(int(input_total)-fee-send_amt):>{column2_width}}", justify=tk.LEFT))
    outputs[1].grid(row=num_inputs+4, column=0, sticky="w")
    outputs.append(tk.Label(out_frame, text=f"\t{'Transaction Fee':<{column1_width}}{str(fee):>{column2_width}}", justify=tk.LEFT))
    outputs[2].grid(row=num_inputs+5, column=0, sticky="w")

    # sign all inputs of the transaction
    for i in range(num_inputs):
        raw_tx = w.w_sign_raw_transaction(i, raw_tx, inp_scriptpks[i], 1, int(inp_amounts[i]), priv)
    signed_tx = raw_tx
    print("final signed tx:",signed_tx)

    # confirm and send transaction
    def send_transaction():
        clear_frame(in_frame)
        run_cmd_get_output(f'sendrawtransaction {signed_tx}')
        
    send_button = tk.Button(in_frame, text="SEND", command=send_transaction)
    send_button.grid()
    

# RPC METHODS
def start_server():
    dogepid = subprocess.run("pidof dogecoind", shell=True, capture_output=True).stdout.decode("utf-8")
    if not dogepid:
        conf_path = "../.dogecoin/dogecoin.conf"
        subprocess.run(f"dogecoind -{chain} -conf={conf_path} &", shell=True) # assigned to port 18443 in conf
        start_node2()
    # satoshi password:   ODywh9M6DF8U8GU7YFhNDwG0NnlG5BVSAABW7ahes8A=

def start_node2():
    conf_path = "../.dogecoin/dogecoin-client.conf"
    subprocess.run(f"dogecoind -{chain} -rpcport={node2_rpcport} -conf={conf_path} &", shell=True) # assigned to port 18444 in conf
    # satoshi2 password:   CzTZr8-hQ1LniGNi-KFD8f6BPZsqbHdsLUhpGD7M8TI=

def stop_nodes():
    if messagebox.askyesno("Exit", "Stop nodes?"):
        dogepid = subprocess.run("pidof dogecoind", shell=True, capture_output=True).stdout.decode("utf-8")
        if dogepid:
            run_cmd_get_output("stop")
            run_rpc_cmd_get_output("stop")

def run_cmd_get_output(cmd):
    raw_output = subprocess.run(f"dogecoin-cli -{chain} {cmd}", shell=True, capture_output=True).stdout
    str_output = raw_output.decode("utf-8")
    return str_output

def run_rpc_cmd_get_output(cmd):
    raw_output = subprocess.run(f"dogecoin-cli -{chain} -rpcport={node2_rpcport} -rpcuser={node2_rpcuser} -rpcpassword={node2_rpcpwd} {cmd}", shell=True, capture_output=True).stdout
    str_output = raw_output.decode("utf-8")
    return str_output



# FRAME CONTROL
def display_main():
    # set up frames
    operation_frame = tk.Frame(root, height=win_height/2, width=win_width/3, borderwidth=2, relief="ridge", padx=5, pady=5)
    input_frame = tk.Frame(root, height=win_height/2, width=(2*win_width)/3, borderwidth=2, relief="ridge", padx=5, pady=5)
    output_frame = tk.Frame(root, height=win_height/2, width=win_width, borderwidth=2, relief="ridge", padx=5, pady=5)

    operation_frame.grid(row=0, column=0, sticky="nesw")
    input_frame.grid(row=0, column=1, sticky="nesw")
    output_frame.grid(row=1, column=0, columnspan=2, sticky="nesw")

    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(2, weight=2)
    
    # function options
    function_options = [("Generate private/public keypair",         lambda: gen_keypair(input_frame, output_frame)),
                        ("Generate HD private/public keypair",      lambda: gen_hdkeypair(input_frame, output_frame)),
                        ("Derive child key from HD master key",     lambda: derive_child(input_frame, output_frame)),
                        ("Verify address",                          lambda: verify_address(input_frame, output_frame)),
                        ("Send transaction",                        lambda: send_tx(input_frame, output_frame))]

    # populate operation frame
    op_buttons = [None]*len(function_options)
    for i in range(len(function_options)):
        op_buttons[i] = tk.Button(operation_frame, text=function_options[i][0], command=function_options[i][1])
        op_buttons[i].grid(column=0, row=i, sticky="nesw", pady=5, padx=5)


#MAIN

# establish root container
root = tk.Tk()
root.title("Dogecoin Simple GUI")

# get screen dimensions
curr_screen = scr.get_monitors()[0]
win_width = int(curr_screen.width*0.4)
win_height = int(curr_screen.height*0.6)
x_offset = int((curr_screen.width-win_width)/2)
y_offset = int((curr_screen.height-win_height)/2)
root.geometry('{}x{}+{}+{}'.format(win_width, win_height, x_offset, y_offset)) # position in screen middle, 60% of the heigh and 40% of the width

#create user response variables
user_choice = tk.IntVar()
user_response = tk.StringVar()

#start app
chain = "testnet"
node2_rpcport = 8333
node2_rpcuser = "satoshi2"
node2_rpcpwd = "CzTZr8-hQ1LniGNi-KFD8f6BPZsqbHdsLUhpGD7M8TI="
start_server()
w.context_start()
display_main()
root.protocol('WM_DELETE_WINDOW', on_exit)
try:
    root.mainloop()
except:
    on_exit()
