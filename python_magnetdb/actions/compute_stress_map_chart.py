import MagnetTools.Bmap as bmap
import MagnetTools.MagnetTools as mt
import numpy as np

def getHoop(Magnets, Tubes, Helices, BMagnets, UMagnets, MType):
    """
    Compute Hoop Stress
    """

    Hoop_ = []
    Hoop_headers = ["num", "r[m]", "j[A/m\u00b2]", "Bz[T]", "Bz_self[T]", "Hoop[MPa]", "Self"] # add self, ext

    # Tube.get_index() is faulty in python
    nindex = 0
    # for i, Tube in enumerate(Tubes):
    #     print("H[%d]: " % (i+1),  Tube)

    if isinstance(Magnets,mt.VectorOfTubes):
        for i, Magnet in enumerate(Magnets):
            rint = Magnet.get_R_int()
            j = None

            # self field:
            B0_l = 0

            n_elem = Magnet.get_n_elem()
            mid_elem = int(n_elem / 2) if (n_elem % 2) == 0 else int((n_elem+1) / 2)
            # print("Magnet[%d]: n_elem=%d" % (i, n_elem), "mid_elem=%d" % mid_elem, len(Helices), "index=%d" % Magnet.get_index())
            j = Helices[mid_elem+Magnet.get_index()].get_CurrentDensity()
            for k,Tube in enumerate(Tubes):
                n_elem = Tube.get_n_elem()
                nindex = Tube.get_index()
                for l in range(n_elem):
                    num = l + nindex #Tube.get_index()
                    # print("Tube[%d]: elem%d/%d" % (k, l, n_elem), "mid_elem=%d" % mid_elem, len(Helices), "num=%d" % num, "index=%d" % Tube.get_index())
                    B0_l += Helices[num].MagneticField(rint, 0.)[1]

            # Total field
            Bz = mt.MagneticField(Tubes, Helices, BMagnets, UMagnets, rint, 0)[1]
            Hoop_.append(["%s%d" % (MType, (i+1)), rint, j, Bz, B0_l, rint * j * Bz / 1.e+6, rint * j * B0_l / 1.e+6])

    elif isinstance(Magnets,mt.VectorOfBitters):
        stacks = mt.create_Bstack(Magnets)
        for i,stack in enumerate(stacks):
            rint = Magnets[stack[0]].get_R_int()
            mid_stack = 0
            for n in stack:
                mid_stack = int(n / 2) if (n % 2) == 0 else int((n+1) / 2)
            j = Magnets[mid_stack].get_CurrentDensity()

            # self field:
            B0_l = 0
            for jMagnet in Magnets:
                B0_l += jMagnet.MagneticField(rint, 0.)[1]

            # Total field
            Bz = mt.MagneticField(Tubes, Helices, BMagnets, UMagnets, rint, 0)[1]
            Hoop_.append(["%s%d" % (MType, (i+1)), rint, j, Bz, B0_l, rint * j * Bz / 1.e+6, rint * j * B0_l / 1.e+6])

    elif isinstance(Magnets,mt.VectorOfUnifs):
        stacks = mt.create_Ustack(Magnets)
        for i,stack in enumerate(stacks):
            rint = Magnets[stack[0]].get_R_int()
            mid_stack = 0
            for n in stack:
                mid_stack = int(n / 2) if (n % 2) == 0 else int((n+1) / 2)
            j = Magnets[mid_stack].get_CurrentDensity()

            # self field:
            B0_l = 0
            for jMagnet in Magnets:
                B0_l += jMagnet.MagneticField(rint, 0.)[1]

            # Total field
            Bz = mt.MagneticField(Tubes, Helices, BMagnets, UMagnets, rint, 0)[1]
            Hoop_.append(["%s%d" % (MType, (i+1)), rint, j, Bz, B0_l, rint * j * Bz / 1.e+6, rint * j * B0_l / 1.e+6])
    else:
        raise Exception("getHoop: unknown type of VectorOfMagnets")

    return (Hoop_headers, Hoop_)

def prepare_stress_map_chart_params(data, i_h, i_b, i_s):
    (Tubes, Helices, OHelices, BMagnets, UMagnets, Shims) = data
    icurrents = mt.get_currents(Tubes, Helices, BMagnets, UMagnets)

    return (
        i_h if i_h is not None else (icurrents[0] if len(icurrents) > 0 else 0),
        i_b if i_b is not None else (icurrents[1] if len(icurrents) > 1 else 0),
        i_s if i_s is not None else (icurrents[2] if len(icurrents) > 2 else 0),
        ["i_h", "i_b", "i_s"][:len(icurrents)],
    )


def compute_stress_map_chart(data, i_h, i_b, i_s):
    def update_current():
        (Tubes, Helices, OHelices, BMagnets, UMagnets, Shims) = data

        icurrents = mt.get_currents(Tubes, Helices, BMagnets, UMagnets)
        n_magnets = len(icurrents)
        mcurrents = icurrents
        print("n_magnets", n_magnets)
        print("icurrents", icurrents)
        for j,Tube in enumerate(Tubes):
            print(f"Tube[{j}]", Tube.get_n_elem(), Tube.get_index())
            for i in range(Tube.get_n_elem()):
                print(f"H[{i}]: j={Helices[i + Tube.get_index()].get_CurrentDensity()}")
        Bz0 = mt.MagneticField(Tubes, Helices, BMagnets, UMagnets, 0, 0)[1]
        print("Bz0=", Bz0)

        # update Ih, Ib, Is range
        vcurrents = list(icurrents)
        num = 0
        if len(Tubes) != 0: vcurrents[num] = i_h; num += 1
        if len(BMagnets) != 0: vcurrents[num] = i_b; num += 1
        if len(UMagnets) != 0: vcurrents[num] = i_s; num += 1

        currents = mt.DoubleVector(vcurrents)
        print(f"currents= set to {vcurrents}")
        mt.set_currents(Tubes, Helices, BMagnets, UMagnets, OHelices, currents)
        print("actual currents", mt.get_currents(Tubes, Helices, BMagnets, UMagnets) )
        Bz0 = mt.MagneticField(Tubes, Helices, BMagnets, UMagnets, 0, 0)[1]
        print("Bz0=", Bz0)

    def sine():
        (Tubes, Helices, OHelices, BMagnets, UMagnets, Shims) = data
        return getHoop(UMagnets, Tubes, Helices, BMagnets, UMagnets, "S")

    def compute_max():
        (Tubes, Helices, OHelices, BMagnets, UMagnets, Shims) = data

        # get current for max
        icurrents = mt.get_currents(Tubes, Helices, BMagnets, UMagnets)
        vcurrents = list(icurrents)
        num = 0
        if len(Tubes) != 0: vcurrents[num] = 31.e+3; num += 1
        if len(BMagnets) != 0: vcurrents[num] = 31.e+3; num += 1
        if len(UMagnets) != 0: vcurrents[num] = 0; num += 1

        Bz0 = mt.MagneticField(Tubes, Helices, BMagnets, UMagnets, 0, 0)[1]

        currents = mt.DoubleVector(vcurrents)
        mt.set_currents(Tubes, Helices, BMagnets, UMagnets, OHelices, currents)
        x, y = sine()
        return y

    update_current()
    x, y = sine()
    return dict(x=x, y=y, ymax=compute_max())
