from pyo import *
s = Server(winhost="wdm-ks").boot()
s.start()
a = '''
; Title: La perdriole
; Author: traditionnel
A = r6 o4 v40 g3 v50 o5 c d e f g5 o+ c o- b3 a g f e d c7
B = |: g3 g g4 f1 e3 d c5 :| g1 g g g g g g g b-3 o+ c d7 r7
C = |: o5 c4 d1 e3 f g4 o+ c1 o- b3 a g f e d e d c5 r5 :|
#0 t92 x.1 |: A A B C :|
A1 = |: r7 o4 c7 d7 e5 f g c7 :|
B1 = |: g7 o- b5 o+ c :| d5 d f g7 r7
C1 = |: c8 d7 g c5 r5 :|
#1 t92 x0.25 v50 |: A1 B1 C1 :|
'''
t = CosTable([(0,0), (64,1), (1024,1), (4096, 0.5), (8191,0)])
mml = MML(a, voices=2, loop=True, poly=4).play()
dur = Sig(mml.getVoice(0, "dur"), mul=2)
tr = TrigEnv(mml.getVoice(0), table=t, dur=dur, mul=mml.getVoice(0, "amp"))
a = SineLoop(freq=mml.getVoice(0, "freq"), feedback=mml.getVoice(0, "x"), mul=tr).mix()
dur2 = Sig(mml.getVoice(1, "dur"), mul=2)
tr2 = TrigEnv(mml.getVoice(1), table=t, dur=dur2, mul=mml.getVoice(1, "amp"))
a2 = LFO(freq=mml.getVoice(1, "freq"), sharp=mml.getVoice(1, "x"), type=2, mul=tr2).mix()
output = STRev([a, a2], inpos=[0.2, 0.8], bal=0.2, mul=1.5).out()

s.gui(locals())