from flask import current_app, render_template_string
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email(to_email, subject, html_content, text_content=None):
    """Send an email using SMTP configuration."""
    try:
        # Get email configuration from app config
        smtp_server = current_app.config.get('MAIL_SERVER')
        smtp_port = current_app.config.get('MAIL_PORT', 587)
        smtp_username = current_app.config.get('MAIL_USERNAME')
        smtp_password = current_app.config.get('MAIL_PASSWORD')
        use_tls = current_app.config.get('MAIL_USE_TLS', True)

        if not all([smtp_server, smtp_username, smtp_password]):
            current_app.logger.warning("Email configuration incomplete. Email not sent.")
            return False

        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = smtp_username
        msg['To'] = to_email

        # Add text content
        if text_content:
            text_part = MIMEText(text_content, 'plain')
            msg.attach(text_part)

        # Add HTML content
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)

        # Send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            if use_tls:
                server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)

        return True

    except Exception as e:
        current_app.logger.error(f"Failed to send email: {str(e)}")
        return False


def send_booking_confirmation(booking):
    """Send booking confirmation email to user."""
    subject = f"Booking Confirmation - Studio {booking.studio.name}"

    html_content = f"""
    <html>
        <body>
            <h2>Booking Confirmation</h2>
            <p>Dear {booking.user.name},</p>

            <p>Your booking has been confirmed with the following details:</p>

            <ul>
                <li><strong>Studio:</strong> {booking.studio.name}</li>
                <li><strong>Date:</strong> {booking.start_time.strftime('%B %d, %Y')}</li>
                <li><strong>Time:</strong> {booking.start_time.strftime('%I:%M %p')} - {booking.end_time.strftime('%I:%M %p')}</li>
                <li><strong>Duration:</strong> {(booking.end_time - booking.start_time).total_seconds() / 3600:.1f} hours</li>
                <li><strong>Total Amount:</strong> ${booking.total_amount:.2f}</li>
            </ul>

            {f'<p><strong>Photographer:</strong> {booking.photographer.user.name}</p>' if booking.photographer else ''}

            {f'<p><strong>Notes:</strong> {booking.notes}</p>' if booking.notes else ''}

            <p>Please arrive 15 minutes early for your session.</p>

            <p>If you need to make any changes or have questions, please contact us.</p>

            <p>Thank you for choosing our studio!</p>

            <p>Best regards,<br>PhotoStudio Booking Team</p>
        </body>
    </html>
    """

    text_content = f"""
    Booking Confirmation

    Dear {booking.user.name},

    Your booking has been confirmed:

    Studio: {booking.studio.name}
    Date: {booking.start_time.strftime('%B %d, %Y')}
    Time: {booking.start_time.strftime('%I:%M %p')} - {booking.end_time.strftime('%I:%M %p')}
    Duration: {(booking.end_time - booking.start_time).total_seconds() / 3600:.1f} hours
    Total Amount: ${booking.total_amount:.2f}

    {'Photographer: ' + booking.photographer.user.name if booking.photographer else ''}

    {'Notes: ' + booking.notes if booking.notes else ''}

    Please arrive 15 minutes early for your session.

    Thank you for choosing our studio!

    PhotoStudio Booking Team
    """

    return send_email(booking.user.email, subject, html_content, text_content)


def send_booking_cancellation(booking):
    """Send booking cancellation email to user."""
    subject = f"Booking Cancelled - Studio {booking.studio.name}"

    html_content = f"""
    <html>
        <body>
            <h2>Booking Cancellation</h2>
            <p>Dear {booking.user.name},</p>

            <p>Your booking has been cancelled:</p>

            <ul>
                <li><strong>Studio:</strong> {booking.studio.name}</li>
                <li><strong>Date:</strong> {booking.start_time.strftime('%B %d, %Y')}</li>
                <li><strong>Time:</strong> {booking.start_time.strftime('%I:%M %p')} - {booking.end_time.strftime('%I:%M %p')}</li>
                <li><strong>Amount:</strong> ${booking.total_amount:.2f}</li>
            </ul>

            <p>If you have any questions about this cancellation, please contact us.</p>

            <p>We hope to serve you again in the future.</p>

            <p>Best regards,<br>PhotoStudio Booking Team</p>
        </body>
    </html>
    """

    return send_email(booking.user.email, subject, html_content)