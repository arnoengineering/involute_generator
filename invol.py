import numpy as np
import sympy as sy
import matplotlib.pyplot as plt


def gen_eq(r, theta, pos=(1, 1)):
    eq = np.array((np.cos(theta), np.sin(theta))) * r
    for i in range(2):
        eq[i] = eq[i]*pos[i]
    return eq


class circle:
    def __init__(self, d, mod, p=20, stub=False):

        self.mod = mod
        self.d = d

        self.n = d / mod
        if stub:
            self.ad = 1.6 * mod
            self.dd = 2.7 * mod
        else:
            self.ad = 2 * mod
            self.dd = 2.5 * mod
        self.ad = 1.6 * mod if stub else 2 * mod
        self.p = np.deg2rad(p)

        self.db = d*np.cos(self.p)

        self.alfa = np.sqrt(d**2-self.db**2)/self.db-self.p
        self.bet = np.pi/self.n-4*self.alfa
        self.fil = 0.2 * mod

        self.do = d + self.ad
        self.dr = d-self.dd

        self.ro = self.do / 2
        self.rb = self.db / 2
        self.rr = self.dr / 2
        self.r = self.d / 2
        # self.c_xb =
        self.ang = 2*np.pi/self.n
        self.fil_ang = None
        self.x = None
        self.x1 = None

        self.xc = None
        self.yc = None

    def gen_invol(self, ang=0, t_sp=0.1):
        t_n = np.sqrt((self.ro / self.rb) ** 2-1)
        t = np.arange(0, t_n+t_sp, t_sp) + ang
        t2 = t + self.bet
        self.x = self.rb * np.array((np.cos(t) + t * np.sin(t), np.sin(t) - t * np.cos(t)))
        self.x1 = self.rb * np.array((np.cos(t2) + t * np.sin(t2), -(np.sin(t2) - t * np.cos(t2))))

    def gen_f_a(self, ri):
        self.fil_ang = np.arctan(self.fil / ri + self.fil)

    def gen_root(self, ang=0, t_sp=0.1):
        def line(thet):
            dr = np.arange(self.rr+self.fil, self.rb, t_sp)
            l_x = dr*np.cos(thet)
            l_y = dr*np.sin(thet)
            return l_x, l_y

        def con_eq(ri, *eqs):

            t2 = np.arange(ang - self.fil_ang, -self.bet + ang + self.fil_ang, t_sp)
            x = gen_eq(ri, t2)
            return np.concatenate((*eqs, x), 1)
        if self.dr > self.db:  # aaddddd, add fil, fill =
            self.gen_invol(ang)
            self.gen_f_a(self.rb)
            x_f = self.gen_fil(self.rb, ang)
            # todo fix
            self.xc = con_eq(self.rb, x_f)
            self.xc = np.concatenate((self.xc, self.gen_fil(self.rb, ang-self.bet, False)))
        else:
            self.gen_invol(ang)
            l1 = line(ang)
            l2 = line(ang-self.bet)
            self.gen_f_a(self.rr)
            x_f = self.gen_fil(self.rr, ang)
            self.xc = con_eq(self.rr, l1, x_f)
            self.xc = np.concatenate((self.xc, self.gen_fil(self.rr, ang-self.bet, False), l2), 1)

    def gen_fil(self, r, angle=0, left=True, t_sp=0.1):  # add for circ curve

        if left:
            ang_st = 3 * np.pi / 2
            tr = np.arange(np.pi / 2 + angle, np.pi + angle + self.fil_ang, t_sp)
        else:
            tr = np.arange(np.pi + angle - self.fil_ang, 3 * np.pi / 2 + angle, t_sp)
            ang_st = np.pi/2
        init_pos = gen_eq(r+self.fil, angle)
        cent = init_pos + gen_eq(self.fil, angle+ang_st)

        x_f = gen_eq(self.fil, tr)
        for i in range(2):
            x_f[i] = x_f[i] + cent[i]
        return x_f

    def gen_tooth(self):
        for i in np.linspace(0,2*np.pi, self.n):
            self.gen_invol()
            self.gen_root()  # todo for n, space n
            self.plot_circ()

    def plot_circ(self):
        def cir(r):
            return r*np.cos(th), r*np.sin(th)
        th = np.arange(0, 2*np.pi, 0.1)
        bc = cir(self.rb)
        rc = cir(self.rr)
        oc = cir(self.ro)
        pc = cir(self.r)
        # for xy in
        plt.plot(*self.x, *self.x1, *self.xc, *pc, *oc, *rc, *bc)  # *pc, *oc, *rc, *bc, self.x1, self.xc)
        # plt.scatter(*self.x)
        # plt.scatter(*self.x1) # , *self.xc) # , *pc, *oc, *rc, *bc) # *pc, *oc, *rc, *bc, self.x1, self.xc
        # plt.scatter(*self.xc)
        plt.show()


if __name__ == '__main__':
    a = circle(10, 1)
    a.gen_root()
    a.plot_circ()
