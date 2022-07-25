# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base # noqa
from app.models.robot_type import RobotType # noqa
from app.models.robot import Robot # noqa
from app.models.welding_point import WeldingPoint # noqa
from app.models.project import Project # noqa
from app.models.generation_template import GenerationTemplate # noqa
from app.models.workpiece import Workpiece # noqa
