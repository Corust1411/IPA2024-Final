from netmiko import ConnectHandler
from pprint import pprint

device_ip = "10.0.15.184"
username = "admin"
password = "cisco"

device_params = {
    "device_type": "cisco_ios",
    "ip": device_ip,
    "username": username,
    "password": password,
}


def gigabit_status():
    ans = ""
    with ConnectHandler(**device_params) as ssh:
        up = 0
        down = 0
        admin_down = 0
        # Run command and parse output using TextFSM
        result = ssh.send_command("show ip interface brief", use_textfsm=True)
        
        # print(result)

        interface_status = []
        for status in result:
            if status['interface'].startswith("GigabitEthernet"):
                iface = status['interface']
                iface_status = status['status'].lower()  # Normalize case for matching

                if iface_status == "up":
                    up += 1
                elif iface_status == "down":
                    down += 1
                elif iface_status == "administratively down":
                    admin_down += 1

                # Append interface status to the list for formatted output
                interface_status.append(f"{iface} {iface_status}")

        # Format the summary message
        ans = ", ".join(interface_status) + f" -> {up} up, {down} down, {admin_down} administratively down"
        pprint(ans)
        return ans
