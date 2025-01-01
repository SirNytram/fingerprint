import serial
import time
import PySimpleGUI as sg
import platform
import psutil

users = {}
user = {"name":"martin", "age": 25}
users['martin'] = user

for key in users:
    print(key, users[key])

def send_and_receive(command):
    try:
        # Replace 'COM3' with your Arduino's port
        arduino = serial.Serial(port='COM3', baudrate=9600, timeout=1)
        time.sleep(2)  # Wait for the connection to establish

        arduino.write(f"{command}\n".encode())
        print(f"Sent: {command}")

        # Read the response
        response = arduino.readline().decode().strip()
        print(f"Received: {response}")

        arduino.close()
        return response
    except serial.serialutil.SerialException as e:
        print(f"Error: {e}")
        return None

def show_system_info():
    system_info = f"""
    System: {platform.system()}
    Node Name: {platform.node()}
    Release: {platform.release()}
    Version: {platform.version()}
    Machine: {platform.machine()}
    Processor: {platform.processor()}
    CPU Count: {psutil.cpu_count()}
    Memory: {psutil.virtual_memory().total / (1024 ** 3):.2f} GB
    """
    
    layout = [
        [sg.Multiline(system_info, size=(50, 10), disabled=True)],
        [sg.Button('Close')]
    ]
    
    window = sg.Window('System Information', layout)
    
    while True:
        event, _ = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Close':
            break
    
    window.close()

def main():
    layout = [
        [sg.Text("Enter the command to send to Arduino:")],
        [sg.Input(key='-COMMAND-')],
        [sg.Button('Send'), sg.Button('Exit')],
        [sg.Text("Response:", size=(40, 1)), sg.Text("", key='-RESPONSE-', size=(40, 1))],
        [sg.Button('Settings')]
    ]

    window = sg.Window('Arduino Command Sender', layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
        if event == 'Send':
            command = values['-COMMAND-']
            response = send_and_receive(command)
            if response:
                window['-RESPONSE-'].update(response)
            else:
                window['-RESPONSE-'].update("Error sending command")
        if event == 'Settings':
            show_system_info()

    window.close()

if __name__ == "__main__":
    main()