from pyo import *

s = Server().boot()


class MyInstrument(EventInstrument):
    def __init__(self, **args):
        EventInstrument.__init__(self, **args)

        # # self.freq is derived from the 'degree' argument.
        # self.phase = Phasor([self.freq, self.freq * 1.003])

        # # self.dur is derived from the 'beat' argument.
        # self.duty = Expseg([(0, 0.05), (self.dur, 0.5)], exp=4).play()

        # self.osc = Compare(self.phase, self.duty, mode="<", mul=1, add=-0.5)

        # # EventInstrument created the amplitude envelope as self.env.
        # self.filt = ButLP(self.osc, freq=5000, mul=self.env).out()

        self.duty = SineLoop(freq = 500,feedback=.1, mul=.2).out()


# We tell the Events object which instrument to use with the 'instr' argument.
e = Events(
    instr=MyInstrument,
    degree=EventSeq([4]),
    beat=1 / 2.0,
    db=-12,
    attack=0.001,
    decay=0.05,
    sustain=0.5,
    release=0.005,
).play()

s.gui(locals())

# s = Server().boot()
# s.start()
# f = Phasor(freq=[1, 1.5], mul=1000, add=500)
# sine = Sine(freq=f, mul=.2).out()


# s = Server().boot()
# s.start()
# l = Expseg([(0,500),(.03,1000),(.1,700),(1,500),(2,500)], loop=True)
# a = Sine(freq=l, mul=.3).mix(2).out()
# # then call:
# l.play()

# s = Server().boot()
# s.start()
# # a = SineLoop(freq=[199,200], feedback=.1, mul=.2)
# b = SineLoop(feedback=.1, mul=.2).out()
# s.gui(locals())
# ph = Phasor(freq=1)
# ch = Compare(input=ph, comp=0.5, mode="<=")
# out = Selector(inputs=[a,b], voice=Port(ch)).out()