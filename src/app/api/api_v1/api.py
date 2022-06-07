from fastapi import APIRouter
from app.api.api_v1.endpoints import (test, robot, robot_type, welding_configuration, welding_point,
                                      generation_template, code_generation)

api_router = APIRouter()
api_router.include_router(robot_type.router, prefix="/robottype", tags=["RobotType"])
api_router.include_router(robot.router, prefix="/robot", tags=["Robot"])
api_router.include_router(welding_configuration.router, prefix="/weldingconfiguration", tags=["WeldingConfiguration"])
api_router.include_router(welding_point.router, prefix="/weldingpoint", tags=["WeldingPoint"])
api_router.include_router(test.router, prefix="/test", tags=["test"])
api_router.include_router(robot_type.router, prefix="/robottype", tags=["robotType"])
api_router.include_router(generation_template.router, prefix="/generationtemplate", tags=["generationTemplate"])
api_router.include_router(code_generation.router, prefix="/codegeneration", tags=["codeGeneration"])
