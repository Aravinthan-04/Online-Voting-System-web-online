from app import db, Voter, Candidate, app

with app.app_context():
    # Create database tables
    db.create_all()

    # Add sample voters
    sample_voters = [
        Voter(voter_id="aravinth", password="2005"),
        Voter(voter_id="mujibu", password="2004"),
        Voter(voter_id="amizhthan", password="2005"),
        Voter(voter_id="kishore", password="2002"),
    ]

    # Add candidates
    sample_candidates = [
        Candidate(name="REPRESENTATIVE"),
        Candidate(name="ASSISTENT REPRESENTATIVE"),
    
    ]

    db.session.bulk_save_objects(sample_voters)
    db.session.bulk_save_objects(sample_candidates)
    db.session.commit()

    print("✅ Database initialized with sample voters and candidates!")
