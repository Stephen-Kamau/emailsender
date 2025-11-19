# **EmailStaffSDK (Python)**
This is a light weight email sdk that allows one to easily send emails by just providing staffs. The **EmailStaffSDK** is a wrapper around Python’s built-in `smtplib` and `email` modules.
It provides an API-style interface for composing and sending fully-featured emails without external dependencies.

This SDK dramatically simplifies tasks such as:

* Sending emails through any SMTP server
* Defining custom **Reply-To** addresses
* Managing **To**, **CC**, and **BCC** recipients
* Sending HTML emails
* Attaching files of any type
* Detailed logging of the sending workflow

It requires no install since it works with python build it module.


## Features

* **Custom Reply-To Handling**
  Essential for support teams, automated responses, ticketing systems, and transactional messaging.

* **Full Recipient Control**
  Send to multiple `to`, `cc`, and `bcc` recipients.

* **HTML + Attachments Support**
  Easily send rich HTML emails and include any number of files.

* **Detailed Logging**
  Every step — from composition to SMTP handshake — is logged for easier debugging.


## Setup

The SDK is a standalone utility. To use it you need:
```python
SMTP_SERVER = 'xxxx.smtp.server.com'
SMTP_PORT = 587
SENDER_EMAIL = 'sending@example.com'
SENDER_PASSWORD = 'senderPass'
```

> **Security Note**
> For providers like **Gmail** and **Outlook**, you must use an **App Password**, not your account's main password.
> (Gmail blocks SMTP using normal passwords.)


## Usage Example

Below is a complete example showing initialization and sending an email with recipients, attachments, and custom Reply-To:

```python
from email_utility import EmailStaffSDK 
# inititlaze
email_sdk = EmailStaffSDK(
    smtp_server='xxx.provider.com',
    smtp_port=587,
    sender_email='noreply@myapp.com',
    sender_password='AppPassword'
)

# send the email
success = email_sdk.send(
    sender_name="Automated Test System",
    to=['user1@org.com', 'user2@org.com'],
    subject="Quarterly Report Notification",
    body="<p>Please find the report attached. Replies go to Support.</p>",
    cc=['auditor@org.com'],
    bcc=['internal_log@org.com'],
    reply_to=['support@org.com'],
    attachments=['files.pdf'],
    is_html=True
)

if success:
    print("Email sent successfully!")
```


## **`send(...)` Method Reference**

| Parameter       | Type        | Required   | Description                                          |
| --------------- | ----------- | ---------- | ---------------------------------------------------- |
| **sender_name** | `str`       | ✔ Yes      | The human-readable name shown in the **From** field. |
| **to**          | `list[str]` | ✔ Yes      | Primary email recipients.                            |
| **subject**     | `str`       | ✔ Yes      | Subject line of the email.                           |
| **body**        | `str`       | ✔ Yes      | Email content — plain text or HTML.                  |
| **cc**          | `list[str]` | ✖ Optional | Carbon-copy recipients.                              |
| **bcc**         | `list[str]` | ✖ Optional | Blind-copy recipients (hidden).                      |
| **reply_to**    | `list[str]` | ✖ Optional | Address(es) to use in the **Reply-To** header.       |
| **attachments** | `list[str]` | ✖ Optional | Paths to local files to attach.                      |
| **is_html**     | `bool`      | ✖ Optional | Set `True` if `body` contains HTML markup.           |

