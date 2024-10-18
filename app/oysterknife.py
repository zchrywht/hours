import oysterknife_clock as okClock
import oysterknife_ui as okUI


clock = okUI.Clock()


okClock.begin()
okClock.hardReset()

while True:
    signal = clock.run()
    if signal:

        print(signal)

        if signal == "START":
            okClock.start()
        elif signal == "STOP":
            okClock.stop()
        elif signal.isnumeric():
            okClock.setTime(signal)
        elif signal == "RESTART":
            #okClock.setTime("000000")
            okClock.hardReset()
            okClock.start()
        elif signal == "END":
            okClock.setTime("240000")