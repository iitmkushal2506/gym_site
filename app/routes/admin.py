from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, jsonify
from flask_login import login_required, current_user
from app.extensions import db
from app.models import (
    Admin, MembershipPlan, Trainer, GymClass, Facility, GalleryImage,
    Transformation, Testimonial, TrialRequest, Consultation, Enquiry,
    LeadNote, InstagramReel
)
from app.forms import (
    MembershipPlanForm, TrainerForm, GymClassForm, FacilityForm,
    TransformationForm, TestimonialForm, InstagramReelForm, LeadNoteForm
)

admin_bp = Blueprint('admin', __name__)


# ----------------------------------------------------
# 1. DASHBOARD
# ----------------------------------------------------
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    # Dynamic counts from DB
    trial_count = TrialRequest.query.count()
    new_trials = TrialRequest.query.filter_by(status='NEW').count()
    
    consultation_count = Consultation.query.count()
    pending_appointments = Consultation.query.filter_by(status='PENDING').count()
    confirmed_appointments = Consultation.query.filter_by(status='CONFIRMED').count()
    
    enquiry_count = Enquiry.query.count()
    new_enquiries = Enquiry.query.filter_by(status='NEW').count()
    
    total_leads = trial_count + consultation_count + enquiry_count
    new_leads = new_trials + pending_appointments + new_enquiries
    
    trainer_count = Trainer.query.count()
    plan_count = MembershipPlan.query.count()
    class_count = GymClass.query.count()
    reels_count = InstagramReel.query.count()
    
    recent_trials = TrialRequest.query.order_by(TrialRequest.created_at.desc()).limit(5).all()
    recent_consultations = Consultation.query.order_by(Consultation.created_at.desc()).limit(5).all()
    recent_enquiries = Enquiry.query.order_by(Enquiry.created_at.desc()).limit(5).all()

    return render_template(
        'admin/dashboard.html',
        total_leads=total_leads,
        new_leads=new_leads,
        trial_count=trial_count,
        new_trials=new_trials,
        consultation_count=consultation_count,
        pending_appointments=pending_appointments,
        confirmed_appointments=confirmed_appointments,
        enquiry_count=enquiry_count,
        new_enquiries=new_enquiries,
        trainer_count=trainer_count,
        plan_count=plan_count,
        class_count=class_count,
        reels_count=reels_count,
        recent_trials=recent_trials,
        recent_consultations=recent_consultations,
        recent_enquiries=recent_enquiries
    )


# ----------------------------------------------------
# 2. LEAD MANAGEMENT (Unified Pipeline)
# ----------------------------------------------------
@admin_bp.route('/leads')
@login_required
def leads():
    lead_type = request.args.get('type', 'ALL')
    status_filter = request.args.get('status', 'ALL')
    search_q = request.args.get('q', '').strip()

    trials_query = TrialRequest.query
    consultations_query = Consultation.query
    enquiries_query = Enquiry.query

    if search_q:
        trials_query = trials_query.filter(
            (TrialRequest.name.ilike(f'%{search_q}%')) |
            (TrialRequest.email.ilike(f'%{search_q}%')) |
            (TrialRequest.phone.ilike(f'%{search_q}%'))
        )
        consultations_query = consultations_query.filter(
            (Consultation.name.ilike(f'%{search_q}%')) |
            (Consultation.email.ilike(f'%{search_q}%')) |
            (Consultation.phone.ilike(f'%{search_q}%'))
        )
        enquiries_query = enquiries_query.filter(
            (Enquiry.name.ilike(f'%{search_q}%')) |
            (Enquiry.email.ilike(f'%{search_q}%')) |
            (Enquiry.phone.ilike(f'%{search_q}%'))
        )

    if status_filter != 'ALL':
        trials_query = trials_query.filter_by(status=status_filter)
        consultations_query = consultations_query.filter_by(status=status_filter)
        enquiries_query = enquiries_query.filter_by(status=status_filter)

    trials = trials_query.order_by(TrialRequest.created_at.desc()).all() if lead_type in ['ALL', 'TRIAL'] else []
    consultations = consultations_query.order_by(Consultation.created_at.desc()).all() if lead_type in ['ALL', 'CONSULTATION'] else []
    enquiries = enquiries_query.order_by(Enquiry.created_at.desc()).all() if lead_type in ['ALL', 'ENQUIRY'] else []

    # Map notes
    all_notes = LeadNote.query.order_by(LeadNote.created_at.desc()).all()
    notes_by_lead = {}
    for note in all_notes:
        key = f"{note.lead_type}_{note.lead_id}"
        notes_by_lead.setdefault(key, []).append(note)

    note_form = LeadNoteForm()

    return render_template(
        'admin/leads.html',
        trials=trials,
        consultations=consultations,
        enquiries=enquiries,
        notes_by_lead=notes_by_lead,
        lead_type=lead_type,
        status_filter=status_filter,
        search_q=search_q,
        note_form=note_form
    )


