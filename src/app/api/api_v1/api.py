from app.api.api_v1.endpoints import (test, robot, robot_type, project, welding_point,
                                      generation_template, code_generation)
from app.api.generic_exception_handler import APIRouterWithGenericExceptionHandler

api_router = APIRouterWithGenericExceptionHandler()
api_router.include_router(project.router, prefix="/project", tags=["Project"])
api_router.include_router(robot_type.router, prefix="/robottype", tags=["RobotType"])
api_router.include_router(robot.router, prefix="/robot", tags=["Robot"])
api_router.include_router(welding_point.router, prefix="/weldingpoint", tags=["WeldingPoint"])
api_router.include_router(generation_template.router, prefix="/generationtemplate", tags=["GenerationTemplate"])
api_router.include_router(code_generation.router, prefix="/codegeneration", tags=["CodeGeneration"])
api_router.include_router(test.router, prefix="/test", tags=["Test"])
