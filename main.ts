input.onButtonPressed(Button.A, function () {
    mode = 1
})
input.onButtonPressed(Button.AB, function () {
    basic.showString("reset ROM")
    syokika()
})
input.onButtonPressed(Button.B, function () {
    basic.showNumber(Math.round(m_deg))
})
function syokika () {
    basic.showString("move 0")
    music.play(music.tonePlayable(262, music.beat(BeatFraction.Whole)), music.PlaybackMode.UntilDone)
    while (pins.digitalReadPin(DigitalPin.P1) == 0) {
    	
    }
    deg_0 = pins.analogReadPin(AnalogPin.P0)
    basic.showString("move 180")
    music.play(music.tonePlayable(262, music.beat(BeatFraction.Whole)), music.PlaybackMode.UntilDone)
    while (pins.digitalReadPin(DigitalPin.P1) == 0) {
    	
    }
    deg_180 = pins.analogReadPin(AnalogPin.P0)
    music.play(music.tonePlayable(262, music.beat(BeatFraction.Whole)), music.PlaybackMode.UntilDone)
    mode = 0
    basic.showIcon(IconNames.Yes)
}
let bf = 0
let deg_180 = 0
let deg_0 = 0
let m_deg = 0
let mode = 0
pins.setPull(DigitalPin.P1, PinPullMode.PullDown)
mode = 999
syokika()
basic.forever(function () {
    if (mode == 1) {
        basic.showIcon(IconNames.Heart)
        while (pins.digitalReadPin(DigitalPin.P1) == 0) {
        	
        }
        bf = pins.analogReadPin(AnalogPin.P0)
        m_deg = Math.map(bf, deg_0, deg_180, 0, 180)
        music.play(music.tonePlayable(262, music.beat(BeatFraction.Whole)), music.PlaybackMode.UntilDone)
        basic.showNumber(Math.round(m_deg))
        mode = 0
    }
})
