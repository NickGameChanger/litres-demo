from aiohttp.web import Response, RouteTableDef, Request, json_response
from api.decorators import ValidatorType, login_not_required
from sqlalchemy.orm import Session
from db.models import User
from datetime import datetime
routes = RouteTableDef()


@routes.post('/api/sing_up', name='singup')
@login_not_required(validator_type=ValidatorType.create_user)
async def application_file(request: Request, db: Session, email: str) -> Response:
    db.add(User(email=email, registration_completed_at=datetime.utcnow()))
    db.commit()

    return json_response({
        'is_user_created': True
    })
