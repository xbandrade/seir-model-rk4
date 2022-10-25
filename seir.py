from compartment import S, E, I, R
from config import *
from app import App, MainFrame, rk4


def main() -> None:
    s0, e0, i0, r0 = S(S_0), E(E_0), I(I_0), R(R_0)
    compartments = s0, e0, i0, r0
    app = App()
    rk4(T_0, compartments)
    MainFrame(app, compartments)
    app.mainloop()


if __name__ == '__main__':
    main()
