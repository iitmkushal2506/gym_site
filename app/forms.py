from flask_wtf import FlaskForm
from wtforms import (
    StringField, PasswordField, BooleanField, SubmitField, TextAreaField,
    FloatField, IntegerField, SelectField, EmailField, TelField
)
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange, URL


class AdminLoginForm(FlaskForm):
    username = StringField('Username or Email', validators=[DataRequired(), Length(min=3, max=80)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In to Dashboard')


class TrialBookingForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Email Address', validators=[DataRequired(), Email()])
    phone = TelField('Phone Number', validators=[DataRequired(), Length(min=8, max=20)])
    age = IntegerField('Age', validators=[Optional(), NumberRange(min=14, max=99)])
    fitness_goal = SelectField('Primary Fitness Goal', choices=[
        ('Weight Loss & Fat Burn', 'Weight Loss & Fat Burn'),
        ('Muscle Gain & Hypertrophy', 'Muscle Gain & Hypertrophy'),
        ('Strength & Powerlifting', 'Strength & Powerlifting'),
        ('Endurance & Functional Fitness', 'Endurance & Functional Fitness'),
        ('General Health & Flexibility', 'General Health & Flexibility'),
        ('Other', 'Other')
    ], validators=[DataRequired()])
    preferred_date = StringField('Preferred Date', validators=[DataRequired()])
    preferred_time = SelectField('Preferred Time Slot', choices=[
        ('06:00 AM - 08:00 AM (Early Bird)', '06:00 AM - 08:00 AM (Early Bird)'),
        ('08:00 AM - 10:00 AM (Morning Peak)', '08:00 AM - 10:00 AM (Morning Peak)'),
        ('10:00 AM - 12:00 PM (Midday)', '10:00 AM - 12:00 PM (Midday)'),
        ('04:00 PM - 06:00 PM (Evening Power)', '04:00 PM - 06:00 PM (Evening Power)'),
        ('06:00 PM - 08:00 PM (Prime Hours)', '06:00 PM - 08:00 PM (Prime Hours)'),
        ('08:00 PM - 10:00 PM (Night Owls)', '08:00 PM - 10:00 PM (Night Owls)')
    ], validators=[DataRequired()])
    message = TextAreaField('Additional Notes / Medical Conditions (Optional)', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Claim My Free Trial Pass')


class ConsultationBookingForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Email Address', validators=[DataRequired(), Email()])
    phone = TelField('Phone Number', validators=[DataRequired(), Length(min=8, max=20)])
    trainer_id = SelectField('Select Preferred Coach', coerce=int, validators=[DataRequired()])
    goal = SelectField('Training Focus', choices=[
        ('1-on-1 Personal Training', '1-on-1 Personal Training'),
        ('Custom Diet & Nutrition Strategy', 'Custom Diet & Nutrition Strategy'),
        ('Body Transformation Program', 'Body Transformation Program'),
        ('Athletic Performance & Conditioning', 'Athletic Performance & Conditioning'),
        ('Injury Rehab & Mobility', 'Injury Rehab & Mobility')
    ], validators=[DataRequired()])
    fitness_level = SelectField('Current Fitness Experience', choices=[
        ('Beginner (Just getting started)', 'Beginner (Just getting started)'),
        ('Intermediate (1-2 years consistent)', 'Intermediate (1-2 years consistent)'),
        ('Advanced (3+ years serious lifting)', 'Advanced (3+ years serious lifting)')
    ], validators=[DataRequired()])
    preferred_date = StringField('Preferred Date', validators=[DataRequired()])
    preferred_time = SelectField('Preferred Time Slot', choices=[
        ('07:00 AM', '07:00 AM'),
        ('09:00 AM', '09:00 AM'),
        ('11:00 AM', '11:00 AM'),
        ('04:00 PM', '04:00 PM'),
        ('06:00 PM', '06:00 PM'),
        ('07:30 PM', '07:30 PM')
    ], validators=[DataRequired()])
    message = TextAreaField('Tell us about your fitness targets & history', validators=[Optional(), Length(max=600)])
    submit = SubmitField('Request Consultation')


class ContactEnquiryForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = EmailField('Email Address', validators=[DataRequired(), Email()])
    phone = TelField('Phone Number', validators=[DataRequired(), Length(min=8, max=20)])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=3, max=150)])
    message = TextAreaField('Your Message', validators=[DataRequired(), Length(min=10, max=1000)])
    submit = SubmitField('Send Enquiry')


class MembershipPlanForm(FlaskForm):
    name = StringField('Plan Name', validators=[DataRequired(), Length(max=100)])
    price = FloatField('Monthly / Period Price (₹)', validators=[DataRequired(), NumberRange(min=0)])
    duration = StringField('Billing Cycle / Duration', default='month', validators=[DataRequired(), Length(max=50)])
    description = TextAreaField('Short Summary', validators=[Optional()])
    features = TextAreaField('Features (1 per line)', validators=[DataRequired()])
    featured = BooleanField('Highlight as Most Popular')
    is_active = BooleanField('Active & Visible to Public', default=True)
    submit = SubmitField('Save Membership Plan')


class TrainerForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(max=100)])
    slug = StringField('URL Slug (e.g. marcus-vance)', validators=[DataRequired(), Length(max=120)])
    specialization = StringField('Primary Specialization', validators=[DataRequired(), Length(max=150)])
    experience = StringField('Experience (e.g. 8+ Years)', validators=[Optional(), Length(max=50)])
    certifications = TextAreaField('Certifications (1 per line)', validators=[Optional()])
    image_url = StringField('Profile Photo URL', validators=[DataRequired(), Length(max=255)])
    instagram_url = StringField('Instagram Profile URL', validators=[Optional(), Length(max=255)])
    bio = TextAreaField('Biography & Training Philosophy', validators=[Optional()])
    is_featured = BooleanField('Feature on Homepage')
    is_active = BooleanField('Active Roster', default=True)
    submit = SubmitField('Save Trainer')


class GymClassForm(FlaskForm):
    name = StringField('Class Title', validators=[DataRequired(), Length(max=100)])
    trainer_id = SelectField('Assigned Trainer', coerce=int, validators=[Optional()])
    day = SelectField('Day of Week', choices=[
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday')
    ], validators=[DataRequired()])
    start_time = StringField('Start Time (e.g. 06:00 AM)', validators=[DataRequired(), Length(max=20)])
    end_time = StringField('End Time (e.g. 07:00 AM)', validators=[DataRequired(), Length(max=20)])
    capacity = IntegerField('Max Capacity', default=20, validators=[DataRequired(), NumberRange(min=1, max=100)])
    description = TextAreaField('Class Description & Intensity', validators=[Optional()])
    is_active = BooleanField('Active in Timetable', default=True)
    submit = SubmitField('Save Class')


class FacilityForm(FlaskForm):
    name = StringField('Facility Name', validators=[DataRequired(), Length(max=100)])
    category = StringField('Zone / Category (e.g. Strength, Recovery)', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Highlights & Equipment Specs', validators=[Optional()])
    image_url = StringField('High-Res Image URL', validators=[DataRequired(), Length(max=255)])
    display_order = IntegerField('Display Order', default=0, validators=[DataRequired()])
    is_active = BooleanField('Active & Published', default=True)
    submit = SubmitField('Save Facility')


class TransformationForm(FlaskForm):
    client_name = StringField('Client Name / Alias', validators=[DataRequired(), Length(max=100)])
    before_image = StringField('Before Photo URL', validators=[DataRequired(), Length(max=255)])
    after_image = StringField('After Photo URL', validators=[DataRequired(), Length(max=255)])
    duration = StringField('Timeline (e.g. 4 Months)', validators=[DataRequired(), Length(max=50)])
    achievement = StringField('Headline Achievement (e.g. Lost 14kg & Built Muscle)', validators=[DataRequired(), Length(max=100)])
    story = TextAreaField('Client Journey & Quote', validators=[Optional()])
    is_featured = BooleanField('Feature on Homepage', default=True)
    is_active = BooleanField('Active & Published', default=True)
    submit = SubmitField('Save Transformation')


class TestimonialForm(FlaskForm):
    client_name = StringField('Member Name', validators=[DataRequired(), Length(max=100)])
    rating = IntegerField('Rating (1-5 Stars)', default=5, validators=[DataRequired(), NumberRange(min=1, max=5)])
    review = TextAreaField('Testimonial / Review Text', validators=[DataRequired()])
    image_url = StringField('Avatar Photo URL (Optional)', validators=[Optional(), Length(max=255)])
    is_featured = BooleanField('Feature on Homepage', default=True)
    submit = SubmitField('Save Testimonial')


class InstagramReelForm(FlaskForm):
    title = StringField('Reel Title / Focus', validators=[DataRequired(), Length(max=120)])
    caption = TextAreaField('Caption / Description', validators=[Optional()])
    instagram_url = StringField('Instagram Reel Post Link', validators=[Optional(), Length(max=255)])
    thumbnail_url = StringField('Vertical Thumbnail (9:16) URL', validators=[DataRequired(), Length(max=255)])
    video_url = StringField('Demo Video Direct URL (MP4 / WebM)', validators=[Optional(), Length(max=255)])
    display_order = IntegerField('Display Order', default=0, validators=[DataRequired()])
    is_featured = BooleanField('Feature on Homepage', default=True)
    is_active = BooleanField('Active & Visible', default=True)
    submit = SubmitField('Save Instagram Reel')


class LeadNoteForm(FlaskForm):
    note = TextAreaField('Internal Follow-Up Note', validators=[DataRequired(), Length(min=2, max=1000)])
    submit = SubmitField('Add Note')
