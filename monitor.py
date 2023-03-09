from WebsiteMonitor import WebsiteMonitor

# load file in local machine
monitor_settings_file = 'monitor-settings.json'
sender_settings_file = 'sender-settings.json'
receiver_settings_file = 'receiver-settings.json'

# monitor
monitor = WebsiteMonitor()
monitor.monitor_multiple_webpages_and_notify(monitor_settings_file, sender_settings_file, receiver_settings_file)
