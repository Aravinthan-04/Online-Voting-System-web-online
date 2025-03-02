from app import db, Voter, Candidate, app

with app.app_context():
    # Create database tables
    db.create_all()

    # Add sample voters
    sample_voters = [
        Voter(voter_id="10001", password="abcd"),
        Voter(voter_id="10002", password="abcd"),
        Voter(voter_id="10003", password="abcd"),
    ]

    # Add candidates
    sample_candidates = [
        Candidate(name="Candidate A"),
        Candidate(name="Candidate B"),
        Candidate(name="Candidate C"),
    ]

    db.session.bulk_save_objects(sample_voters)
    db.session.bulk_save_objects(sample_candidates)
    db.session.commit()

    print("✅ Database initialized with sample voters and candidates!")
