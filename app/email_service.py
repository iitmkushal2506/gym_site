import logging
from flask import current_app
from flask_mail import Message
from app.extensions import mail

logger = logging.getLogger(__name__)


def send_async_email(app, msg):
    with app.app_context():
        try:
            if app.config.get('MAIL_USERNAME') and app.config.get('MAIL_PASSWORD'):
                mail.send(msg)
                logger.info(f"Email sent successfully to {msg.recipients}")
            else:
                logger.info(f"[EMAIL SIMULATION] To: {msg.recipients} | Subject: {msg.subject}\nBody:\n{msg.body}")
        except Exception as e:
            logger.warning(f"Failed to send real email via SMTP: {e}. Fallback to simulated delivery.")


def send_trial_confirmation(trial):
    """Notify customer of trial booking & alert admin."""
    app = current_app._get_current_object()
    gym_title = app.config.get('GYM_NAME', "Kushal's Gym Site")
    
    # 1. Customer Email
    cust_msg = Message(
        subject=f"Your Free Trial Pass at {gym_title} is Booked!",
        sender=app.config.get('MAIL_DEFAULT_SENDER'),
        recipients=[trial.email]
    )
    cust_msg.body = f"""Hi {trial.name},

Thank you for choosing {gym_title}!

We have received your Free Trial request. Here are your booking details:
- Date: {trial.preferred_date}
- Time Slot: {trial.preferred_time}
- Fitness Goal: {trial.fitness_goal}
- Status: Confirmed / Pass Active

What to Bring:
- Athletic workout wear & training shoes
- Water bottle & workout towel
- Government ID for gym check-in

Our team looks forward to welcoming you at {app.config.get('GYM_ADDRESS')}.

If you need to reschedule or have questions, reach us on WhatsApp: {app.config.get('GYM_PHONE')}.

Strength & Honor,
The {gym_title} Team
"""

    # 2. Admin Alert Email
    admin_email = app.config.get('ADMIN_NOTIFICATION_EMAIL') or app.config.get('MAIL_DEFAULT_SENDER')
    admin_msg = Message(
        subject=f"[NEW LEAD - FREE TRIAL] {trial.name} - {trial.preferred_date}",
        sender=app.config.get('MAIL_DEFAULT_SENDER'),
        recipients=[admin_email]
    )
    admin_msg.body = f"""NEW FREE TRIAL REQUEST RECEIVED

Name: {trial.name}
Email: {trial.email}
Phone: {trial.phone}
Age: {trial.age or 'N/A'}
Goal: {trial.fitness_goal}
Preferred Date: {trial.preferred_date}
Preferred Slot: {trial.preferred_time}
Notes: {trial.message or 'None'}

Log in to the Admin Dashboard to manage this lead.
"""

    send_async_email(app, cust_msg)
    send_async_email(app, admin_msg)


def send_consultation_confirmation(consultation, trainer_name="Assigned Coach"):
    """Notify customer of consultation request & alert gym."""
    app = current_app._get_current_object()
    gym_title = app.config.get('GYM_NAME', "Kushal's Gym Site")

    cust_msg = Message(
        subject=f"Consultation Request Received - {gym_title}",
        sender=app.config.get('MAIL_DEFAULT_SENDER'),
        recipients=[consultation.email]
    )
    cust_msg.body = f"""Hi {consultation.name},

We have received your Personal Training & Strategy Consultation request with Coach {trainer_name}.

Appointment Details (Status: PENDING REVIEW):
- Coach: {trainer_name}
- Date: {consultation.preferred_date}
- Time: {consultation.preferred_time}
- Focus: {consultation.goal}
- Experience Level: {consultation.fitness_level}

Our coaching manager will review your schedule and confirm the appointment within 24 hours.

Best regards,
{gym_title} Coaching Staff
"""

    admin_email = app.config.get('ADMIN_NOTIFICATION_EMAIL') or app.config.get('MAIL_DEFAULT_SENDER')
    admin_msg = Message(
        subject=f"[NEW APPOINTMENT - PENDING] {consultation.name} with {trainer_name}",
        sender=app.config.get('MAIL_DEFAULT_SENDER'),
        recipients=[admin_email]
    )
    admin_msg.body = f"""NEW CONSULTATION APPOINTMENT REQUEST

Client: {consultation.name}
Email: {consultation.email}
Phone: {consultation.phone}
Coach: {trainer_name}
Target Date: {consultation.preferred_date} at {consultation.preferred_time}
Focus: {consultation.goal}
Level: {consultation.fitness_level}
Notes: {consultation.message or 'None'}

Please confirm or reschedule this slot inside the Admin Appointments section.
"""

    send_async_email(app, cust_msg)
    send_async_email(app, admin_msg)


def send_enquiry_notification(enquiry):
    """Notify admin of general enquiry."""
    app = current_app._get_current_object()

    admin_email = app.config.get('ADMIN_NOTIFICATION_EMAIL') or app.config.get('MAIL_DEFAULT_SENDER')
    admin_msg = Message(
        subject=f"[NEW ENQUIRY] {enquiry.subject} - {enquiry.name}",
        sender=app.config.get('MAIL_DEFAULT_SENDER'),
        recipients=[admin_email]
    )
    admin_msg.body = f"""NEW WEBSITE ENQUIRY

From: {enquiry.name} ({enquiry.email}, {enquiry.phone})
Subject: {enquiry.subject}
Message:
{enquiry.message}
"""
    send_async_email(app, admin_msg)
