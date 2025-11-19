import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import logging 


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class EmailStaffSDK:
    """
    An utility for sending rich, complex emails via SMTP, 
    designed like a basic SDK.
    
    Configuration is managed during initialization, and the send method 
    handles all composition and logging.
    """
    def __init__(self, smtp_server, smtp_port, sender_email, sender_password):
        """
        Initializes the SDK with connection and authentication details.
        
        Args:
            smtp_server (str): The SMTP server address (e.g., 'smtp.gmail.com').
            smtp_port (int): The SMTP server port (e.g., 587 or 465).
            sender_email (str): The email address used for sending.
            sender_password (str): The password or app-specific password for the sender email.
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = sender_email
        self.sender_password = sender_password
        logger.info(f"EmailStaffSDK initialized for sender: {self.sender_email}")
        logger.info(f"Using SMTP server: {self.smtp_server}:{self.smtp_port}")

    def send(
        self,
        sender_name: str,
        to: list,
        subject: str,
        body: str,
        cc: list = None,
        bcc: list = None,
        reply_to: list = None,
        attachments: list = None,
        is_html: bool = False
    ):
        """
        create and sends a complex email, handling all recipients, Reply-To, 
        attachments, and logging the process.

        Args:
            sender_name (str): The name displayed as the sender (e.g., 'Staff Assistant').
            to (list): List of primary recipient email addresses.
            subject (str): The email subject line.
            body (str): The content of the email (can be plain text or HTML).
            cc (list, optional): List of CC recipient email addresses. Defaults to None.
            bcc (list, optional): List of BCC recipient email addresses. Defaults to None.
            reply_to (list, optional): List of email addresses to use for the Reply-To header.
                                       If specified, replies will go here instead of SENDER_EMAIL.
                                       Defaults to None.
            attachments (list, optional): List of file paths for attachments. Defaults to None.
            is_html (bool, optional): Set to True if the body is HTML content. Defaults to False.
        
        Returns:
            bool: True if the email was sent successfully, False otherwise.
        """
        logger.info(f"Starting email composition for subject: '{subject}'")

        msg = MIMEMultipart()
        msg['From'] = f"{sender_name} <{self.sender_email}>"
        msg['Subject'] = subject

        to_list = to if to else []
        cc_list = cc if cc else []
        bcc_list = bcc if bcc else []
        
        all_recipients = to_list + cc_list + bcc_list
        
        if not all_recipients:
            logger.error("No recipients provided. Aborting send operation.")
            return False

        if to_list:
            msg['To'] = ', '.join(to_list)
        if cc_list:
            msg['Cc'] = ', '.join(cc_list)


        reply_to_address = ', '.join(reply_to) if reply_to else self.sender_email
        msg.add_header('Reply-To', reply_to_address)
        logger.info(f"Set Reply-To header to: {reply_to_address}")
        
        mime_type = 'html' if is_html else 'plain'
        msg.attach(MIMEText(body, mime_type))
        logger.info(f"Attached body content as {mime_type}.")

        if attachments:
            for file_path in attachments:
                if not os.path.exists(file_path):
                    logger.warning(f"Attachment file not found: {file_path}. Skipping.")
                    continue

                try:
                    with open(file_path, 'rb') as fp:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(fp.read())
                        
                    encoders.encode_base64(part)
                    filename = os.path.basename(file_path)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename={filename}',
                    )
                    msg.attach(part)
                    logger.info(f"Successfully attached file: {filename}")

                except Exception as e:
                    logger.error(f"Error attaching file {file_path}: {e}")
                    return False
        
        try:
            logger.info(f"Connecting to SMTP server {self.smtp_server}:{self.smtp_port}...")
            
            if self.smtp_port == 465:
                server = smtplib.SMTP_SSL(self.smtp_server, self.smtp_port)
            else:
                server = smtplib.SMTP(self.smtp_server, self.smtp_port)
                server.ehlo()
                server.starttls() 
                server.ehlo()

            logger.info("Connection established. Logging in...")
            server.login(self.sender_email, self.sender_password)
            logger.info("Login successful. Sending email...")

            server.sendmail(self.sender_email, all_recipients, msg.as_string())

            server.quit()
            logger.info("SMTP server connection closed.")

            logger.info(f"Email sent successfully!")
            logger.info(f"To: {', '.join(to_list)}")
            logger.info(f"CC: {', '.join(cc_list)}")
            logger.info(f"BCC count: {len(bcc_list)}")
            
            return True

        except smtplib.SMTPAuthenticationError:
            logger.critical("SMTP Authentication Failed. Check SENDER_EMAIL and SENDER_PASSWORD/App Password.")
            return False
        except smtplib.SMTPConnectError as e:
            logger.critical(f"SMTP Connection Error. Check server address and port. Error: {e}")
            return False
        except Exception as e:
            logger.error(f"An unexpected error occurred during email transmission: {e}")
            return False

