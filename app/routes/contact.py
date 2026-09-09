from flask import Blueprint, render_template, flash, redirect, url_for
from app.extensions import db
from app.models import Enquiry
from app.forms import ContactEnquiryForm
from app.email_service import send_enquiry_notification

contact_bp = Blueprint('contact', __name__)


@contact_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactEnquiryForm()
    
    if form.validate_on_submit():
        enquiry = Enquiry(
            name=form.name.data.strip(),
            email=form.email.data.strip().lower(),
            phone=form.phone.data.strip(),
            subject=form.subject.data.strip(),
            message=form.message.data.strip(),
            status='NEW'
        )
        db.session.add(enquiry)
        db.session.commit()
        
        # Send admin notification email
        send_enquiry_notification(enquiry)
        
        flash('Thank you for reaching out! Our membership team will contact you within 2 business hours.', 'success')
        return redirect(url_for('contact.contact'))
        
    return render_template('contact.html', form=form)
