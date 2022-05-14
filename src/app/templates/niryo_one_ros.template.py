from niryo_one_python_api.niryo_one_api import *
import rospy


def run_actions(n):
    {% for action in action_sequence %}
    n.{{ action.key }}({% for param in action.parameters %}{{param.name}}={{param.value}}{% endfor %})

    {% endfor %}

if __name__ == '__main__':
    rospy.init_node('{{ node_name }}')

    niryo_one = NiryoOne()
    run_actions(niryo_one)
