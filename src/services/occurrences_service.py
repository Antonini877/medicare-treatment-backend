from models.Occurrences import Occurrences
from app import db

def get_occurrences_list(user_id:int) -> list:
    
    user_occurrences = Occurrences.query\
        .filter(Occurrences.user_id==user_id)\
        .order_by(Occurrences.created)\
        .all()
    

    results = [
            {
                'datetime': occurrence.created,
                'pain': occurrence.pain,
                'description': occurrence.description
            }
            for occurrence in user_occurrences
        ]
    return results

def write_occurrence(user_id:int, data:dict) -> None:
    new_occurrence = Occurrences(
        user_id=user_id,
        pain=data['pain'],
        description=data['description'] if 'description' in data else None,
        created=data['created']
    )

    db.session.add(new_occurrence)
    db.session.commit()