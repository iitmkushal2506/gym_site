import os
from app import create_app
from app.extensions import db
from app.models import (
    Admin, MembershipPlan, Trainer, GymClass, Facility, GalleryImage,
    Transformation, Testimonial, TrialRequest, Consultation, Enquiry,
    LeadNote, InstagramReel
)

def seed_database():
    app = create_app('development')
    with app.app_context():
        # Create all database tables
        db.create_all()

        # 1. Seed Admin Account
        admin = Admin.query.filter_by(username='admin').first()
        if not admin:
            admin = Admin(
                username='admin',
                email='admin@kushalgym.demo'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            print("Created default admin user: admin / admin123")

        # 2. Seed Membership Plans
        if MembershipPlan.query.count() == 0:
            plans = [
                MembershipPlan(
                    name="BASIC ATHLETE",
                    price=1499.0,
                    duration="month",
                    description="Essential gym & strength floor access for dedicated lifters.",
                    features="Full strength & cardio floor access\nCalibrated plates & barbell zones\nLocker room & shower access\n1 Complimentary InBody scan per month\nAccess during all standard hours",
                    featured=False,
                    is_active=True
                ),
                MembershipPlan(
                    name="PREMIUM ALL-ACCESS",
                    price=2499.0,
                    duration="month",
                    description="Our most popular membership with unlimited group classes and diet strategy.",
                    features="Everything in Basic Athlete tier\nUnlimited group classes (HIIT, Boxing, Yoga)\nMonthly coach fitness assessment\nCustomized macro & nutrition guide\nExecutive towel & locker service\n2 Complimentary VIP guest passes per month",
                    featured=True,
                    is_active=True
                ),
                MembershipPlan(
                    name="ELITE PERFORMANCE",
                    price=4999.0,
                    duration="month",
                    description="The ultimate transformation package with dedicated 1-on-1 coaching.",
                    features="Everything in Premium All-Access tier\n4 Monthly 1-on-1 Personal Training sessions\nCustomized periodization program\nWeekly 1-on-1 nutrition review\nInfrared sauna & recovery suite access\nPriority class & trainer booking\nComplimentary daily protein smoothie",
                    featured=False,
                    is_active=True
                )
            ]
            db.session.add_all(plans)
            print("Seeded 3 membership plans.")

        # 3. Seed Trainers
        if Trainer.query.count() == 0:
            trainers = [
                Trainer(
                    name="Marcus Vance",
                    slug="marcus-vance",
                    specialization="Powerlifting & Hypertrophy",
                    experience="10+ Years",
                    certifications="CSCS Certified Strength Specialist\nUSAW Level 2 Weightlifting Coach\nISSA Master Bodybuilding Coach",
                    image_url="https://images.unsplash.com/photo-1567013127542-490d757e51fc?q=80&w=800&auto=format&fit=crop",
                    instagram_url="https://instagram.com/ironforgefitness",
                    bio="Former competitive powerlifter specialized in biomechanical barbell optimization, progressive overload programming, and maximum lean muscle hypertrophy.",
                    is_featured=True,
                    is_active=True
                ),
                Trainer(
                    name="Elena Rostova",
                    slug="elena-rostova",
                    specialization="HIIT, Functional Turf & Athletics",
                    experience="7+ Years",
                    certifications="NASM Certified Personal Trainer\nEXOS Performance Specialist\nKettlebell Athletics Level 2",
                    image_url="https://images.unsplash.com/photo-1594381898411-846e7d193883?q=80&w=800&auto=format&fit=crop",
                    instagram_url="https://instagram.com/ironforgefitness",
                    bio="High-performance conditioning specialist focused on explosive metabolic conditioning, athletic agility, and rapid fat loss protocols.",
                    is_featured=True,
                    is_active=True
                ),
                Trainer(
                    name="Jaxson Cole",
                    slug="jaxson-cole",
                    specialization="Boxing, Strength & Combat Fitness",
                    experience="8+ Years",
                    certifications="USA Boxing Certified Coach\nACE Certified Master Trainer\nFMS Functional Movement Level 1",
                    image_url="https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?q=80&w=800&auto=format&fit=crop",
                    instagram_url="https://instagram.com/ironforgefitness",
                    bio="Combines fight-camp conditioning with compound resistance training to build relentless cardiovascular stamina and explosive punching power.",
                    is_featured=True,
                    is_active=True
                ),
                Trainer(
                    name="Priya Sharma",
                    slug="priya-sharma",
                    specialization="Mobility, Yoga & Rehab",
                    experience="6+ Years",
                    certifications="500-Hour RYT Master Instructor\nNASM Corrective Exercise Specialist (CES)\nFunctional Range Conditioning (FRC)",
                    image_url="https://images.unsplash.com/photo-1518611012118-696072aa579a?q=80&w=800&auto=format&fit=crop",
                    instagram_url="https://instagram.com/ironforgefitness",
                    bio="Passionate about bulletproofing joints, unlocking functional mobility, and accelerating central nervous system recovery through breathwork and movement flows.",
                    is_featured=True,
                    is_active=True
                ),
                Trainer(
                    name="Viktor Lindqvist",
                    slug="viktor-lindqvist",
                    specialization="Olympic Lifting & Strongman",
                    experience="9+ Years",
                    certifications="IWF Olympic Lifting Master\nCSCS Strength Coach\nPrecision Nutrition Level 1",
                    image_url="https://images.unsplash.com/photo-1534367507873-d2d7e24c797f?q=80&w=800&auto=format&fit=crop",
                    instagram_url="https://instagram.com/ironforgefitness",
                    bio="Olympic snatch and clean-and-jerk specialist dedicated to building raw explosive power, kinetic chain alignment, and athlete mindset.",
                    is_featured=False,
                    is_active=True
                )
            ]
            db.session.add_all(trainers)
            db.session.commit()
            print("Seeded 5 elite trainers.")

        # 4. Seed Classes
        if GymClass.query.count() == 0:
            marcus = Trainer.query.filter_by(slug="marcus-vance").first()
            elena = Trainer.query.filter_by(slug="elena-rostova").first()
            jaxson = Trainer.query.filter_by(slug="jaxson-cole").first()
            priya = Trainer.query.filter_by(slug="priya-sharma").first()

            classes = [
                GymClass(name="Sunrise HIIT Blast", trainer_id=elena.id if elena else None, day="Monday", start_time="06:00 AM", end_time="07:00 AM", capacity=25, description="High-intensity intervals designed to ignite calorie burn and athletic stamina.", is_active=True),
                GymClass(name="Heavy Barbell Powerlifting", trainer_id=marcus.id if marcus else None, day="Monday", start_time="06:00 PM", end_time="07:30 PM", capacity=15, description="Technique refinement and overload sets on squat, bench press, and deadlift.", is_active=True),
                GymClass(name="Combat Boxing Conditioning", trainer_id=jaxson.id if jaxson else None, day="Tuesday", start_time="07:00 AM", end_time="08:00 AM", capacity=20, description="Heavy bag combinations, footwork drills, and core conditioning.", is_active=True),
                GymClass(name="Athletic Turf Conditioning", trainer_id=elena.id if elena else None, day="Tuesday", start_time="06:30 PM", end_time="07:30 PM", capacity=20, description="Sled pushes, battle ropes, plyometrics, and kettlebell work.", is_active=True),
                GymClass(name="Functional Kettlebell Flow", trainer_id=elena.id if elena else None, day="Wednesday", start_time="06:00 AM", end_time="07:00 AM", capacity=18, description="Multi-planar kettlebell movements targeting core stability and grip strength.", is_active=True),
                GymClass(name="Power Strike & Boxing", trainer_id=jaxson.id if jaxson else None, day="Thursday", start_time="06:00 PM", end_time="07:15 PM", capacity=20, description="High-octane boxing rounds and metabolic burn finisher.", is_active=True),
                GymClass(name="Mobility & Core Recovery Flow", trainer_id=priya.id if priya else None, day="Friday", start_time="07:00 AM", end_time="08:00 AM", capacity=25, description="Joint decompression, myofascial release, and yoga breathwork.", is_active=True),
                GymClass(name="Iron Gauntlet Weekend Circuit", trainer_id=marcus.id if marcus else None, day="Saturday", start_time="08:30 AM", end_time="10:00 AM", capacity=30, description="Our signature team endurance circuit combining strength and speed.", is_active=True)
            ]
            db.session.add_all(classes)
            print("Seeded 8 weekly classes.")

        # 5. Seed Facilities
        if Facility.query.count() == 0:
            facilities = [
                Facility(name="Heavy Strength & Powerlifting Zone", category="Strength", description="Custom Eleiko platforms, calibrated steel discs, and competition-spec power racks.", image_url="https://images.unsplash.com/photo-1540497077202-7c8a3999166f?q=80&w=800&auto=format&fit=crop", display_order=1, is_active=True),
                Facility(name="Precision Cardio & Enduro Lab", category="Cardio", description="Woodway curved treadmills, Concept2 Rowers, SkiErgs, and Assault AirBikes.", image_url="https://images.unsplash.com/photo-1576678927484-cc907957088c?q=80&w=800&auto=format&fit=crop", display_order=2, is_active=True),
                Facility(name="Free Weights & Dumbbell Deck", category="Free Weights", description="Urethane dumbbells from 2kg to 60kg, adjustable incline benches, and preacher stations.", image_url="https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?q=80&w=800&auto=format&fit=crop", display_order=3, is_active=True),
                Facility(name="40-Meter Sprint & Sled Turf", category="Functional", description="High-density shock-absorbent synthetic grass for sled sprints, plyos, and agility drills.", image_url="https://images.unsplash.com/photo-1517838277536-f5f99be501cd?q=80&w=800&auto=format&fit=crop", display_order=4, is_active=True),
                Facility(name="Recovery Lounge & Infrared Saunas", category="Recovery", description="Dry cedarwood saunas, contrast hydrotherapy baths, and compression boot lounge.", image_url="https://images.unsplash.com/photo-1506126613408-eca07ce68773?q=80&w=800&auto=format&fit=crop", display_order=5, is_active=True),
                Facility(name="Executive Lockers & Rainfall Showers", category="Amenities", description="Spacious private lockers, complimentary towel service, grooming bars, and rainfall showers.", image_url="https://images.unsplash.com/photo-1584622650111-993a426fbf0a?q=80&w=800&auto=format&fit=crop", display_order=6, is_active=True)
            ]
            db.session.add_all(facilities)
            print("Seeded 6 facility zones.")

        # 6. Seed Testimonials
        if Testimonial.query.count() == 0:
            testimonials = [
                Testimonial(client_name="Rahul Mehta", review="Ironforge is hands down the best training facility in the city. The calibrated plates and high-energy atmosphere keep you pushing beyond your limits every single workout.", rating=5, image_url="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=100&auto=format&fit=crop", is_featured=True),
                Testimonial(client_name="Tanya Deshmukh", review="I lost 14 kgs in 4 months training with Coach Elena. The periodization and accountability are on a completely different level than standard commercial gyms.", rating=5, image_url="https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=100&auto=format&fit=crop", is_featured=True),
                Testimonial(client_name="Arjun Nair", review="The powerlifting platform setup is world-class. Added 45kg to my total in 6 months under Coach Marcus's guidance. Outstanding community.", rating=5, image_url="https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=100&auto=format&fit=crop", is_featured=True),
                Testimonial(client_name="Sneha Roy", review="The cleanliness, cedar sauna suites, and dynamic boxing classes make waking up for 6 AM workouts the absolute best part of my day.", rating=5, image_url="https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=100&auto=format&fit=crop", is_featured=True),
                Testimonial(client_name="Karan Patel", review="No gimmicks, no waiting for benches. Pure athletic focus and an encouraging community that welcomes everyone from beginners to seasoned lifters.", rating=5, image_url="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=100&auto=format&fit=crop", is_featured=True),
                Testimonial(client_name="Maya Varma", review="The customized nutrition roadmap and functional mobility coaching resolved years of lower back stiffness. Gained confidence and true strength!", rating=5, image_url="https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=100&auto=format&fit=crop", is_featured=True)
            ]
            db.session.add_all(testimonials)
            print("Seeded 6 member testimonials.")

        # 7. Seed Transformations
        if Transformation.query.count() == 0:
            transformations = [
                Transformation(client_name="David K.", before_image="https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?q=80&w=400&auto=format&fit=crop", after_image="https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=400&auto=format&fit=crop", duration="4 Months", achievement="Lost 14 kg & Built Lean Muscle", story="Followed the Ironforge 16-week recomp protocol. Dropped from 24% to 13% body fat while increasing squat and deadlift by 35kg.", is_featured=True, is_active=True),
                Transformation(client_name="Priya M.", before_image="https://images.unsplash.com/photo-1518611012118-696072aa579a?q=80&w=400&auto=format&fit=crop", after_image="https://images.unsplash.com/photo-1594381898411-846e7d193883?q=80&w=400&auto=format&fit=crop", duration="6 Months", achievement="Down 18 kg & Ran First Half-Marathon", story="Came in with zero athletic background. Built core strength and cardiovascular stamina with Coach Elena's daily conditioning split.", is_featured=True, is_active=True),
                Transformation(client_name="Alex R.", before_image="https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?q=80&w=400&auto=format&fit=crop", after_image="https://images.unsplash.com/photo-1567013127542-490d757e51fc?q=80&w=400&auto=format&fit=crop", duration="5 Months", achievement="Gained 8 kg Lean Mass & +50kg Total", story="Structured progressive overload and dialed-in macros under Coach Marcus completely overhauled my physical frame and strength.", is_featured=True, is_active=True),
                Transformation(client_name="Samantha T.", before_image="https://images.unsplash.com/photo-1544005313-94ddf0286df2?q=80&w=400&auto=format&fit=crop", after_image="https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=400&auto=format&fit=crop", duration="3 Months", achievement="Post-Rehab Recovery & -9 kg Fat Loss", story="Eliminated knee discomfort and restored sprint speed through progressive isometric and mobility training.", is_featured=True, is_active=True),
                Transformation(client_name="Vikram S.", before_image="https://images.unsplash.com/photo-1500648767791-00dcc994a43e?q=80&w=400&auto=format&fit=crop", after_image="https://images.unsplash.com/photo-1534367507873-d2d7e24c797f?q=80&w=400&auto=format&fit=crop", duration="6 Months", achievement="Lost 22 kg & Transformed Energy", story="Total lifestyle reset. The coaches gave me the exact daily habits, lifting discipline, and nutrition guidance to thrive.", is_featured=True, is_active=True)
            ]
            db.session.add_all(transformations)
            print("Seeded 5 transformation stories.")

        # 8. Seed Instagram Reels (9:16 vertical cards)
        if InstagramReel.query.count() == 0:
            reels = [
                InstagramReel(
                    title="Top 3 Barbell Deadlift Mistakes",
                    caption="Stop rounding your upper back! Coach Marcus breaks down proper foot rooting and lat wedge. #StrengthTips",
                    instagram_url="https://instagram.com/ironforgefitness",
                    thumbnail_url="https://images.unsplash.com/photo-1517838277536-f5f99be501cd?q=80&w=600&auto=format&fit=crop",
                    video_url="https://assets.mixkit.co/videos/preview/mixkit-man-working-out-with-a-battle-rope-in-a-gym-42646-large.mp4",
                    display_order=1,
                    is_featured=True,
                    is_active=True
                ),
                InstagramReel(
                    title="Explosive Dumbbell Snatch Form",
                    caption="Triple extension mechanics on the turf with Coach Elena. #AthleticTraining #HIIT",
                    instagram_url="https://instagram.com/ironforgefitness",
                    thumbnail_url="https://images.unsplash.com/photo-1594381898411-846e7d193883?q=80&w=600&auto=format&fit=crop",
                    video_url="https://assets.mixkit.co/videos/preview/mixkit-crossfit-athlete-doing-snatches-with-a-dumbbell-43288-large.mp4",
                    display_order=2,
                    is_featured=True,
                    is_active=True
                ),
                InstagramReel(
                    title="Boxing Footwork & Hook Mechanics",
                    caption="Generating explosive power from the hips: Coach Jaxson demonstrates rapid 1-2-hook combinations.",
                    instagram_url="https://instagram.com/ironforgefitness",
                    thumbnail_url="https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?q=80&w=600&auto=format&fit=crop",
                    video_url="https://assets.mixkit.co/videos/preview/mixkit-young-boxer-training-in-the-gym-43093-large.mp4",
                    display_order=3,
                    is_featured=True,
                    is_active=True
                ),
                InstagramReel(
                    title="5-Min Pre-Squat Hip Opener",
                    caption="Unlock your deep squat depth with this 5-minute pre-training mobility sequence from Coach Priya.",
                    instagram_url="https://instagram.com/ironforgefitness",
                    thumbnail_url="https://images.unsplash.com/photo-1518611012118-696072aa579a?q=80&w=600&auto=format&fit=crop",
                    video_url="https://assets.mixkit.co/videos/preview/mixkit-woman-doing-stretching-exercises-in-a-gym-43187-large.mp4",
                    display_order=4,
                    is_featured=True,
                    is_active=True
                ),
                InstagramReel(
                    title="Friday Night Heavy PR Session",
                    caption="Electric energy on the platforms tonight! 3 new gym records shattered. #IronforgeAthletes",
                    instagram_url="https://instagram.com/ironforgefitness",
                    thumbnail_url="https://images.unsplash.com/photo-1534438327276-14e5300c3a48?q=80&w=600&auto=format&fit=crop",
                    video_url="https://assets.mixkit.co/videos/preview/mixkit-athlete-lifting-weights-in-a-gym-42647-large.mp4",
                    display_order=5,
                    is_featured=True,
                    is_active=True
                ),
                InstagramReel(
                    title="Post-Workout Recovery Smoothie",
                    caption="Optimal 3:1 carb-to-protein ratio at the Ironforge Smoothie Bar. Fuel your recovery right.",
                    instagram_url="https://instagram.com/ironforgefitness",
                    thumbnail_url="https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?q=80&w=600&auto=format&fit=crop",
                    video_url="https://assets.mixkit.co/videos/preview/mixkit-people-exercising-in-a-gym-43075-large.mp4",
                    display_order=6,
                    is_featured=True,
                    is_active=True
                )
            ]
            db.session.add_all(reels)
            print("Seeded 6 interactive Instagram reels.")

        # 9. Seed Sample Trials, Consultations, and Enquiries for live dashboard demo
        if TrialRequest.query.count() == 0:
            trials = [
                TrialRequest(name="Ananya Roy", email="ananya@example.com", phone="+91 98111 22334", age=24, fitness_goal="Weight Loss & Fat Burn", preferred_date="2026-09-12", preferred_time="06:00 AM - 08:00 AM (Early Bird)", message="Interested in testing group HIIT classes.", status="NEW"),
                TrialRequest(name="Rohan Gupta", email="rohan@example.com", phone="+91 98222 33445", age=29, fitness_goal="Muscle Gain & Hypertrophy", preferred_date="2026-09-14", preferred_time="06:00 PM - 08:00 PM (Prime Hours)", message="Looking for powerlifting racks and calibrated plates.", status="CONTACTED"),
                TrialRequest(name="Kavita Sen", email="kavita@example.com", phone="+91 98333 44556", age=32, fitness_goal="General Health & Flexibility", preferred_date="2026-09-15", preferred_time="08:00 AM - 10:00 AM (Morning Peak)", message="Want to test the yoga and mobility studio.", status="CONFIRMED")
            ]
            db.session.add_all(trials)

        if Consultation.query.count() == 0:
            marcus = Trainer.query.filter_by(slug="marcus-vance").first()
            elena = Trainer.query.filter_by(slug="elena-rostova").first()
            consultations = [
                Consultation(name="Manish Verma", email="manish@example.com", phone="+91 98444 55667", trainer_id=marcus.id if marcus else 1, goal="1-on-1 Personal Training", fitness_level="Intermediate (1-2 years consistent)", preferred_date="2026-09-16", preferred_time="06:00 PM", message="Need help breaking past a 140kg squat plateau.", status="PENDING"),
                Consultation(name="Ritika Bajaj", email="ritika@example.com", phone="+91 98555 66778", trainer_id=elena.id if elena else 2, goal="Body Transformation Program", fitness_level="Beginner (Just getting started)", preferred_date="2026-09-18", preferred_time="09:00 AM", message="Looking for a structured 12-week fat loss plan.", status="CONFIRMED")
            ]
            db.session.add_all(consultations)

        if Enquiry.query.count() == 0:
            enquiries = [
                Enquiry(name="Siddharth Rao", email="siddharth@example.com", phone="+91 98666 77889", subject="Corporate Membership Inquiry", message="We have a team of 25 employees and would like to explore corporate annual packages.", status="NEW"),
                Enquiry(name="Pooja Nair", email="pooja@example.com", phone="+91 98777 88990", subject="Personal Locker & Valet Parking", message="Are dedicated executive lockers included in the Elite Performance plan?", status="RESOLVED")
            ]
            db.session.add_all(enquiries)

        db.session.commit()
        print("Database seeded successfully with all demo data!")

if __name__ == '__main__':
    seed_database()
