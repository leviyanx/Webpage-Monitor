
# Webpage Monitor

### Features

- You can monitor the specified webpage, if the webpage is updated, send a notification to your specified email address. The notification email contains the changes.
- You can specify the interval of monitoring.
- You can set sender and receiver of the notification email.
- You **don't need to restart the script after changing the settings** in any setting file, the running script will automatically apply the new settings.

### Example

- [ ] show a example picture

### Requirement

#### Install Environment and Dependencies

Python@3.10

Download the denpendencies with the following command:

```bash
pip3 install -r requirements.txt
```

#### Setup Settings

Create a `receiver-settings.json` file in the same directory as the script. The file should contain the following (replace the values with your own):

```json
{
    "mailReceiver": "<receiver@mail.com>"
}
```

Create a `sender-settings.json` file in the same directory as the script. The file should contain the following (replace the values with your own):

```json
{
    "mailSender": "<sender@qq.com/foxmail.com>",
    "mailSenderPassword": "<password>"
}
```

**WARNING**: The sender mail **must** be a **qq mail** or **foxmail**, and you can get password de. you can get password depend on the rules that qq mail official website provides. (Maybe support other mail accounts in the future.)

Create a `monitor-settings.json` file in the same directory as the script. The file should contain the following (replace the values with your own):

- `targetUrl`: the url of the webpage you want to monitor
- `intervalToDetect`: the interval to detect the change of the webpage, in `seconds`

```json
{
    "targetUrl": "<http://example.com/url-of-target-webpage>",
    "intervalToDetect": 1800
}
```

TIP: It's recommended that set the interval to detect to be a little long. For example, 1800 seconds (30 minutes), 3600 seconds (1 hour), 86400 (1 day). Because the script will send a notification email to you if the webpage is updated. If you set the interval to be too short, you will receive too many emails.

---

You can also run the script to generate settings files above (But it's **not** recommended to do so when you **first** use the script, because there are some essential messages you need to read):

```bash
bash init.sh
```

### Usage

After the settings are done, run the script with the following command:

```bash
python3 WebpageMonitor.py
```

If you want to run the script in the **background** (in server), you can use `nohup`:

```bash
nohup python3 WebpageMonitor.py &
```

View the running status of the script:

```bash
ps aux | grep WebpageMonitor.py

# output example:
# USER PID ...  18:10   0:00 python3 WebsiteMonitor.py
```

And you can kill the script with the following command:

```bash
kill -9 <PID>
```

If you want to change settings (either url or email settings...), enjoy your freedom to change the settings in the corresponding setting files and go ahead do your work. The script will automatically apply the settings without restarting. 

### TODO

- [x] If target webpage is changed in `monitor-settings.json`, the script should take notice of it and apply it.
- [ ] Support multiple receivers
- [ ] Support more mail accounts of receiver
