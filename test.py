# sample test
from dotenv import load_dotenv
import os
from email_utility import EmailStaffSDK
import logging

load_dotenv()

# get the creds
SMTP_SERVER = os.getenv("SMTP_SERVER")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")


# sample file
sample_file_attach = "jira_req.txt"

# intiialize the sdk
email_sdk = EmailStaffSDK(
    smtp_server=SMTP_SERVER,
    smtp_port=SMTP_PORT,
    sender_email=SENDER_EMAIL,
    sender_password=SENDER_PASSWORD
)



# subject
subject = "JIRA Update:>> ML Credit Scoring Model >> Weekly Progress Report"


# sample body
body = """
<html>
    <body style="font-family: Arial, sans-serif; padding: 20px;">
        
        <h2 style="color: #0052CC;">[JIRA] ML Credit Scoring System – Weekly Update</h2>

        <p>Dear Team,</p>

        <p>
            This email provides an automated update from the <strong>EmailStaffSDK</strong> regarding the 
            ongoing development of the <em>Machine Learning Credit Scoring Engine</em> for the banking platform.
        </p>

        <h3 style="color:#172B4D;"> Summary of Work Completed</h3>
        <ul>
            <li><strong>Model Feature Pipeline:</strong> Implemented new transactional behavior signals.</li>
            <li><strong>Credit Score Calibration:</strong> Improved stability across low-volume accounts.</li>
            <li><strong>Data Quality Layer:</strong> Added anomaly detection for malformed KYC data.</li>
            <li><strong>JIRA Task:</strong> <code>MLCS-417</code> – Feature Drift Monitoring Completed.</li>
        </ul>

        <h3 style="color:#172B4D;"> Next Steps</h3>
        <ol>
            <li>Deploy model candidate v1.8 to staging for sensitivity analysis.</li>
            <li>Integrate bureau data scoring baseline (Task <code>MLCS-433</code>).</li>
            <li>Finalize explainability dashboard for audit compliance.</li>
        </ol>

        <p>
            Please review the included attachment for additional metrics and logs. 
            If you have any questions, kindly reply to this email—your message will be 
            routed to the appropriate support contact via the configured <strong>Reply-To</strong> header.
        </p>

        <p>Sincerely,<br/>ML Engineering Team</p>
    </body>
</html>
"""


# send the email
success = email_sdk.send(
    sender_name="ML HOOOOOMAAN!",
    to=['stiveckamash@gmail.com'],
    subject=subject,
    body=body,
    cc=[],
    bcc=[], 
    reply_to=['ml.admin@org.com'],
    attachments=[sample_file_attach],
    is_html=True
)

if success:
    print("Main script finished successfully.")
else:
    print("Main script finished with email sending failure.")
