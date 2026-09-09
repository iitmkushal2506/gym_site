from flask import Blueprint, render_template, make_response, current_app, abort
from app.models import (
    MembershipPlan, Trainer, GymClass, Facility, GalleryImage,
    Transformation, Testimonial, InstagramReel
)

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    featured_plans = MembershipPlan.query.filter_by(is_active=True).order_by(MembershipPlan.price.asc()).limit(3).all()
    featured_trainers = Trainer.query.filter_by(is_active=True, is_featured=True).limit(4).all()
    if not featured_trainers:
        featured_trainers = Trainer.query.filter_by(is_active=True).limit(4).all()
        
    classes_preview = GymClass.query.filter_by(is_active=True).limit(6).all()
    facilities_preview = Facility.query.filter_by(is_active=True).order_by(Facility.display_order.asc()).limit(6).all()
    transformations = Transformation.query.filter_by(is_active=True, is_featured=True).limit(4).all()
    testimonials = Testimonial.query.filter_by(is_featured=True).limit(6).all()
    reels = InstagramReel.query.filter_by(is_active=True).order_by(InstagramReel.display_order.asc()).limit(6).all()

    return render_template(
        'home.html',
        plans=featured_plans,
        trainers=featured_trainers,
        classes=classes_preview,
        facilities=facilities_preview,
        transformations=transformations,
        testimonials=testimonials,
        reels=reels
    )


@main_bp.route('/about')
def about():
    trainers_preview = Trainer.query.filter_by(is_active=True).limit(3).all()
    testimonials = Testimonial.query.filter_by(is_featured=True).limit(3).all()
    return render_template('about.html', trainers=trainers_preview, testimonials=testimonials)


@main_bp.route('/membership')
def membership():
    plans = MembershipPlan.query.filter_by(is_active=True).order_by(MembershipPlan.price.asc()).all()
    return render_template('membership.html', plans=plans)


@main_bp.route('/trainers')
def trainers():
    all_trainers = Trainer.query.filter_by(is_active=True).all()
    specializations = list(set([t.specialization for t in all_trainers if t.specialization]))
    return render_template('trainers.html', trainers=all_trainers, specializations=specializations)


@main_bp.route('/trainers/<slug>')
def trainer_detail(slug):
    trainer = Trainer.query.filter_by(slug=slug, is_active=True).first_or_404()
    trainer_classes = GymClass.query.filter_by(trainer_id=trainer.id, is_active=True).all()
    return render_template('trainer_detail.html', trainer=trainer, classes=trainer_classes)


@main_bp.route('/classes')
def classes():
    all_classes = GymClass.query.filter_by(is_active=True).order_by(GymClass.day, GymClass.start_time).all()
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Group classes by day
    schedule_by_day = {day: [] for day in days}
    for c in all_classes:
        if c.day in schedule_by_day:
            schedule_by_day[c.day].append(c)
            
    return render_template('classes.html', schedule=schedule_by_day, days=days, all_classes=all_classes)


@main_bp.route('/facilities')
def facilities():
    all_facilities = Facility.query.filter_by(is_active=True).order_by(Facility.display_order.asc()).all()
    categories = sorted(list(set([f.category for f in all_facilities if f.category])))
    gallery = GalleryImage.query.filter_by(is_active=True).order_by(GalleryImage.display_order.asc()).all()
    return render_template('facilities.html', facilities=all_facilities, categories=categories, gallery=gallery)


@main_bp.route('/transformations')
def transformations():
    all_transformations = Transformation.query.filter_by(is_active=True).all()
    return render_template('transformations.html', transformations=all_transformations)


@main_bp.route('/robots.txt')
def robots_txt():
    content = "User-agent: *\nAllow: /\nDisallow: /admin/\nSitemap: /sitemap.xml\n"
    response = make_response(content, 200)
    response.mimetype = "text/plain"
    return response


@main_bp.route('/sitemap.xml')
def sitemap_xml():
    pages = [
        {'loc': '/', 'priority': '1.0'},
        {'loc': '/about', 'priority': '0.8'},
        {'loc': '/membership', 'priority': '0.9'},
        {'loc': '/trainers', 'priority': '0.9'},
        {'loc': '/classes', 'priority': '0.8'},
        {'loc': '/facilities', 'priority': '0.8'},
        {'loc': '/transformations', 'priority': '0.8'},
        {'loc': '/contact', 'priority': '0.7'},
        {'loc': '/book-trial', 'priority': '0.9'},
        {'loc': '/book-consultation', 'priority': '0.9'},
    ]
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    for page in pages:
        xml += f"  <url>\n    <loc>{page['loc']}</loc>\n    <priority>{page['priority']}</priority>\n  </url>\n"
    xml += '</urlset>'
    response = make_response(xml, 200)
    response.mimetype = "application/xml"
    return response
