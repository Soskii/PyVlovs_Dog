import gui
import sim_window
import network_ph
d = sim_window.Dog(gui.t_location)


def obj_update(obj_type, obj_build):
    obj_build.name = obj_type.name.get()
    obj_build.colour = obj_type.colour.get()
    obj_build.collide = obj_type.var.get()
    obj_build.size = obj_type.size.get()
    obj_build.alpha = obj_type.alpha.get()

def dog_update():
    global d
    if d.location != gui.t_location:
        try:
            d = sim_window.Dog(gui.t_location)
        except:
            print("Invalid File Location")

while True:
    # events
    reinforcement = gui.rules_check()

    # back updates
    wheel_vols = network_ph.pol_net()
    for obj in range(len(gui.object_types)):
        obj_update(gui.object_types[obj], sim_window.obj_list[obj])

    # display updates
    sim_window.space_step(gui.sim_speed.get(), wheel_vols, d)
    dog_update()
    gui.update_gui()
    sim_window.update_sim(d)