@admin_bp.route('/leads/<lead_type>/<int:id>/status', methods=['POST'])
@login_required
def update_lead_status(lead_type, id):
    new_status = request.form.get('status')
    if lead_type == 'TRIAL':
        lead = TrialRequest.query.get_or_404(id)
    elif lead_type == 'CONSULTATION':
        lead = Consultation.query.get_or_404(id)
    elif lead_type == 'ENQUIRY':
        lead = Enquiry.query.get_or_404(id)
    else:
        abort(400)

    if new_status:
        lead.status = new_status
        db.session.commit()
        flash(f'Status for {lead.name} updated to {new_status}.', 'success')
    return redirect(request.referrer or url_for('admin.leads'))


@admin_bp.route('/leads/<lead_type>/<int:id>/note', methods=['POST'])
@login_required
def add_lead_note(lead_type, id):
    form = LeadNoteForm()
    if form.validate_on_submit():
        note = LeadNote(
            lead_type=lead_type.upper(),
            lead_id=id,
            note=form.note.data.strip(),
            author=current_user.username
        )
        db.session.add(note)
        db.session.commit()
        flash('Internal note added successfully.', 'success')
    return redirect(request.referrer or url_for('admin.leads'))


@admin_bp.route('/leads/<lead_type>/<int:id>/delete', methods=['POST'])
@login_required
def delete_lead(lead_type, id):
    if lead_type == 'TRIAL':
        lead = TrialRequest.query.get_or_404(id)
    elif lead_type == 'CONSULTATION':
        lead = Consultation.query.get_or_404(id)
    elif lead_type == 'ENQUIRY':
        lead = Enquiry.query.get_or_404(id)
    else:
        abort(400)

    # Remove attached notes
    LeadNote.query.filter_by(lead_type=lead_type.upper(), lead_id=id).delete()
    db.session.delete(lead)
    db.session.commit()
    flash(f'Lead for {lead.name} was removed.', 'info')
    return redirect(request.referrer or url_for('admin.leads'))


# ----------------------------------------------------
# 3. TRIAL REQUESTS
# ----------------------------------------------------
@admin_bp.route('/trials')
@login_required
def trials():
    status = request.args.get('status', 'ALL')
    query = TrialRequest.query
    if status != 'ALL':
        query = query.filter_by(status=status)
    trials_list = query.order_by(TrialRequest.created_at.desc()).all()
    return render_template('admin/trials.html', trials=trials_list, current_status=status)


@admin_bp.route('/trials/<int:id>/status', methods=['POST'])
@login_required
def trial_status(id):
    trial = TrialRequest.query.get_or_404(id)
    new_status = request.form.get('status')
    if new_status:
        trial.status = new_status
        db.session.commit()
        flash(f'Trial request for {trial.name} is now {new_status}.', 'success')
    return redirect(url_for('admin.trials'))


# ----------------------------------------------------
# 4. APPOINTMENT MANAGEMENT
# ----------------------------------------------------
@admin_bp.route('/appointments')
@login_required
def appointments():
    status = request.args.get('status', 'ALL')
    trainer_id = request.args.get('trainer_id', 'ALL')

    query = Consultation.query
    if status != 'ALL':
        query = query.filter_by(status=status)
    if trainer_id != 'ALL' and trainer_id.isdigit():
        query = query.filter_by(trainer_id=int(trainer_id))

    appointments_list = query.order_by(Consultation.created_at.desc()).all()
    trainers_list = Trainer.query.all()

    return render_template(
        'admin/appointments.html',
        appointments=appointments_list,
        trainers=trainers_list,
        current_status=status,
        current_trainer=trainer_id
    )


