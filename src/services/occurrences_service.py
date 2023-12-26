from models.Occurrences import Occurrences
from app import db
from sqlalchemy import text


def get_occurrences_list(user_id:int) -> list:
    
    user_occurrences = Occurrences.query\
        .filter(Occurrences.user_id==user_id)\
        .order_by(Occurrences.created.desc())\
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

def group_occorrences_day(user_id:int) -> list:
     
    query = text(
        '''
        SELECT
            DAY(oc.created) AS day,
            MONTH(oc.created) AS month,
            COUNT(*) AS count
        FROM
            (
                SELECT 
                    created,
                    user_id 
                FROM  occurrences 
                WHERE :user_id=user_id
                ORDER BY created DESC

            ) oc
        GROUP BY
            DAY(oc.created),
            MONTH(oc.created)
        
        LIMIT 7 
    
        '''
    )
    
    result = db.session.execute(query, {"user_id": user_id})


    formatted_result = [
        {
            'date': f'{row.day}/{row.month}',
            'count': row.count
         }
        for row in result
    ]

    return formatted_result