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
                'datetime': occurrence.created.strftime('%d/%m/%Y %H:%M:%S'),
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

def group_occurrences_day(user_id:int) -> list:
     
    query = text(
        '''
        SELECT
            DAY(oc.created) AS day,
            MONTH(oc.created) AS month,
            COUNT(*) AS count,
            AVG(oc.pain) AS avg_pain
        FROM
            (
                SELECT 
                    created,
                    user_id,
                    pain
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
            'count': row.count,
            'avg_pain': float(row.avg_pain)
         }
        for row in result
    ]

    return formatted_result


def group_occurrences_day_period(user_id:int) -> list:
     
    query = text(
        '''
        
        SELECT
            oc.time_of_day,
            COUNT(oc.time_of_day) AS count,
            AVG(oc.pain) AS avg_pain
        FROM
            (
                SELECT 
                    CASE
                        WHEN HOUR(created) >= 0 AND HOUR(created) < 4 THEN 'Midnight'
                        WHEN HOUR(created) < 12 THEN 'Morning'
                        WHEN HOUR(created) >= 12 AND HOUR(created) < 15 THEN 'Afternoon'
                        WHEN HOUR(created) >= 15 AND HOUR(created) < 17 THEN 'Late afternoon'
                        ELSE 'Evening'
                    END AS time_of_day,
                    user_id,
                    pain
                FROM  occurrences 
                WHERE :user_id=user_id
                AND  created >= DATE_SUB(NOW(), INTERVAL 1 MONTH)
                AND created <= NOW()
            ) oc
        GROUP BY
            oc.time_of_day      
    
        '''
    )
    
    result = db.session.execute(query, {"user_id": user_id})


    formatted_result = [
        {
            'time_of_day': row.time_of_day,
            'count': row.count,
            'avg_pain':float(row.avg_pain)
         }
        for row in result
    ]

   

    return formatted_result