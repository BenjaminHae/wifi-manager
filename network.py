#!/usr/bin/python3
import dbus

def connectWifi(ssid, encryption, passphrase):
        #todo: encryption type
        bus = dbus.SystemBus()
        # Obtain handles to manager objects.
        manager_bus_object = bus.get_object("org.freedesktop.NetworkManager",
                                            "/org/freedesktop/NetworkManager")
        manager = dbus.Interface(manager_bus_object,
                                 "org.freedesktop.NetworkManager")
        manager_props = dbus.Interface(manager_bus_object,
                                       "org.freedesktop.DBus.Properties")
        # Assuming Wireless is already enabled
        # Assuming we want wlan0
        device_path = manager.GetDeviceByIpIface("wlan0")
        print("wlan0 path: ", device_path)
         # Connect to the device's Wireless interface and obtain list of access
        # points.
        device = dbus.Interface(bus.get_object("org.freedesktop.NetworkManager",
                                               device_path),
                                "org.freedesktop.NetworkManager.Device.Wireless")
        accesspoints_paths_list = device.GetAccessPoints()

        # Identify our access point. We do this by comparing our desired SSID
        # to the SSID reported by the AP.
        our_ap_path = None
        for ap_path in accesspoints_paths_list:
            ap_props = dbus.Interface(
                bus.get_object("org.freedesktop.NetworkManager", ap_path),
                "org.freedesktop.DBus.Properties")
            ap_ssid = ap_props.Get("org.freedesktop.NetworkManager.AccessPoint",
                                   "Ssid")
            # Returned SSID is a list of ASCII values. Let's convert it to a proper
            # string.
            str_ap_ssid = "".join(chr(i) for i in ap_ssid)
            print(ap_path, ": SSID =", str_ap_ssid)
            if str_ap_ssid == ssid:
                our_ap_path = ap_path
                break
        if not our_ap_path:
          print("AP not found :(")
          exit(2)
        print("Our AP: ", our_ap_path)
        # At this point we have all the data we need. Let's prepare our connection
        # parameters so that we can tell the NetworkManager what is the passphrase.
        connection_params = {
            "802-11-wireless": {
                "security": "802-11-wireless-security",
            },
            "802-11-wireless-security": {
                "key-mgmt": "wpa-psk", # Encryption Type: wpa-psk, 
                "psk": passphrase
            },
        }
        # Establish the connection.
        settings_path, connection_path = manager.AddAndActivateConnection(
            connection_params, device_path, our_ap_path)
        print("settings_path =", settings_path)
        print("connection_path =", connection_path)
        # Connect
        connection_props = dbus.Interface(
          bus.get_object("org.freedesktop.NetworkManager", connection_path),
          "org.freedesktop.DBus.Properties")
