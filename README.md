
# Webpage Monitor

### Example

`todo`: show a example picture

### Requirement

Python@3.10

Setting files

- receiver-settings.json
- sender-settings.json
- monitor-settings.json

##### receiver-settings.json

This file is used to set receiver mail address.

Example

```json
{
    "mailReceiver": "<receiver@mail.com>"
}
```

##### sender-settings.json

This file is used to set a mail account that sends mail to receiver.

Example

```json
{
    "mailSender": "<sender@mail.com>",
    "mailSenderPassword": "<password>"
}
```

##### monitor-settings.json

This file is used to set webpage that you want to monitor.

Example

```json
{
    "targetUrl": "<http://example.com/url-of-target-webpage>"
    "intervalToDetect": 1800
}
```

### Usage

`todo`:
1. prepare three files
2. run the script

