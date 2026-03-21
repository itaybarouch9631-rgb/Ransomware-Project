# Advanced Ransomware attack (Hybrid Encryption & TLS)

This project is Ransomware attack. It demonstrates the lifecycle of an infection, from silent background encryption to a secure decryption process controlled by C2 server.
 

How it Works:
1. **Silent Infection**==: Upon execution, the client automatically connects to the server, receives an AES key, and encrypts the target directory without user intervention.
2. **Hybrid Encryption**: 
    * **AES-256**: Used for high-speed file encryption.
    * **RSA-2048**: Used to protect the AES keys within the server's database.
3. **Secure Communication**: All data exchange is wrapped in a **TLS/SSL** tunnel using `server.crt` and `server.key`.
4. **Automated Recovery**: Once the payment status is updated in the **SQLite** database, the client can automatically retrieve the key and restore the files.

---

## Project Structure:

### Attacker Side (Server)
* `ransomware_server.py`: The entry point that starts the C2 server.
* `secure_server.py`: Handles TLS wrapping and multi-threaded client connections.
* `client_handler.py`: The "Brain" - manages DB logic, RSA encryption, and command flow.
* `generate_rsa_keys.py`: Utility to generate the master RSA key pair.
* `simulate_payment.py`: Admin tool to manually verify a victim's payment.

### Victim Side (Client)
* `secure_client.py`: The malware executable. It connects, encrypts, and waits for the decryption signal.
* `cipher_utils.py`: The cryptographic engine for file-system operations.

### used by many files
* `protocol.py`: Custom messaging protocol to ensure data integrity over sockets.

---

## Getting Started

### 1. Befor Running:
Install the required cryptographic library:
```bash
pip install pycryptodome
2. Setup Keys
Generate the RSA keys used for securing the database:

Bash
python generate_rsa_keys.py
Ensure you have server.crt and server.key in the server folder for TLS.

3. Running the Simulation
Start the Server:

Bash
python ransomware_server.py
Infect the Client:
Run the client on the victim machine/folder:

Bash
python secure_client.py
The client will automatically encrypt files in the designated test folder.

Simulate Payment:
Update the database status for the victim's IP:

Bash
python simulate_payment.py
Restore Files:
Run the client again. It will detect the "Paid" status, receive the key, and decrypt everything.

IMPORTANT!
This project is for educational and research purposes only. It was created to help cybersecurity students understand the mechanics of ransomware and how to defend against it. Do not use this code for any malicious activities.
