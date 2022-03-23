from functools import wraps

from flask import Blueprint as _Blueprint, current_app

from app.libs.permission import permission_required

navs = {}
navs_link = {}


class Blueprint(_Blueprint):
    def nav(self, name, permission=0, location="left", **options):
        def wrap(func):
            navs[name] = NavBase(name.split(".")[-1], "{}.{}".format(self.name, func.__name__), permission, location,
                                 **options)

            @wraps(func)
            @permission_required(permission)
            def _wrap(*args, **kwargs):
                return func(*args, **kwargs)

            return _wrap

        return wrap


def init_nav():
    for name in navs:
        if "." in name:
            name_l = name.split(".")
            if name_l[0] not in navs_link:
                navs_link[name_l[0]] = {"name": name_l[0], "dropdown": [],
                                        "permission": navs[name].permission}
            else:
                navs_link[name_l[0]]["permission"] &= navs[name].permission
            navs_link[name_l[0]]["dropdown"].append(navs[name])
        else:
            navs_link[name] = navs[name]
    current_app.add_template_global(navs_link, 'navs_link')


class NavBase:
    name: str
    href: str
    permission: int
    location: str
    options: dict
    is_active: bool = False

    def __init__(self, name, href, permission=0, location="left", **options):
        self.name = name
        self.permission = permission
        self.href = href
        self.location = location
        self.options = options

    def __repr__(self):
        return "<NavBase object (name:{},href:{},permission:{})>".format(self.name, self.href, self.permission)


__all__ = [Blueprint, init_nav]

if __name__ == '__main__':
    pass
