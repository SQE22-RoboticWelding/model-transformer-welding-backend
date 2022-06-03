
def init():
    rospy.setEnv("JAVA_HOME", "/dev/null")
    rospy.setEnv("PATH", "/dev/null")

    return


if __name__ == '__main__':
    init()
