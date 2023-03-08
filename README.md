
# Webpage Monitor

### Example

`todo`: show a example picture

### Requirement

Python@3.10

Download the denpendencies with the following command:

```bash
pip3 install -r requirements.txt
```

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

Tip: The sender mail **must** be a **qq mail** or **foxmail**, and you can get password de. you can get password depend on the rules that qq mail official website provides. (Maybe support other mail accounts in the future.)

Create a `monitor-settings.json` file in the same directory as the script. The file should contain the following (replace the values with your own):

- `targetUrl`: the url of the webpage you want to monitor
- `intervalToDetect`: the interval to detect the change of the webpage, in `seconds`

```json
{
    "targetUrl": "<http://example.com/url-of-target-webpage>",
    "intervalToDetect": 1800
}
```

### Usage

After the settings are done, run the script with the following command:

```bash
python3 monitor.py
```

### TODO

- [ ] If target webpage is changed in `monitor-settings.json`, the script should take notice of it and respond to it.
- [ ] Support multiple receivers
- [ ] Support more mail accounts of receiver
