#!/usr/bin/python3
""" console """

import cmd
import shlex  # for splitting the line along spaces except in double quotes

import models
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

all_cls = {
    "State": State, "User": User,
    "Amenity": Amenity, "City": City,
    "Place": Place, "Review": Review
}


class HBNBCommand(cmd.Cmd):
    """ HBNH console """
    pmt = '(hbnb) '

    def do_EOF(self, arg):
        """do_EOF"""
        return True

    def emptyline(self):
        """ emptyline """
        return False

    def do_quit(self, arg):
        """do_quit"""
        return True

    def _key_value_parser(self, args):
        """_key_value_parser"""
        nd = {}
        for a in args:
            if "=" in a:
                vp = a.split('=', 1)
                k = vp[0]
                vl = vp[1]
                if vl[0] == vl[-1] == '"':
                    vl = shlex.split(vl)[0].replace('_', ' ')
                else:
                    try:
                        vl = int(vl)
                    except ValueError:
                        try:
                            vl = float(vl)
                        except ValueError:
                            continue
                nd[k] = vl
        return nd

    def do_create(self, arg):
        """do_create"""
        ags = arg.split()
        if len(ags) == 0:
            print("** class name missing **")
            return False
        if ags[0] in all_cls:
            nd = self._key_value_parser(ags[1:])
            ins = all_cls[ags[0]](**nd)
        else:
            print("** class doesn't exist **")
            return False
        print(ins.id)
        ins.save()

    def do_show(self, arg):
        """do_show"""
        ags = shlex.split(arg)
        if len(ags) == 0:
            print("** class name missing **")
            return False
        if ags[0] in all_cls:
            if len(ags) > 1:
                k = ags[0] + "." + ags[1]
                if k in models.storage.all():
                    print(models.storage.all()[k])
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_destroy(self, arg):
        """do_destroy"""
        ags = shlex.split(arg)
        if len(ags) == 0:
            print("** class name missing **")
        elif ags[0] in all_cls:
            if len(ags) > 1:
                k = ags[0] + "." + ags[1]
                if k in models.storage.all():
                    models.storage.all().pop(k)
                    models.storage.save()
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")

    def do_all(self, arg):
        """do_all"""
        ags = shlex.split(arg)
        ojl = []
        if len(ags) == 0:
            ojd = models.storage.all()
        elif ags[0] in all_cls:
            ojd = models.storage.all(all_cls[ags[0]])
        else:
            print("** class doesn't exist **")
            return False
        for k in ojd:
            ojl.append(str(ojd[k]))
        print("[", end="")
        print(", ".join(ojl), end="")
        print("]")

    def do_update(self, arg):
        """do_update"""
        ags = shlex.split(arg)
        igs = [
            "number_rooms",
            "number_bathrooms",
            "max_guest",
            "price_by_night"
        ]
        fls = [
            "latitude",
            "longitude"
        ]
        if len(ags) == 0:
            print("** class name missing **")
        elif ags[0] in all_cls:
            if len(ags) > 1:
                k = ags[0] + "." + ags[1]
                if k in models.storage.all():
                    if len(ags) > 2:
                        if len(ags) > 3:
                            if ags[0] == "Place":
                                if ags[2] in igs:
                                    try:
                                        ags[3] = int(ags[3])
                                    except ValueError:
                                        ags[3] = 0
                                elif ags[2] in fls:
                                    try:
                                        ags[3] = float(ags[3])
                                    except ValueError:
                                        ags[3] = 0.0
                            setattr(models.storage.all()[k], ags[2], ags[3])
                            models.storage.all()[k].save()
                        else:
                            print("** value missing **")
                    else:
                        print("** attribute name missing **")
                else:
                    print("** no instance found **")
            else:
                print("** instance id missing **")
        else:
            print("** class doesn't exist **")


if __name__ == '__main__':
    HBNBCommand().cmdloop()
