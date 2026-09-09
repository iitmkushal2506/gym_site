from flask import Blueprint, render_template, redirect, url_for, flash, request
from app.extensions import db
from app.models import TrialRequest, Consultation, Trainer
from app.forms import TrialBookingForm, ConsultationBookingForm
from app.email_service import send_trial_confirmation, send_consultation_confirmation

booking_bp = Blueprint('booking', __name__)


@booking_bp.route('/book-trial', methods=['GET', 'POST'])
def book_trial():
    form = TrialBookingForm()
    
    if form.validate_on_submit():
        trial = TrialRequest(
            name=form.name.data.strip(),
            email=form.email.data.strip().lower(),
            phone=form.phone.data.strip(),
            age=form.age.data,
            fitness_goal=form.fitness_goal.data,
            preferred_date=form.preferred_date.data,
            preferred_time=form.preferred_time.data,
            message=form.message.data.strip() if form.message.data else None,
            status='NEW'
        )
        db.session.add(trial)
        db.session.commit()
        
        # Send confirmation email and admin alert
        send_trial_confirmation(trial)
        
        flash('Your 1-Day VIP Trial Pass has been registered! Check your email for pass details.', 'success')
        return redirect(url_for('booking.success', type='trial', name=trial.name, date=trial.preferred_date, slot=trial.preferred_time))
        
    return render_template('book_trial.html', form=form)


@booking_bp.route('/book-consultation', methods=['GET', 'POST'])
def book_consultation():
    form = ConsultationBookingForm()
    
    # Populate trainer choices dynamically
    active_trainers = Trainer.query.filter_by(is_active=True).all()
    form.trainer_id.choices = [(t.id, f"{t.name} — {t.specialization}") for t in active_trainers]
    
    # Pre-select trainer if provided via query param ?trainer=slug
    trainer_slug = request.args.get('trainer')
    if request.method == 'GET' and trainer_slug:
        matched_trainer = Trainer.query.filter_by(slug=trainer_slug, is_active=True).first()
        if matched_trainer:
            form.trainer_id.data = matched_trainer.id

    if form.validate_on_submit():
        chosen_trainer_id = form.trainer_id.data
        chosen_date = form.preferred_date.data.strip()
        chosen_time = form.preferred_time.data.strip()
        
        # Check for double booking conflict with non-cancelled consultations
        existing_slot = Consultation.query.filter(
            Consultation.trainer_id == chosen_trainer_id,
            Consultation.preferred_date == chosen_date,
            Consultation.preferred_time == chosen_time,
            Consultation.status.in_(['PENDING', 'CONFIRMED'])
        ).first()
        
        trainer = Trainer.query.get(chosen_trainer_id)
        trainer_name = trainer.name if trainer else "Coach"
        
        if existing_slot:
            flash(
                f"Sorry, {trainer_name} already has an appointment booked on {chosen_date} at {chosen_time}. "
                "Please select another time slot or date.",
                "warning"
            )
            return render_template('book_consultation.html', form=form, trainers=active_trainers)
            
        # Create pending appointment
        consultation = Consultation(
            name=form.name.data.strip(),
            email=form.email.data.strip().lower(),
            phone=form.phone.data.strip(),
            trainer_id=chosen_trainer_id,
            goal=form.goal.data,
            fitness_level=form.fitness_level.data,
            preferred_date=chosen_date,
            preferred_time=chosen_time,
            message=form.message.data.strip() if form.message.data else None,
            status='PENDING'
        )
        db.session.add(consultation)
        db.session.commit()
        
        # Dispatch emails
        send_consultation_confirmation(consultation, trainer_name=trainer_name)
        
        flash(
            f'Your consultation request with {trainer_name} has been submitted (Status: PENDING). '
            'Our team will verify the schedule and confirm your booking.',
            'success'
        )
        return redirect(url_for(
            'booking.success',
            type='consultation',
            name=consultation.name,
            trainer=trainer_name,
            date=consultation.preferred_date,
            slot=consultation.preferred_time
        ))

    return render_template('book_consultation.html', form=form, trainers=active_trainers)


@booking_bp.route('/success')
def success():
    booking_type = request.args.get('type', 'booking')
    name = request.args.get('name', 'Fitness Enthusiast')
    trainer = request.args.get('trainer')
    date = request.args.get('date')
    slot = request.args.get('slot')
    
    return render_template(
        'success.html',
        booking_type=booking_type,
        name=name,
        trainer=trainer,
        date=date,
        slot=slot
    )
