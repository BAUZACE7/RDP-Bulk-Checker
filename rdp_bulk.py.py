import subprocess
import concurrent.futures




def test_rdp_connection(pattern):
    ip = pattern[0].strip()
    user = pattern[1].strip()
    passwd = pattern[2].strip()

    command = f"xfreerdp /v:{ip} /u:{user} /p:'{passwd}' /cert-ignore +auth-only"

    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate(timeout=5)
        error_output = stderr
    
        if "_DNS_NAME_NOT_FOUND" in error_output:
            print(f'not working {ip}')
        elif "failed to connect" in error_output:
            print(f'not working {ip}')
        elif "STATUS_LOGON_FAILURE" in error_output:
            print(f'user or password is wrong {ip}')
        elif "Authentication only, exit status 0" in error_output:
            print(f'working {ip}')
        else:
            print(f'unknown error {ip}')

    except subprocess.TimeoutExpired:
        #another error, it takes long to print that error so we put it here!
        print(f"not working {ip}")

def main(filepath):
    with open(filepath, 'r') as fp:
        patterns = [line.split('|', 3) for line in fp]

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(test_rdp_connection, patterns)
                
if __name__ == "__main__":

    filepath = input('file name: ')
    main(filepath=filepath)
