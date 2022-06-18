import random
import string


def random_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_int(negative=True) -> int:
    if negative:
        return random.randint(-5000, 5000)
    else:
        return random.randint(0, 5000)


def random_float(negative=True) -> float:
    if negative:
        return random.uniform(-5.0, 5.0)
    else:
        return random.uniform(0.0, 5.0)


def get_example_template() -> str:
    return ("{% for p in welding_points %}"
            "{{p.x}}, {{p.y}}, {{p.z}} / {{p.roll}}, {{p.pitch}}, {{p.yaw}} / {{p.welding_order}}"
            "{% endfor %}")
