import tkinter as tk
import screeninfo as scr
import time
import sys
sys.path.append("./bindings/py_wrappers/libdogecoin/")
import wrappers as w

# HELPER METHODS
def display_radiobutton_choice(frame, choices):

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
    return int(user_choice.get())


def receive_entry(frame, prompt):

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


def display_output(frame, labs, vals):

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
    user_choice.set(-1)
    user_response.set("err")
    root.destroy()


# LIBDOGE METHODS
def gen_keypair(in_frame, out_frame):
    clear_frame(in_frame)
    clear_frame(out_frame)
    chain_list = ["Main", "Testnet"]
    chain = display_radiobutton_choice(in_frame, chain_list)

    if user_choice.get() != -1:
        user_choice.set(None)
        res = w.generate_priv_pub_key_pair(chain_code=chain)
        labels = ["Wif-encoded private key:", "P2PKH address:"]
        values = list(res)
        display_output(out_frame, labels, values)

def gen_hdkeypair(in_frame, out_frame):
    clear_frame(in_frame)
    clear_frame(out_frame)
    chain_list = ["Main", "Testnet"]
    chain = display_radiobutton_choice(in_frame, chain_list)

    if user_choice.get() != -1:
        user_choice.set(None)
        res = w.generate_hd_master_pub_key_pair(chain_code=chain)
        labels = ["Wif-encoded master private key:", "P2PKH master public key:"]
        values = list(res)
        display_output(out_frame, labels, values)

def derive_child(in_frame, out_frame):
    clear_frame(in_frame)
    clear_frame(out_frame)
    master_key = receive_entry(in_frame, "Enter the master private key")

    if user_response.get() != "err":
        user_response.set(None)
        res = w.generate_derived_hd_pub_key(master_key)
        labels = ["Derived child P2PKH public key"]
        values = [res]
        display_output(out_frame, labels, values)

def display_main():
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
    
    button1 = tk.Button(operation_frame, text="Generate private/public keypair", command=lambda: gen_keypair(input_frame, output_frame))
    button2 = tk.Button(operation_frame, text="Generate HD private/public keypair", command=lambda: gen_hdkeypair(input_frame, output_frame))
    button3 = tk.Button(operation_frame, text="Derive child key from HD master key", command=lambda: derive_child(input_frame, output_frame))
    button1.grid(column=0, row=0, sticky="nesw", pady=5, padx=5)
    button2.grid(column=0, row=1, sticky="nesw", pady=5, padx=5) 
    button3.grid(column=0, row=2, sticky="nesw", pady=5, padx=5)


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
root.geometry('{}x{}+{}+{}'.format(win_width, win_height, x_offset, y_offset))

#load function library
dogelib = w.load_libdogecoin()

#create user response variables
user_choice = tk.IntVar()
user_response = tk.StringVar()

#start app
display_main()
root.protocol('WM_DELETE_WINDOW', on_exit)
root.mainloop()
