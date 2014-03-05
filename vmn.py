import subprocess
from utils import *

#
# interface functions for verificatum commands
#

def kill_verificatum():
    print("killing previous verificatum instances..")
    # TODO

def pre_kill_verificatum(func):
    def go(*args, **kwargs):
        # TODO: add some config flag
        if(True):
            kill_verificatum()

        return func(*args, **kwargs)
    return go

@pre_kill_verificatum
def v_gen_protocol_info(session_id, name, num_parties, num_threshold_parties, session_privpath):
    command = ["vmni", "-prot", "-sid", session_id, "-name", name, "-nopart",
        str(num_parties), "-thres", str(num_threshold_parties)]

    return subprocess.check_call(command, cwd=session_privpath)

@pre_kill_verificatum
def v_gen_private_info(auth_name, server_url, hint_server_url, session_privpath):
    command = ["vmni", "-party", "-arrays", "file", "-name", auth_name, "-http",
            server_url, "-hint", hint_server_url]

    return subprocess.check_call(command, cwd=session_privpath)

@pre_kill_verificatum
def v_merge(protinfos, session_privpath):
    start = ["vmni", "-merge"]
    command = start + protinfos

    return subprocess.check_call(command, cwd=session_privpath)

@pre_kill_verificatum
def v_gen_public_key(session_privpath, output_filter):
    return call_cmd(["vmn", "-keygen", "publicKey_raw"], cwd=session_privpath,
             timeout=10*60, check_ret=0, output_filter=output_filter)

@pre_kill_verificatum
def v_mix(session_privpath):
    return call_cmd(["vmn", "-mix", "privInfo.xml", "protInfo.xml",
        "ciphertexts_raw", "plaintexts_raw"], cwd=session_privpath,
        timeout=5*3600, check_ret=0)

@pre_kill_verificatum
def v_reset(election_private_path):
    return subprocess.check_call(["vmn", "-reset", "privInfo.xml", "protInfo.xml",
      "-f"], cwd=election_private_path)

@pre_kill_verificatum
def v_verify(protinfo_path, proofs_path):
    return subprocess.check_output(["vmnv", protinfo_path, proofs_path, "-v"])

@pre_kill_verificatum
def v_convert_pkey_json(session_privpath):
  return call_cmd(["vmnc", "-pkey", "-outi", "json", "publicKey_raw",
    "publicKey_json"], cwd=session_privpath, timeout=20, check_ret=0)

@pre_kill_verificatum
def v_convert_ctexts_json(session_privpath):
    return subprocess.check_call(["vmnc", "-ciphs", "-ini", "json",
            "ciphertexts_json", "ciphertexts_raw"], cwd=session_privpath)

@pre_kill_verificatum
def v_convert_plaintexts_json(session_privpath):
    return call_cmd(["vmnc", "-plain", "-outi", "json", "plaintexts_raw",
        "plaintexts_json"], cwd=session_privpath, check_ret=0, timeout=3600)