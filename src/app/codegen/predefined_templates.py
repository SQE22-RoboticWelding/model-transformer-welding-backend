

class PredefinedTemplates:
    NIRYO_ONE_ROS = """from niryo_one_python_api.niryo_one_api import NiryoOne
import rospy
import time


def grab_release_reset(niryo):
    niryo.grab_with_tool(niryo.get_current_tool_id())  # grab
    niryo.release_tool(niryo.get_current_tool_id())  # release
    niryo.move_pose(0.1, 0.1, 0.4, 0, 0, 0)  # reset


if __name__ = '__main__':
    rospy.init_node('niryo_one_example_python_api')
    n = NiryoOne()

    {% for p in welding_points -%}
    n.move_pos(x={{p.x}}, y={{p.y}}, z={{p.z}}, roll={{p.roll}}, pitch={{p.pitch}}, yaw={{p.yaw}})
    grab_release_reset(niryo)
    {%- if loop.index != welding_points|length %}
    {% endif %}{% endfor %}
"""
