from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.extensions import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return Admin.query.get(int(user_id))


class Admin(UserMixin, db.Model):
    __tablename__ = 'admins'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<Admin {self.username}>'


class MembershipPlan(db.Model):
    __tablename__ = 'membership_plans'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    duration = db.Column(db.String(50), default='month', nullable=False)  # e.g., 'month', '3 months', 'year'
    description = db.Column(db.Text, nullable=True)
    features = db.Column(db.Text, nullable=False)  # Stored as newline or pipe separated features
    featured = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def feature_list(self):
        if not self.features:
            return []
        # Support both newline and semicolon/pipe split
        lines = [f.strip() for f in self.features.replace(';', '\n').replace('|', '\n').split('\n') if f.strip()]
        return lines

    def __repr__(self):
        return f'<MembershipPlan {self.name}>'


class Trainer(db.Model):
    __tablename__ = 'trainers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False, index=True)
    bio = db.Column(db.Text, nullable=True)
    experience = db.Column(db.String(50), nullable=True)  # e.g. "8+ Years"
    specialization = db.Column(db.String(150), nullable=False)
    certifications = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    instagram_url = db.Column(db.String(255), nullable=True)
    is_featured = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    classes = db.relationship('GymClass', backref='trainer', lazy=True, cascade='all, delete-orphan')
    consultations = db.relationship('Consultation', backref='trainer', lazy=True)

    @property
    def cert_list(self):
        if not self.certifications:
            return []
        return [c.strip() for c in self.certifications.replace(';', '\n').replace('|', '\n').split('\n') if c.strip()]

    def __repr__(self):
        return f'<Trainer {self.name}>'


class GymClass(db.Model):
    __tablename__ = 'gym_classes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainers.id'), nullable=True)
    day = db.Column(db.String(20), nullable=False)  # e.g., Monday, Tuesday, etc.
    start_time = db.Column(db.String(20), nullable=False)  # e.g., "06:00 AM"
    end_time = db.Column(db.String(20), nullable=False)    # e.g., "07:00 AM"
    capacity = db.Column(db.Integer, default=20)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<GymClass {self.name} - {self.day}>'


class Facility(db.Model):
    __tablename__ = 'facilities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), default='General')
    description = db.Column(db.Text, nullable=True)
    image_url = db.Column(db.String(255), nullable=False)
    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Facility {self.name}>'


class GalleryImage(db.Model):
    __tablename__ = 'gallery_images'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=True)
    category = db.Column(db.String(50), default='Facility')
    image_url = db.Column(db.String(255), nullable=False)
    display_order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Transformation(db.Model):
    __tablename__ = 'transformations'

    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    before_image = db.Column(db.String(255), nullable=False)
    after_image = db.Column(db.String(255), nullable=False)
    duration = db.Column(db.String(50), nullable=False)  # e.g., "4 Months"
    achievement = db.Column(db.String(100), nullable=False)  # e.g., "Lost 14 kg & Built Lean Muscle"
    story = db.Column(db.Text, nullable=True)
    is_featured = db.Column(db.Boolean, default=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Transformation {self.client_name}>'


class Testimonial(db.Model):
    __tablename__ = 'testimonials'

    id = db.Column(db.Integer, primary_key=True)
    client_name = db.Column(db.String(100), nullable=False)
    review = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, default=5)
    image_url = db.Column(db.String(255), nullable=True)
    is_featured = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Testimonial {self.client_name}>'


class TrialRequest(db.Model):
    __tablename__ = 'trial_requests'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, index=True)
    phone = db.Column(db.String(30), nullable=False, index=True)
    age = db.Column(db.Integer, nullable=True)
    fitness_goal = db.Column(db.String(100), nullable=False)  # Weight Loss, Muscle Gain, Strength, etc.
    preferred_date = db.Column(db.String(30), nullable=False)  # e.g., "YYYY-MM-DD"
    preferred_time = db.Column(db.String(30), nullable=False)  # e.g., "06:00 AM - 08:00 AM"
    message = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(30), default='NEW', nullable=False)  # NEW, CONTACTED, CONFIRMED, COMPLETED, CANCELLED
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<TrialRequest {self.name} - {self.status}>'


class Consultation(db.Model):
    __tablename__ = 'consultations'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, index=True)
    phone = db.Column(db.String(30), nullable=False, index=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('trainers.id'), nullable=False)
    goal = db.Column(db.String(100), nullable=False)
    fitness_level = db.Column(db.String(50), nullable=False)  # Beginner, Intermediate, Advanced
    preferred_date = db.Column(db.String(30), nullable=False)  # "YYYY-MM-DD"
    preferred_time = db.Column(db.String(30), nullable=False)  # "10:00 AM", "05:00 PM"
    message = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(30), default='PENDING', nullable=False)  # PENDING, CONFIRMED, COMPLETED, CANCELLED
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Consultation {self.name} with Trainer #{self.trainer_id}>'


class Enquiry(db.Model):
    __tablename__ = 'enquiries'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, index=True)
    phone = db.Column(db.String(30), nullable=False)
    subject = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(30), default='NEW', nullable=False)  # NEW, IN_PROGRESS, RESOLVED, CLOSED
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Enquiry {self.name} - {self.subject}>'


class LeadNote(db.Model):
    __tablename__ = 'lead_notes'

    id = db.Column(db.Integer, primary_key=True)
    lead_type = db.Column(db.String(20), nullable=False)  # 'TRIAL', 'CONSULTATION', 'ENQUIRY'
    lead_id = db.Column(db.Integer, nullable=False)
    note = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(80), default='Admin')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<LeadNote on {self.lead_type} #{self.lead_id}>'


class InstagramReel(db.Model):
    __tablename__ = 'instagram_reels'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    caption = db.Column(db.Text, nullable=True)
    instagram_url = db.Column(db.String(255), nullable=True)
    thumbnail_url = db.Column(db.String(255), nullable=False)
    video_url = db.Column(db.String(255), nullable=True)
    display_order = db.Column(db.Integer, default=0)
    is_featured = db.Column(db.Boolean, default=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<InstagramReel {self.title}>'
