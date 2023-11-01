function get_start_position() {
    
    OLED12864_I2C.clear()
    OLED12864_I2C.showString(0, 1, "move to St.", 1)
    basic.showIcon(IconNames.Asleep)
    //  タクトスイッチが押されるまで待つ
    while (pins.digitalReadPin(DigitalPin.P1) == 0) {
        
    }
    bf = pins.analogReadPin(AnalogPin.P0)
    // 可変抵抗の電圧を取得
    // 取得したアナログ値をキャリブレーション値で角度に変換
    m_deg = Math.map(bf, deg_0, deg_180, 0, 180)
    music.play(music.tonePlayable(262, music.beat(BeatFraction.Whole)), music.PlaybackMode.UntilDone)
    bf = Math.round(m_deg)
    // 角度を四捨五入
    let string_bf = bf + " deg"
    OLED12864_I2C.clear()
    OLED12864_I2C.showString(0, 0, "Start deg", 1)
    OLED12864_I2C.showString(0, 1, string_bf, 1)
    start_deg = bf
}

input.onButtonPressed(Button.A, function on_button_pressed_a() {
    
    //  Aボタンで測定開始
    // mode = 1
    OLED12864_I2C.clear()
    OLED12864_I2C.showString(0, 0, "Start Position.", 1)
    get_start_position()
    mode = 1
})
input.onButtonPressed(Button.AB, function on_button_pressed_ab() {
    //  A+Bボタンでキャリブレーション呼び出し
    syokika()
})
function syokika() {
    
    //  キャリブレーション
    OLED12864_I2C.clear()
    OLED12864_I2C.showString(0, 0, "Start Cal", 1)
    OLED12864_I2C.showString(0, 1, "move to 0", 1)
    music.play(music.tonePlayable(262, music.beat(BeatFraction.Whole)), music.PlaybackMode.UntilDone)
    while (pins.digitalReadPin(DigitalPin.P1) == 0) {
        
    }
    deg_0 = pins.analogReadPin(AnalogPin.P0)
    OLED12864_I2C.showString(0, 1, "move to 180", 1)
    music.play(music.tonePlayable(262, music.beat(BeatFraction.Whole)), music.PlaybackMode.UntilDone)
    while (pins.digitalReadPin(DigitalPin.P1) == 0) {
        
    }
    deg_180 = pins.analogReadPin(AnalogPin.P0)
    music.play(music.tonePlayable(262, music.beat(BeatFraction.Whole)), music.PlaybackMode.UntilDone)
    mode = 0
    basic.showIcon(IconNames.Yes)
    OLED12864_I2C.showString(0, 2, "END Cal", 1)
    basic.pause(1000)
    OLED12864_I2C.clear()
    OLED12864_I2C.showString(0, 0, "Measurement  Ready", 1)
    OLED12864_I2C.showString(0, 2, "Start->A", 1)
}

let m_deg = 0
let bf = 0
let deg_180 = 0
let deg_0 = 0
let mode = 0
let start_deg = 0
//  最初に実行する
OLED12864_I2C.init(60)
OLED12864_I2C.showString(0, 0, "ROM 3-78", 1)
basic.pause(3000)
//  角度の測定値を入れる
mode = 999
//  測定過程を入れる(999:準備状態 1:測定中 0:停止)
pins.setPull(DigitalPin.P1, PinPullMode.PullDown)
//  タクトスイッチの入力を安定化させる
syokika()
//  キャリブレーション呼び出し
//  測定ルーチン
//  測定停止
basic.forever(function on_forever() {
    let string_bf: string;
    
    if (mode == 1) {
        //  測定中
        basic.showIcon(IconNames.Heart)
        //  タクトスイッチが押されるまで待つ
        while (pins.digitalReadPin(DigitalPin.P1) == 0) {
            
        }
        bf = pins.analogReadPin(AnalogPin.P0)
        //  可変抵抗の電圧を取得
        //  取得したアナログ値をキャリブレーション値で角度に変換
        m_deg = Math.map(bf, deg_0, deg_180, 0, 180)
        music.play(music.tonePlayable(262, music.beat(BeatFraction.Whole)), music.PlaybackMode.UntilDone)
        bf = Math.round(m_deg)
        //  角度を四捨五入
        string_bf = "" + ("" + bf) + " deg"
        OLED12864_I2C.clear()
        OLED12864_I2C.showString(0, 0, string_bf, 1)
        OLED12864_I2C.showString(0, 2, "measur->A", 1)
        mode = 0
    }
    
})