@admin_bp.route('/appointments/<int:id>/status', methods=['POST'])
@login_required
def appointment_status(id):
    appointment = Consultation.query.get_or_404(id)
    new_status = request.form.get('status')
    if new_status:
        appointment.status = new_status
        db.session.commit()
        flash(f'Appointment #{appointment.id} ({appointment.name}) updated to {new_status}.', 'success')
    return redirect(url_for('admin.appointments'))


# ----------------------------------------------------
# 5. MEMBERSHIP MANAGEMENT (CRUD)
# ----------------------------------------------------
@admin_bp.route('/memberships')
@login_required
def memberships():
    plans = MembershipPlan.query.order_by(MembershipPlan.price.asc()).all()
    return render_template('admin/memberships.html', plans=plans)


@admin_bp.route('/memberships/create', methods=['GET', 'POST'])
@login_required
def create_membership():
    form = MembershipPlanForm()
    if form.validate_on_submit():
        plan = MembershipPlan(
            name=form.name.data.strip(),
            price=form.price.data,
            duration=form.duration.data.strip(),
            description=form.description.data.strip() if form.description.data else None,
            features=form.features.data.strip(),
            featured=form.featured.data,
            is_active=form.is_active.data
        )
        db.session.add(plan)
        db.session.commit()
        flash(f'Membership plan "{plan.name}" created successfully.', 'success')
        return redirect(url_for('admin.memberships'))
    return render_template('admin/memberships.html', form=form, action='create', plans=MembershipPlan.query.all())


