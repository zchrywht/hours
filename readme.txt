INSTRUCTIONS

1.  Setting up the Raspberry Pi
    a.  Take the MicroSD card and insert it into the computer, using the full-size SD adapter if necessary.
    b.  Using a text editor (like Notepad), open "wpa_supplicant.conf"
    c.  Replace <<network name>> and <<network password>> with your WiFi network name and password.
    d.  Save and close the file, and copy it to the microSD card's "boot" directory.
    e.  Eject the MicroSD card and insert it into the Raspberry Pi (there is a small slot on the underside, near the indicator lights).
    f.  Using the already attached velcro, place the Raspberry Pi on the back of the clock.

2.  Starting Up
    a.  Plug in the clock and the Raspberry Pi. They require different voltages, so be careful not to swap the power supplies.
    b.  Wait for the indicator light on the side of the clock to change from red to blue. This may take a couple minutes.
    c.  The Raspberry Pi is now connected to the clock over bluetooth, and is also running a local server over WiFi.
    d.  Open "launcher.exe", which will find the Raspberry Pi's local IP address and open a control panel for the clock in your default browser.

3.  Using the Control Panel
    a.  POWER deactivates the clock's display, but does not power off the whole device.
    b.  START begins the time, STOP stops it.
    c.  RESET sets the clock to 00:00:00.
    d.  SET allows you to manually enter a number to display on the clock. START will then count upwards from this number.
    e.  RUN begins at a given time, counts upwards until another time is reached, then resets the clock to zero.
    f.  CYCLE behaves like run, except that after resetting the count will restart, and repeatedly count upwards from zero to the maximum time.
    g.  All times must be entered in format HHMMSS (eg, 23:30:59 should be entered as 233059).
    h.  If RUN or CYCLE are manually interrupted, they cannot be automatically resumed. Instead, re-start the operation using the desired start and end times.