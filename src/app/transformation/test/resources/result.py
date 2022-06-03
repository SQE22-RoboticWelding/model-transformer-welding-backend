import json
import sys

from rospy import *


def init():
    rospy.setEnv("JAVA_HOME", "/dev/null")
    rospy.setEnv("PATH", "/dev/null")

    return


def run(niryo):
    niryo.move_pos(x=10.5, log="This is a wooden log.")
    niryo.grab_with_tool(tool_id="hand", num=5)

    return


if __name__ == '__main__':
    init()
    niryo = NiryoOne()
    run(niryo)
