from app import db, Voter, Candidate, app

with app.app_context():
    # Create database tables
    db.create_all()

    # Add sample voters
    sample_voters = [
        
    ]

    # Add candidates
    sample_candidates = [
        
    ]

    db.session.bulk_save_objects(sample_voters)
    db.session.bulk_save_objects(sample_candidates)
    db.session.commit()

    print("✅ Database initialized with sample voters and candidates!")