@admin_bp.route('/memberships/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_membership(id):
    plan = MembershipPlan.query.get_or_404(id)
    form = MembershipPlanForm(obj=plan)
    if form.validate_on_submit():
        plan.name = form.name.data.strip()
        plan.price = form.price.data
        plan.duration = form.duration.data.strip()
        plan.description = form.description.data.strip() if form.description.data else None
        plan.features = form.features.data.strip()
        plan.featured = form.featured.data
        plan.is_active = form.is_active.data
        db.session.commit()
        flash(f'Membership plan "{plan.name}" updated successfully.', 'success')
        return redirect(url_for('admin.memberships'))
    return render_template('admin/memberships.html', form=form, editing_plan=plan, action='edit', plans=MembershipPlan.query.all())


@admin_bp.route('/memberships/<int:id>/delete', methods=['POST'])
@login_required
def delete_membership(id):
    plan = MembershipPlan.query.get_or_404(id)
    db.session.delete(plan)
    db.session.commit()
    flash(f'Membership plan "{plan.name}" deleted.', 'info')
    return redirect(url_for('admin.memberships'))


# ----------------------------------------------------
# 6. TRAINER MANAGEMENT (CRUD)
# ----------------------------------------------------
@admin_bp.route('/trainers')
@login_required
def trainers():
    all_trainers = Trainer.query.order_by(Trainer.id.asc()).all()
    return render_template('admin/trainers.html', trainers=all_trainers)


@admin_bp.route('/trainers/create', methods=['GET', 'POST'])
@login_required
def create_trainer():
    form = TrainerForm()
    if form.validate_on_submit():
        trainer = Trainer(
            name=form.name.data.strip(),
            slug=form.slug.data.strip().lower(),
            specialization=form.specialization.data.strip(),
            experience=form.experience.data.strip() if form.experience.data else None,
            certifications=form.certifications.data.strip() if form.certifications.data else None,
            image_url=form.image_url.data.strip(),
            instagram_url=form.instagram_url.data.strip() if form.instagram_url.data else None,
            bio=form.bio.data.strip() if form.bio.data else None,
            is_featured=form.is_featured.data,
            is_active=form.is_active.data
        )
        db.session.add(trainer)
        db.session.commit()
        flash(f'Trainer "{trainer.name}" added to the roster.', 'success')
        return redirect(url_for('admin.trainers'))
    return render_template('admin/trainers.html', form=form, action='create', trainers=Trainer.query.all())


@admin_bp.route('/trainers/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_trainer(id):
    trainer = Trainer.query.get_or_404(id)
    form = TrainerForm(obj=trainer)
    if form.validate_on_submit():
        trainer.name = form.name.data.strip()
        trainer.slug = form.slug.data.strip().lower()
        trainer.specialization = form.specialization.data.strip()
        trainer.experience = form.experience.data.strip() if form.experience.data else None
        trainer.certifications = form.certifications.data.strip() if form.certifications.data else None
        trainer.image_url = form.image_url.data.strip()
        trainer.instagram_url = form.instagram_url.data.strip() if form.instagram_url.data else None
        trainer.bio = form.bio.data.strip() if form.bio.data else None
        trainer.is_featured = form.is_featured.data
        trainer.is_active = form.is_active.data
        db.session.commit()
        flash(f'Trainer "{trainer.name}" updated successfully.', 'success')
        return redirect(url_for('admin.trainers'))
    return render_template('admin/trainers.html', form=form, editing_trainer=trainer, action='edit', trainers=Trainer.query.all())


@admin_bp.route('/trainers/<int:id>/delete', methods=['POST'])
@login_required
def delete_trainer(id):
    trainer = Trainer.query.get_or_404(id)
    db.session.delete(trainer)
    db.session.commit()
    flash(f'Trainer "{trainer.name}" removed.', 'info')
    return redirect(url_for('admin.trainers'))


# ----------------------------------------------------
# 7. CLASS MANAGEMENT (CRUD)
# ----------------------------------------------------
@admin_bp.route('/classes')
@login_required
def classes():
    classes_list = GymClass.query.order_by(GymClass.day, GymClass.start_time).all()
    return render_template('admin/classes.html', classes=classes_list)


@admin_bp.route('/classes/create', methods=['GET', 'POST'])
@login_required
def create_class():
    form = GymClassForm()
    trainers = Trainer.query.filter_by(is_active=True).all()
    form.trainer_id.choices = [(0, '-- Unassigned / Open Class --')] + [(t.id, t.name) for t in trainers]

    if form.validate_on_submit():
        gym_class = GymClass(
            name=form.name.data.strip(),
            trainer_id=form.trainer_id.data if form.trainer_id.data != 0 else None,
            day=form.day.data,
            start_time=form.start_time.data.strip(),
            end_time=form.end_time.data.strip(),
            capacity=form.capacity.data,
            description=form.description.data.strip() if form.description.data else None,
            is_active=form.is_active.data
        )
        db.session.add(gym_class)
        db.session.commit()
        flash(f'Class "{gym_class.name}" added to timetable.', 'success')
        return redirect(url_for('admin.classes'))
    return render_template('admin/classes.html', form=form, action='create', classes=GymClass.query.all())


@admin_bp.route('/classes/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_class(id):
    gym_class = GymClass.query.get_or_404(id)
    form = GymClassForm(obj=gym_class)
    trainers = Trainer.query.filter_by(is_active=True).all()
    form.trainer_id.choices = [(0, '-- Unassigned / Open Class --')] + [(t.id, t.name) for t in trainers]
    if request.method == 'GET' and gym_class.trainer_id is None:
        form.trainer_id.data = 0

    if form.validate_on_submit():
        gym_class.name = form.name.data.strip()
        gym_class.trainer_id = form.trainer_id.data if form.trainer_id.data != 0 else None
        gym_class.day = form.day.data
        gym_class.start_time = form.start_time.data.strip()
        gym_class.end_time = form.end_time.data.strip()
        gym_class.capacity = form.capacity.data
        gym_class.description = form.description.data.strip() if form.description.data else None
        gym_class.is_active = form.is_active.data
        db.session.commit()
        flash(f'Class "{gym_class.name}" updated successfully.', 'success')
        return redirect(url_for('admin.classes'))
    return render_template('admin/classes.html', form=form, editing_class=gym_class, action='edit', classes=GymClass.query.all())


@admin_bp.route('/classes/<int:id>/delete', methods=['POST'])
@login_required
def delete_class(id):
    gym_class = GymClass.query.get_or_404(id)
    db.session.delete(gym_class)
    db.session.commit()
    flash(f'Class "{gym_class.name}" removed.', 'info')
    return redirect(url_for('admin.classes'))


# ----------------------------------------------------
# 8. FACILITIES & GALLERY (CRUD)
# ----------------------------------------------------
@admin_bp.route('/facilities')
@login_required
def facilities():
    facilities_list = Facility.query.order_by(Facility.display_order.asc()).all()
    return render_template('admin/facilities.html', facilities=facilities_list)


@admin_bp.route('/facilities/create', methods=['GET', 'POST'])
@login_required
def create_facility():
    form = FacilityForm()
    if form.validate_on_submit():
        facility = Facility(
            name=form.name.data.strip(),
            category=form.category.data.strip(),
            description=form.description.data.strip() if form.description.data else None,
            image_url=form.image_url.data.strip(),
            display_order=form.display_order.data,
            is_active=form.is_active.data
        )
        db.session.add(facility)
        db.session.commit()
        flash(f'Facility "{facility.name}" created.', 'success')
        return redirect(url_for('admin.facilities'))
    return render_template('admin/facilities.html', form=form, action='create', facilities=Facility.query.all())


@admin_bp.route('/facilities/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_facility(id):
    facility = Facility.query.get_or_404(id)
    form = FacilityForm(obj=facility)
    if form.validate_on_submit():
        facility.name = form.name.data.strip()
        facility.category = form.category.data.strip()
        facility.description = form.description.data.strip() if form.description.data else None
        facility.image_url = form.image_url.data.strip()
        facility.display_order = form.display_order.data
        facility.is_active = form.is_active.data
        db.session.commit()
        flash(f'Facility "{facility.name}" updated.', 'success')
        return redirect(url_for('admin.facilities'))
    return render_template('admin/facilities.html', form=form, editing_facility=facility, action='edit', facilities=Facility.query.all())


@admin_bp.route('/facilities/<int:id>/delete', methods=['POST'])
@login_required
def delete_facility(id):
    facility = Facility.query.get_or_404(id)
    db.session.delete(facility)
    db.session.commit()
    flash(f'Facility "{facility.name}" removed.', 'info')
    return redirect(url_for('admin.facilities'))


# ----------------------------------------------------
# 9. TRANSFORMATIONS (CRUD)
# ----------------------------------------------------
@admin_bp.route('/transformations')
@login_required
def transformations():
    transformations_list = Transformation.query.order_by(Transformation.created_at.desc()).all()
    return render_template('admin/transformations.html', transformations=transformations_list)


@admin_bp.route('/transformations/create', methods=['GET', 'POST'])
@login_required
def create_transformation():
    form = TransformationForm()
    if form.validate_on_submit():
        transformation = Transformation(
            client_name=form.client_name.data.strip(),
            before_image=form.before_image.data.strip(),
            after_image=form.after_image.data.strip(),
            duration=form.duration.data.strip(),
            achievement=form.achievement.data.strip(),
            story=form.story.data.strip() if form.story.data else None,
            is_featured=form.is_featured.data,
            is_active=form.is_active.data
        )
        db.session.add(transformation)
        db.session.commit()
        flash(f'Transformation for {transformation.client_name} added.', 'success')
        return redirect(url_for('admin.transformations'))
    return render_template('admin/transformations.html', form=form, action='create', transformations=Transformation.query.all())


@admin_bp.route('/transformations/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_transformation(id):
    transformation = Transformation.query.get_or_404(id)
    form = TransformationForm(obj=transformation)
    if form.validate_on_submit():
        transformation.client_name = form.client_name.data.strip()
        transformation.before_image = form.before_image.data.strip()
        transformation.after_image = form.after_image.data.strip()
        transformation.duration = form.duration.data.strip()
        transformation.achievement = form.achievement.data.strip()
        transformation.story = form.story.data.strip() if form.story.data else None
        transformation.is_featured = form.is_featured.data
        transformation.is_active = form.is_active.data
        db.session.commit()
        flash(f'Transformation for {transformation.client_name} updated.', 'success')
        return redirect(url_for('admin.transformations'))
    return render_template('admin/transformations.html', form=form, editing_transformation=transformation, action='edit', transformations=Transformation.query.all())


@admin_bp.route('/transformations/<int:id>/delete', methods=['POST'])
@login_required
def delete_transformation(id):
    transformation = Transformation.query.get_or_404(id)
    db.session.delete(transformation)
    db.session.commit()
    flash(f'Transformation for {transformation.client_name} removed.', 'info')
    return redirect(url_for('admin.transformations'))


# ----------------------------------------------------
# 10. TESTIMONIALS (CRUD)
# ----------------------------------------------------
@admin_bp.route('/testimonials')
@login_required
def testimonials():
    testimonials_list = Testimonial.query.order_by(Testimonial.created_at.desc()).all()
    return render_template('admin/testimonials.html', testimonials=testimonials_list)


@admin_bp.route('/testimonials/create', methods=['GET', 'POST'])
@login_required
def create_testimonial():
    form = TestimonialForm()
    if form.validate_on_submit():
        testimonial = Testimonial(
            client_name=form.client_name.data.strip(),
            rating=form.rating.data,
            review=form.review.data.strip(),
            image_url=form.image_url.data.strip() if form.image_url.data else None,
            is_featured=form.is_featured.data
        )
        db.session.add(testimonial)
        db.session.commit()
        flash(f'Testimonial from {testimonial.client_name} added.', 'success')
        return redirect(url_for('admin.testimonials'))
    return render_template('admin/testimonials.html', form=form, action='create', testimonials=Testimonial.query.all())


@admin_bp.route('/testimonials/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_testimonial(id):
    testimonial = Testimonial.query.get_or_404(id)
    form = TestimonialForm(obj=testimonial)
    if form.validate_on_submit():
        testimonial.client_name = form.client_name.data.strip()
        testimonial.rating = form.rating.data
        testimonial.review = form.review.data.strip()
        testimonial.image_url = form.image_url.data.strip() if form.image_url.data else None
        testimonial.is_featured = form.is_featured.data
        db.session.commit()
        flash(f'Testimonial from {testimonial.client_name} updated.', 'success')
        return redirect(url_for('admin.testimonials'))
    return render_template('admin/testimonials.html', form=form, editing_testimonial=testimonial, action='edit', testimonials=Testimonial.query.all())


@admin_bp.route('/testimonials/<int:id>/delete', methods=['POST'])
@login_required
def delete_testimonial(id):
    testimonial = Testimonial.query.get_or_404(id)
    db.session.delete(testimonial)
    db.session.commit()
    flash(f'Testimonial from {testimonial.client_name} removed.', 'info')
    return redirect(url_for('admin.testimonials'))


# ----------------------------------------------------
# 11. INSTAGRAM / REELS MANAGEMENT (CRUD)
# ----------------------------------------------------
@admin_bp.route('/instagram')
@login_required
def instagram():
    reels_list = InstagramReel.query.order_by(InstagramReel.display_order.asc()).all()
    return render_template('admin/instagram.html', reels=reels_list)


@admin_bp.route('/instagram/create', methods=['GET', 'POST'])
@login_required
def create_reel():
    form = InstagramReelForm()
    if form.validate_on_submit():
        reel = InstagramReel(
            title=form.title.data.strip(),
            caption=form.caption.data.strip() if form.caption.data else None,
            instagram_url=form.instagram_url.data.strip() if form.instagram_url.data else None,
            thumbnail_url=form.thumbnail_url.data.strip(),
            video_url=form.video_url.data.strip() if form.video_url.data else None,
            display_order=form.display_order.data,
            is_featured=form.is_featured.data,
            is_active=form.is_active.data
        )
        db.session.add(reel)
        db.session.commit()
        flash(f'Instagram Reel "{reel.title}" created.', 'success')
        return redirect(url_for('admin.instagram'))
    return render_template('admin/instagram.html', form=form, action='create', reels=InstagramReel.query.all())


@admin_bp.route('/instagram/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_reel(id):
    reel = InstagramReel.query.get_or_404(id)
    form = InstagramReelForm(obj=reel)
    if form.validate_on_submit():
        reel.title = form.title.data.strip()
        reel.caption = form.caption.data.strip() if form.caption.data else None
        reel.instagram_url = form.instagram_url.data.strip() if form.instagram_url.data else None
        reel.thumbnail_url = form.thumbnail_url.data.strip()
        reel.video_url = form.video_url.data.strip() if form.video_url.data else None
        reel.display_order = form.display_order.data
        reel.is_featured = form.is_featured.data
        reel.is_active = form.is_active.data
        db.session.commit()
        flash(f'Instagram Reel "{reel.title}" updated.', 'success')
        return redirect(url_for('admin.instagram'))
    return render_template('admin/instagram.html', form=form, editing_reel=reel, action='edit', reels=InstagramReel.query.all())


@admin_bp.route('/instagram/<int:id>/delete', methods=['POST'])
@login_required
def delete_reel(id):
    reel = InstagramReel.query.get_or_404(id)
    db.session.delete(reel)
    db.session.commit()
    flash(f'Instagram Reel "{reel.title}" deleted.', 'info')
    return redirect(url_for('admin.instagram'))
